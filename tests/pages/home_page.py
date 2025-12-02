class HomePage:
    """Page Object for https://example.com minimal interactions."""

    def __init__(self, page):
        self.page = page
        self.url = "https://example.com"

    def load(self):
        self.page.goto(self.url)

    def title(self):
        return self.page.title()
