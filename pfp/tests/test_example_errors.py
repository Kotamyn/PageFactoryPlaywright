from allure import (
    feature
)

@feature('Example of test case logging with failde status')
class TestErrors:

    async def test_example_failed_status(self, home_page, docs_page):
        await home_page.navbar.visit_docs()
        await docs_page.sidebar.visit(
            url="/docs/intro", title="Errors"
        )
        await docs_page.present(title="Errors")


