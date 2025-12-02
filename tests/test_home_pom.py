from tests.pages.home_page import HomePage


def test_home_page_pom(page):
    hp = HomePage(page)
    hp.load()
    assert "Example Domain" in hp.title()
