# mdflux

Mdflux is a utility which facilitates keeping Markdown files up-to-date by allowing you to invisibly embed shell commands into the markdown document, the output of which will be transposed into the same document.


## Markdown syntax
```
[mdflux code]: # (mdflux --help)
```

## CLI usage
[mdflux code]: # (mdflux --help)
```
Usage: mdflux [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  escape  Escape markdown so that it's safe to embed in markdown.
  update  Update a markdown file using the embedded mdflux shell commands.
```
[u end]: # ()

### mdflux update
[mdflux code]: # (mdflux update --help)
```
Usage: mdflux update [OPTIONS] FILENAME

  Update a markdown file using the embedded mdflux shell commands.

Options:
  --no-write  Output updated content on stdout without modifying the file.
  --help      Show this message and exit.
```
[mdflux end]: # ()

### mdflux escape
[mdflux code]: # (mdflux escape --help)
```
Usage: mdflux escape [OPTIONS] [FILE]

  Escape markdown so that it's safe to embed in markdown.

  Turns [search](https://google.com) into \[search\]\(https://google.com\)
  etc.

Options:
  --help  Show this message and exit.
```
[mdflux end]: # ()