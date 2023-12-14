from playwright.sync_api import Page

from elements import Title, Input, ListItem


class SearchModal:
    def __init__(self, page: Page) -> None:
        self.page = page

        self.empty_results_title = Title(
            page, locator='p.DocSearch-Help', name='Empty results'
        )
        self.search_input = Input(
            page, locator='#docsearch-input', name='Search docs'
        )
        self.search_result = ListItem(
            page, locator='#docsearch-item-{result_number}', name='Result item'
        )

    async def modal_is_opened(self):
        await self.search_input.should_be_visible()
        await self.empty_results_title.should_be_visible()

    async def find_result(self, keyword: str, result_number: int) -> None:
        await self.search_input.fill(keyword, validate_value=True)
        await self.search_result.click(result_number=result_number)
