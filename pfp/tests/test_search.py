import pytest
from allure import title, feature, tag, severity, severity_level

@feature('Search')
@pytest.mark.regress
@pytest.mark.search
class TestHome:

    @title("Search by title -> {keyword}")
    @tag("positive")
    @severity(severity_level.NORMAL)
    @pytest.mark.parametrize('keyword', ["Python", "JavaScript and TypeScript"])
    async def test_search(self, keyword, home_page, docs_page):
        await home_page.navbar.open_search()
        await home_page.navbar.search_modal.find_result(
            keyword, result_number=0
        )
        await docs_page.present(title="Supported languages")