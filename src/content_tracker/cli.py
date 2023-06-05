from typer import Typer

from .main import ContentTracker


def cli(tracker: ContentTracker) -> Typer:
    contents_app = Typer()
    contents_app.command("add")(tracker.add_content)
    contents_app.command("list")(tracker.list_contents)

    changes_app = Typer()
    changes_app.command("list")(tracker.list_changes)

    app = Typer(context_settings={"help_option_names": ["-h", "--help"]})
    app.add_typer(contents_app, name="contents")
    app.add_typer(changes_app, name="changes")
    return app
