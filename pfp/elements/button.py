import allure

from elements.component import Component


class Button(Component):
    
    @property
    def type_of(self) -> str:
        return 'button'

    async def hover(self, **kwargs) -> None:
        with allure.step(f'Hovering over {self.type_of} with name "{self.name}"'):
            locator = await self.get_locator(**kwargs)
            await locator.hover()

    async def double_click(self, **kwargs):
        with allure.step(f'Double clicking {self.type_of} with name "{self.name}"'):
            locator = await self.get_locator(**kwargs)
            await locator.dblclick()
