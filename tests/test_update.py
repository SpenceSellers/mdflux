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

