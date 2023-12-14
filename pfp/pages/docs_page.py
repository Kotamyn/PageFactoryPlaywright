from playwright.async_api import Page

from elements import Title
from pages import BasePage

class DocsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.title = Title(page, locator="header > h1", name='Doc Title')

    async def present(self, title: str) -> None:
        await self.title.should_be_visible(title=title)
        await self.title.should_have_text(
            title.capitalize(), title=title
        )

