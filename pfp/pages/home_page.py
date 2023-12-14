from playwright.async_api import Page

from pages import BasePage

class HomePage(BasePage):
    
    def __init__(self, page: Page) -> None:
        super().__init__(page)
