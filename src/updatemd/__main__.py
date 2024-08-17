import click

from updatemd import apply_updatemd_file


@click.command()
@click.argument("filename")
def main(filename: str):
    apply_updatemd_file(filename)
    return


if __name__ == "__main__":
    main()
