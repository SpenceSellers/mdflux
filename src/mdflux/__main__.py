import sys
import click

from mdflux import apply_updatemd_file
from mdflux.markdown import escape_markdown

@click.group()
def cli():
    pass


@cli.command()
@click.argument("filename")
@click.option(
    "--no-write",
    is_flag=True,
    help="Output updated content on stdout without modifying the file.",
)
def update(filename: str, no_write: bool = False):
    """Update a markdown file using the embedded mdflux shell commands."""
    result = apply_updatemd_file(filename, write=not no_write)
    if no_write:
        print(result)

@cli.command()
@click.argument("file", type=click.File('r'), default=sys.stdin)
def escape(file):
    """Escape markdown so that it's safe to embed in markdown.
    
    Turns [search](https://google.com) into \\[search\\]\\(https://google.com\\) etc."""
    print(escape_markdown(file.read()))


if __name__ == "__main__":
    cli()
