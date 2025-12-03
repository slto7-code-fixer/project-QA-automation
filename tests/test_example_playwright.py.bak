import pytest


def test_example_domain_title(page):
    """مثال يستخدم fixture `page` من `conftest.py` لفتح example.com."""
    page.goto("https://example.com")
    assert "Example Domain" in page.title()
