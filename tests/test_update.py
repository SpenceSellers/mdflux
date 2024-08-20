import mdflux


def test_update_does_not_change_tagless_file():
    markdown = """# Heading



[Link](https://link.com)
"""

    res = mdflux.apply_updatemd_str(markdown, "test-file.md")

    assert markdown == res


def test_basic_transpose():
    markdown = \
"""[mdflux]: # (echo "Test String")
[mdflux end]: #
"""

    res = mdflux.apply_updatemd_str(markdown, "test-file.md")

    assert res == \
"""[mdflux]: # (echo "Test String")
Test String

[mdflux end]: #
"""

def test_tags_ignored_in_code_blocks():
    markdown = """
# Heading
```
[mdflux]: # (echo "Test String")
[mdflux end]: #
```
# Heading after
"""

    res = mdflux.apply_updatemd_str(markdown, "test-file.md")

    assert markdown == res

def test_code_argument():
    markdown = """
[mdflux code]: # (echo "Test String")
[mdflux end]: #
"""

    expected_res = """
[mdflux code]: # (echo "Test String")
```
Test String
```
[mdflux end]: #
"""

    res = mdflux.apply_updatemd_str(markdown, "test-file.md")

    assert res == expected_res

def test_code_argument_with_language():
    markdown = """
[mdflux code=javascript]: # (echo "Test String")
[mdflux end]: #
"""

    expected_res = """
[mdflux code=javascript]: # (echo "Test String")
```javascript
Test String
```
[mdflux end]: #
"""

    res = mdflux.apply_updatemd_str(markdown, "test-file.md")

    assert res == expected_res

def test_markdown_is_escaped_by_default():
    markdown = """
[mdflux]: # (echo "_italics_")
[mdflux end]: #
"""

    expected_res = """
[mdflux]: # (echo "_italics_")
\\_italics\\_

[mdflux end]: #
"""

    res = mdflux.apply_updatemd_str(markdown, "test-file.md")

    assert res == expected_res

def test_markdown_in_markdown():
    markdown = """
[mdflux markdown]: # (echo "_italics_")
[mdflux end]: #
"""

    expected_res = """
[mdflux markdown]: # (echo "_italics_")
_italics_

[mdflux end]: #
"""

    res = mdflux.apply_updatemd_str(markdown, "test-file.md")

    assert res == expected_res




