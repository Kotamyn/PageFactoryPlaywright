import pytest
import pytest_asyncio

from asyncio import get_event_loop
from allure import label, step, attach, attachment_type
from datetime import datetime
from playwright.async_api import Page, async_playwright

from pages import *

def pytest_addoption(parser):
    parser.addoption(
      '--brow',
      action="store",
      default='chromium',
      help="Choose browser!",
      choices=("chromium", "firefox", "webkit")
    )
    parser.addoption(
      '--headless',
      action="store",
      default=False,
      help="Choose headless mode!",
      choices=(True, False)
    )

@pytest.fixture(scope="session")
def get_param(request):
    config_param = {}
    config_param["browser"] = request.config.getoption("--brow")
    config_param["headless"] = request.config.getoption("--headless")
    return config_param

@pytest_asyncio.fixture(scope="function")
async def page(get_param):
    async with async_playwright() as playwright:
        __headless = get_param.get("headless")
        match get_param.get("browser").lower():
            case "chromium":
                chromium = await playwright.chromium.launch(headless=__headless)
                yield await chromium.new_page()
            case "firefox":
                firefox = await playwright.firefox.launch(headless=__headless)
                yield await firefox.new_page()
            case "webkit":
                webkit = await playwright.webkit.launch(headless=__headless)
                yield await webkit.new_page()

@pytest_asyncio.fixture(scope="function")
async def home_page(page: Page) -> HomePage:
    with step(f'Opening the home page'):
        await page.goto('https://playwright.dev/', wait_until='networkidle')
    return HomePage(page)

@pytest_asyncio.fixture(scope="function")
async def docs_page(page: Page) -> DocsPage:
    return DocsPage(page)


#хук распределения тестов по папкам
def pytest_collection_modifyitems(session, config, items):
      for test_case in items:
            test_case.add_marker(label("layer", "ui")) # AllureTestOps -> Settings -> Test Layers
            test_case.add_marker(label("epic", "Playwright"))
            test_case.add_marker(label("product", "Autotests"))
            test_case.add_marker(label("component", f"UI"))

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
      outcome = yield
      rep = outcome.get_result()
      if rep.when == "call" and rep.failed:
            task = item.funcargs['event_loop'].create_task(screenshot(item.funcargs['page']))
            item.funcargs['event_loop'].run_until_complete(task)
      return rep

async def screenshot(page: Page) -> None:
    url = page.url
    screen = await page.screenshot()
    with step("Screenshot error"):
        attach(
            screen,
            name=f"{url}|{datetime.now().strftime('%d.%m.%Y %H:%M')}",
            attachment_type=attachment_type.PNG
        )