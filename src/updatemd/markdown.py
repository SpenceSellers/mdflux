import re
from typing import Tuple


def get_link_label(line: str) -> Tuple[str, str] | None:
    link_label_pattern = r"\[(.*?)\]:\s*#?\s*\((.*)\)"
    match = re.search(link_label_pattern, line)
    if match:

        return match.group(1), match.group(2).replace('\\)', ')')
    else:
        return None
