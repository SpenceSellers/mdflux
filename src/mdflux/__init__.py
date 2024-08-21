from mdflux.markdown import escape_markdown
from . import shell
from . import parser


def apply_mdflux_str(input_md: str, filename: str) -> str:
    """Runs all mdflux tags in a markdown document and returns the new version of the document"""
    parsed_lines = list(parser.parse_mdflux_file(input_md))

    # If we need the count to display progress in the future:
    # count_to_run = sum(isinstance(x, parser.MdfluxExecuteTagLine) for x in parsed_lines)

    new_lines = []
    for line in parsed_lines:
        match line:
            case parser.MarkdownLine() | parser.MdfluxEndLine():
                new_lines.append(line.line)
            case parser.OldContentLine():
                pass  # Just get rid of old content
            case parser.MdfluxExecuteTagLine():
                new_lines.append(line.line)  # Preserve the link label
                exec_result = shell.exec(line.content_inside_parens, filename)
                new_content = (
                    exec_result.stdout
                    if "stderr" not in line.link_label_tags
                    else exec_result.stderr
                )
                new_lines.append(
                    _prepare_content(
                        new_content,
                        code=line.link_label_tags.get("code"),
                        markdown="markdown" in line.link_label_tags,
                    )
                )
            case _:
                raise ValueError("Unexpected line type", line)
    return _ensure_ends_in_newline("\n".join(new_lines))


def apply_mdflux_file(filename: str, write=True) -> str:
    """Runs all mdflux tags in a file and optionally saves the file.

    Returns the updated document either way."""
    with open(filename, "r") as f:
        file_contents = f.read()

    result = apply_mdflux_str(file_contents, filename)
    if write:
        with open(filename, "w") as f:
            f.write(result)
    return result


def _ensure_ends_in_newline(s: str) -> str:
    if not s.endswith("\n"):
        return s + "\n"
    else:
        return s


def _prepare_content(
    content: str, code: str | None = None, markdown: bool = False
) -> str:
    """Renders and escapes a string so that it can be included into a markdown document, using the supplied settings."""
    content = _ensure_ends_in_newline(content.strip())
    if code is not None:
        return f"```{code}\n{content}```"
    elif markdown:
        return content
    else:
        # Putting \ at the end of a markdown line creates a single-line break. Hence the \\\n
        return (
            "\\\n".join(line for line in escape_markdown(content).splitlines()) + "\n"
        )
