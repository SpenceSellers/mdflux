import shlex
import re

_allowed_tags = ['u', 'code', 'markdown']
def parse_tags(s: str) -> dict[str, str]:
    res = {}
    for tag in shlex.split(s):
        key, _, value = tag.partition('=')
        res[key] = value
    return res

