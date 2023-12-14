import pytest
from allure import (
    title,
    feature,
    tag,
    severity,
    severity_level
)

@feature('Docs')
@pytest.mark.regress
@pytest.mark.docs
class TestDocs:

    @title("Check sidebar docs -> {sidebar_title}")
    @tag("positive")
    @severity(severity_level.NORMAL)
    @pytest.mark.parametrize(('sidebar_url', 'sidebar_title'),
                                [
                                    ("/docs/intro", "Installation"),
                                    ("/docs/writing-tests", "Writing tests")
                                ]
                            )
    async def test_check_sidebar_docs(self, sidebar_url, sidebar_title, home_page, docs_page):
        await home_page.navbar.visit_docs()
        await docs_page.sidebar.visit(
            url=sidebar_url, title=sidebar_title
        )
        await docs_page.present(title=sidebar_title)


