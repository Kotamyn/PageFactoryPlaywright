from abc import ABC, abstractmethod

import allure
from playwright.async_api import Locator, Page, expect


class Component(ABC):

      def __init__(self, page: Page, locator: str, name: str) -> None:
            self.page = page
            self.name = name
            self.locator = locator

      @property
      @abstractmethod
      def type_of(self) -> str:
            return 'component'

      async def get_locator(self, **kwargs) -> Locator:
            locator = self.locator.format(**kwargs)
            return self.page.locator(locator)

      async def click(self, **kwargs) -> None:
            with allure.step(f'Clicking {self.type_of} with name "{self.name}"'):
                  locator = await self.get_locator(**kwargs)
                  await locator.click()

      async def should_be_visible(self, **kwargs) -> None:
            with allure.step(f'Checking that {self.type_of} "{self.name}" is visible'):
                  locator = await self.get_locator(**kwargs)
                  await expect(locator).to_be_visible()

      async def should_have_text(self, text: str, **kwargs) -> None:
            with allure.step(f'Checking that {self.type_of} "{self.name}" has text "{text}"'):
                  locator = await self.get_locator(**kwargs)
                  await expect(locator).to_have_text(text)