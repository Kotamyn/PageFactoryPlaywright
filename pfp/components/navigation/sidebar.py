from playwright.sync_api import Page
from allure import step

from elements import Link


class Sidebar:
    def __init__(self, page: Page) -> None:
        self.page = page

        self.sidebar_link = Link(page, locator="//a[contains(@href, '{url}') and text()='{title}']",
                                       name='sidebar_title')

    async def visit(self, url: str, title: str) -> None:
        with step(f'Opening the url "{url}"'):
            await self.sidebar_link.click(url=url, title=title.capitalize())
