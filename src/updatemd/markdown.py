import re
from typing import Tuple

def _unescape_string(s):
    backslash_placeholder = '63f74ada-71f4-407d-a01c-f8ec61f558e8'
    
    # Replace double backslashes with a temporary placeholder
    s = s.replace("\\\\", backslash_placeholder)
    # Unescape all other escaped characters
    s = re.sub(r'\\(.)', r'\1', s)
    # Restore the backslashes
    s = s.replace(backslash_placeholder, "\\")
    return s



def get_link_label(line: str) -> Tuple[str, str] | None:
    link_label_pattern = r"\[(.*?)\]:\s*#?\s*\((.*)\)"
    match = re.search(link_label_pattern, line)
    if match:

        return match.group(1), _unescape_string(match.group(2))
    else:
        return None


def escape_markdown(text: str) -> str:
    escape_chars = r'[\*_\{\}\[\]\#\+\-\.\!`]'
    return re.sub(escape_chars, r'\\\g<0>', text)