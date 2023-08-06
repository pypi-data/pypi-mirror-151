"""Define bookmark commands."""
import typer

BOOKMARK_APP = typer.Typer()


@BOOKMARK_APP.command()
def all():
    """Get all bookmarks."""
    typer.echo("PLACEHOLDER")
