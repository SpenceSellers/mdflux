# mdflux

Mdflux is a utility which facilitates keeping Markdown files up-to-date by allowing you to invisibly embed shell commands into the markdown document, the output of which will be transposed into the same document.


## Basic usage & concept
Mdflux transposes shell command output between an `[mdflux]` opening line and an `[mdflux end]` closing line:
```
[mdflux]: # (echo "Hello World")
[mdflux end]: #
```
After running `mdflux update my-file.md`, mdflux will run `echo "Hello World"` and insert the output between the two mdflux tags. This will become:
```
[mdflux]: # (echo "Hello World")
Hello World
[mdflux end]: #
```

The mdflux tags are invisible, Markdown renderers such as Github will render this as simply:

[mdflux]: # (echo "Hello World")
Hello World

[mdflux end]: #

Any old or outdated content between the opening and closing tags will be replaced with the new content. It's safe to run `mflux update` multiple times, duplicate insertions won't happen.



## How it works
mdflux works by using (abusing) [Markdown Reference-Style Links](https://www.markdownguide.org/basic-syntax/#reference-style-links). This is the most reliable way to create invisible syntax elements in markdown across nearly all markdown renderers.

In their normal usage, reference-style links work like this:
```
I use [my favorite search engine][1] to browse the web

[1]: https://google.com (Google)
```
It's meant to allow re-using links inside of a markdown document, or simply making the document easier to edit.

However, if the link label is never used, it simply isn't rendered. That gives us a way to embed invisible instructions in a markdown document. 

Here's the anatomy of a link label being used as an mdflux tag:
```
[mdflux]: # (echo "Hello World")                 
 ▲        ▲  ▲                                   
 │        │  └─Optional page title (used as shell command)
 │        │                                      
 │        └─URL (ignored by mdflux)              
 │                                               
 └─Link name (used as mdflux instructions)       
```

## Complete syntax
### Basic usage
```
[mdflux]: # (echo "Hello World")
[mdflux end]: #
```
Yields:
```
Hello World
```

### Code blocks
Use the `code` argument to enclose the content in a code block:
```
[mdflux code]: # (echo "Hello World")
[mdflux end]: #
```
Yields:
````
```
Hello World
```
````

### Code blocks with language
Optionally specify a language for the code block:
```
[mdflux code=python]: # (echo "return 1 + 2")
[mdflux end]: #
```
Yields:
````python
```python
return 1 + 2
```
````

### Embedding Markdown in Markdown
By default, any content that mdflux inserts into a markdown document is escaped: `_some text_` becomes `\_some text\_`.

However, the `markdown` argument allows opting-in to rendering content as markdown without escaping it:
```
[mdflux markdown]: # (echo "_some text_")
[mdflux end] #
```
Yields:
```
_some text_
```
Rendered as:Hello World

_some text_




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
[mdflux end]: #

### mdflux update
[mdflux code]: # (mdflux update --help)
```
Usage: mdflux update [OPTIONS] FILENAME

  Update a markdown file using the embedded mdflux shell commands.

Options:
  --no-write  Output updated content on stdout without modifying the file.
  --help      Show this message and exit.
```
[mdflux end]: #

### mdflux escape
[mdflux code]: # (mdflux escape --help)
```
Usage: mdflux escape [OPTIONS] [FILE]

  Escape markdown so that it's safe to embed in markdown.

  Turns [search](https://google.com) into \[search\]\(https://google.com\)
  etc.

  FILE is optional, and will default to stdin if not provided.

Options:
  --help  Show this message and exit.
```
[mdflux end]: #