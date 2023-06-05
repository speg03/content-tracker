from typing import Optional, Sequence

from ..models import ChangedContent, Content
from .base import Database


class BigQuery(Database):
    def __init__(self, dataset: str, project: Optional[str] = None) -> None:
        """Initialize BigQuery database.

        Args:
            dataset (str): Dataset name.
            project (Optional[str], optional): Project name. Defaults to None.
        """
        from google.cloud.bigquery import Client

        self.project = project
        self.dataset = dataset
        if self.project:
            self.contents_table = f"{self.project}.{self.dataset}.contents"
            self.content_histories_table = (
                f"{self.project}.{self.dataset}.content_histories"
            )
        else:
            self.contents_table = f"{self.dataset}.contents"
            self.content_histories_table = f"{self.dataset}.content_histories"

        self._client = Client()

    def insert_or_update_content(self, content: Content) -> None:
        from google.cloud.bigquery import QueryJobConfig, ScalarQueryParameter

        sql = f"""
            MERGE `{self.contents_table}` AS target
            USING (
                SELECT
                    @id AS id,
                    @title AS title,
                    @body AS body,
                    @created_at AS created_at,
                    @updated_at AS updated_at
            ) AS source
            ON target.id = source.id
            WHEN MATCHED THEN
                UPDATE SET
                    target.title = source.title,
                    target.body = source.body,
                    target.updated_at = source.updated_at
            WHEN NOT MATCHED THEN
                INSERT ROW
        """
        job_config = QueryJobConfig(
            query_parameters=[
                ScalarQueryParameter("id", "STRING", content.id),
                ScalarQueryParameter("title", "STRING", content.title),
                ScalarQueryParameter("body", "STRING", content.body),
                ScalarQueryParameter("created_at", "TIMESTAMP", content.created_at),
                ScalarQueryParameter("updated_at", "TIMESTAMP", content.updated_at),
            ]
        )
        self._client.query(sql, job_config=job_config).result()

    def insert_content_history(self, content: Content) -> None:
        table = self._client.get_table(self.content_histories_table)
        errors = self._client.insert_rows(
            table,
            [
                dict(
                    content_id=content.id,
                    title=content.title,
                    body=content.body,
                    created_at=content.updated_at,
                )
            ],
        )
        if errors:
            raise RuntimeError(f"Failed to insert content history: {errors}")

    def list_contents(self) -> Sequence[Content]:
        table = self._client.get_table(self.contents_table)
        results = self._client.list_rows(table)
        return [Content(**row) for row in results]

    def list_changed_contents(
        self, intervals: int = 24, part: str = "HOUR"
    ) -> Sequence[ChangedContent]:
        from google.cloud.bigquery import QueryJobConfig, ScalarQueryParameter

        # Validate part for DATETIME_DIFF
        # see: https://cloud.google.com/bigquery/docs/reference/standard-sql/datetime_functions#datetime_diff
        valid_parts = (
            "MICROSECOND",
            "MILLISECOND",
            "SECOND",
            "MINUTE",
            "HOUR",
            "DAY",
            "WEEK",
            "WEEK(SUNDAY)",
            "WEEK(MONDAY)",
            "WEEK(TUESDAY)",
            "WEEK(WEDNESDAY)",
            "WEEK(THURSDAY)",
            "WEEK(FRIDAY)",
            "WEEK(SATURDAY)",
            "ISOWEEK",
            "MONTH",
            "QUARTER",
            "YEAR",
        )
        part_upper = part.upper()
        if part_upper not in valid_parts:
            raise ValueError(
                f"Invalid part: {part}. Valid parts are {', '.join(valid_parts)}."
            )

        sql = f"""
            WITH contents_with_lags AS (
                SELECT
                    *,
                    LAG(body) OVER (
                        PARTITION BY content_id ORDER BY created_at
                    ) AS previous_body
                FROM `{self.content_histories_table}`
            )
            SELECT *
            FROM contents_with_lags
            WHERE
                body != previous_body
                AND DATETIME_DIFF(
                    CURRENT_DATETIME,
                    DATETIME(created_at),
                    {part_upper}
                ) <= @intervals
        """
        job_config = QueryJobConfig(
            query_parameters=[ScalarQueryParameter("intervals", "INTEGER", intervals)]
        )
        results = self._client.query(sql, job_config=job_config).result()
        return [ChangedContent(**row) for row in results]
