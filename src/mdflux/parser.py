from dataclasses import dataclass
import shlex
import click
from typing import Generator
from .markdown import get_link_label


def parse_tags(s: str) -> dict[str, str]:
    res = {}
    for tag in shlex.split(s):
        key, _, value = tag.partition("=")
        res[key] = value
    return res


@dataclass
class SourceLine:
    line: str
    line_number: int


@dataclass
class MarkdownLine(SourceLine):
    pass


@dataclass
class OldContentLine(SourceLine):
    pass


@dataclass
class MdfluxExecuteTagLine(SourceLine):
    link_label_tags: dict[str, str]
    content_inside_parens: str


@dataclass
class MdfluxEndLine(SourceLine):
    pass


def parse_mdflux_file(input_md: str) -> Generator[SourceLine, None, None]:
    """Splits a markdown document into a series of lines, marked with what they mean to us."""
    inside_content_block = False
    inside_code_block = False  # mdflux tags can't be used inside code blocks, because link labels can't be used inside code blocks.
    lines = input_md.splitlines()
    for i, line in enumerate(lines):
        if "```" in line:
            inside_code_block = not inside_code_block

        if not inside_code_block and (label := get_link_label(line)):
            link_label_name, content_inside_parentheses = label

            link_label_tags = parse_tags(link_label_name)

            if "mdflux" in link_label_tags:
                if "end" in link_label_tags:
                    inside_content_block = False
                    yield MdfluxEndLine(line, i)
                else:
                    if inside_content_block:
                        # It's very easy to accidentally forget an [mdflux end] tag
                        raise MdfluxFormatError(
                            f"Line {i + 1}: Encountered a non-end [mdflux] tag while already in an [mdflux] block. Are you missing an `[mdflux end]: #` ?"
                        )
                    yield MdfluxExecuteTagLine(
                        line, i, link_label_tags, content_inside_parentheses
                    )
                    inside_content_block = True
            else:
                # It's a link label, but not an mdflux link label. To us it's just markdown then.
                yield MarkdownLine(line, i)
        else:
            # It's just regular markdown.
            # Maybe it's a link-label inside a code block, but that means it's not a real link label.
            yield MarkdownLine(line, i)


class MdfluxFormatError(click.ClickException):
    """We ran into trouble parsing this markdown document"""

    pass
