import click

from updatemd import apply_updatemd_file

@click.group()
def cli():
    pass


@click.command()
@click.argument("filename")
@click.option(
    "--no-write",
    is_flag=True,
    help="Output updated content on stdout without modifying the file.",
)
def main(filename: str, no_write: bool = False):
    result = apply_updatemd_file(filename, write=not no_write)
    if no_write:
        print(result)


if __name__ == "__main__":
    cli()
