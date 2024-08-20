import subprocess
import os

from mdflux.markdown import escape_markdown, get_link_label
from mdflux.tagparsing import parse_tags


def apply_updatemd_file(filename: str, write=True) -> str:
    with open(filename, "r") as f:
        file_contents = f.read()

    result = apply_updatemd_str(file_contents, filename)
    if write:
        with open(filename, "w") as f:
            f.write(result)
    return result


def _exec(cmd: str, file_path: str) -> str:
    file_path = os.path.abspath(file_path)
    cwd = os.path.dirname(file_path)
    res = subprocess.run(cmd, shell=True, check=True, capture_output=True, cwd=cwd)
    return res.stdout.decode("utf-8")


def _ensure_ends_in_newline(s: str) -> str:
    if not s.endswith("\n"):
        return s + "\n"
    else:
        return s


def _prepare_content(
    content: str, code: str | None = None, markdown: bool = False
) -> str:
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


def apply_updatemd_str(input_md: str, filename: str) -> str:
    inside_content_block = False
    lines = input_md.splitlines()
    new_lines = []

    for i, line in enumerate(lines):
        if label := get_link_label(line):
            link_label_name, content_inside_parentheses = label

            link_label_tags = parse_tags(link_label_name)
            if "u" not in link_label_tags:
                continue  # This isn't an updatemd tag

            if "end" in link_label_tags:
                inside_content_block = False
            else:
                new_lines.append(line)  # Preserve the link label
                new_content = _exec(content_inside_parentheses, filename)
                new_lines.append(
                    _prepare_content(
                        new_content,
                        code=link_label_tags.get("code"),
                        markdown="markdown" in link_label_tags,
                    )
                )
                inside_content_block = True

        if not inside_content_block:
            new_lines.append(line)

    return "\n".join(new_lines)


# [comment]: # (This actually is the most platform independent comment)
