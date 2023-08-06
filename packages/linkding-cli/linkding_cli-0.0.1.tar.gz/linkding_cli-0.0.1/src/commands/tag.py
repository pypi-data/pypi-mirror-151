"""Define tag commands."""
import typer

TAG_APP = typer.Typer()


@TAG_APP.command()
def all():
    """Get all tags."""
    typer.echo("PLACEHOLDER")
