import allure
from playwright.async_api import Page

from components import *


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.navbar = Navbar(page)
        self.sidebar = Sidebar(page)

    async def visit(self, url: str) -> None:
        with allure.step(f'Opening the url "{url}"'):
            await self.page.goto(url, wait_until='networkidle')

    async def reload(self) -> None:
        with allure.step(f'Reloading page with url "{self.page.url}"'):
            await self.page.reload(wait_until='domcontentloaded')
