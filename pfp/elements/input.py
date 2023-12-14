import allure
from playwright.async_api import expect

from elements.component import Component


class Input(Component):
    
    @property
    def type_of(self) -> str:
        return 'input'

    async def fill(self, value: str, validate_value=False, **kwargs):
        with allure.step(f'Fill {self.type_of} "{self.name}" to value "{value}"'):
            locator = await self.get_locator(**kwargs)
            await locator.fill(value)

            if validate_value:
                await self.should_have_value(value, **kwargs)

    async def should_have_value(self, value: str, **kwargs):
        with allure.step(f'Checking that {self.type_of} "{self.name}" has a value "{value}"'):
            locator = await self.get_locator(**kwargs)
            await expect(locator).to_have_value(value)
