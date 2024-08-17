import subprocess
import os

from updatemd.markdown import get_link_label
from updatemd.tagparsing import parse_tags

def apply_updatemd_file(filename: str):
    with open(filename, "r") as f:
        file_contents = f.read()
    
    result = apply_updatemd_str(file_contents, filename)
    with open(filename, "w") as f:
        f.write(result)


def _exec(cmd: str, file_path: str) -> str:

    cwd = os.path.dirname(file_path)
    res = subprocess.run(cmd, shell=True, check=True, capture_output=True, cwd=cwd)
    return res.stdout.decode("utf-8")

def _ensure_ends_in_newline(s: str) -> str:
    if not s.endswith('\n'):
        return s + '\n'
    else:
        return s


def _prepare_content(content: str, code: str | None = None, markdown: bool = False) -> str:
    content = _ensure_ends_in_newline(content.strip())
    if code is not None:
        return f"```{code}\n{content}```"
    elif markdown:
        return content
    else:
        # This puts a newline at the end, which we actually need because link labels seem to need a newline in
        # front of them, unless they're after a code block (??)
        return "\n".join(line + "\n" for line in content.splitlines())


def apply_updatemd_str(input_md: str, filename: str) -> str:
    inside_content_block = False
    lines = input_md.splitlines()
    new_lines = []

    for i, line in enumerate(lines):
        if label := get_link_label(line):
            link_label_name, content_inside_parentheses = label
            print(f"Processing {link_label_name=}, {content_inside_parentheses=}")

            link_label_tags = parse_tags(link_label_name)
            print(repr(link_label_tags))
            if "u" not in link_label_tags:
                continue  # This isn't an updatemd tag

            if "end" in link_label_tags:
                inside_content_block = False
            else:
                new_lines.append(line)  # Preserve the link label
                new_content = _exec(content_inside_parentheses, filename)
                new_lines.append(
                    _prepare_content(new_content, code=link_label_tags.get("code"), markdown="markdown" in link_label_tags)
                )
                inside_content_block = True

        if not inside_content_block:
            new_lines.append(line)

    return "\n".join(new_lines)


# [comment]: # (This actually is the most platform independent comment)
