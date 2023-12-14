from playwright.sync_api import Page

from components import SearchModal
from elements import Button, Link


class Navbar:
    def __init__(self, page: Page) -> None:
        self.page = page

        self.search_modal = SearchModal(page)

        self.api_link = Link(page, locator="//a[text()='API']", name='API')
        self.docs_link = Link(page, locator="//a[text()='Docs']", name='Docs')
        self.community_link = Link(page, locator="//a[text()='Community']", name='Community')
        self.search_button = Button(
            page, locator="button.DocSearch-Button", name='Search'
        )

    async def visit_docs(self) -> None:
        await self.docs_link.click()

    async def visit_api(self) -> None:
        await self.api_link.click()

    async def visit_community(self) -> None:
        await self.community_link.click()

    async def open_search(self) -> None:
        await self.search_button.should_be_visible()

        await self.search_button.hover()
        await self.search_button.click()

        await self.search_modal.modal_is_opened()
