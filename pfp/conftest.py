import os
import pytest
import pytest_asyncio

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
        browser_type = get_param.get("browser").lower()
        browser = getattr(playwright, browser_type)
        context = await browser.launch(headless=__headless)
        video_context = await context.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir="videos/",
            record_video_size={"width": 1920, "height": 1080}
        )
        yield await video_context.new_page()
        await video_context.close()
        await context.close()


@pytest_asyncio.fixture(scope="function")
async def home_page(page: Page) -> HomePage:
    with step(f'Opening the home page'):
        await page.goto('https://playwright.dev/', wait_until='networkidle')
    return HomePage(page)

@pytest_asyncio.fixture(scope="function")
async def docs_page(page: Page) -> DocsPage:
    return DocsPage(page)


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
    if rep.when == "call":
        page = item.funcargs['page']
        loop = item.funcargs['event_loop']
        if rep.failed:
            # Attach video & screenshot if test failed
            loop.run_until_complete(screenshot_and_video(page))
        elif rep.outcome == "passed":
            # Remove video if test passed
            loop.run_until_complete(delete_video(page))
    return rep

async def screenshot_and_video(page: Page) -> None:
    url = page.url
    screen = await page.screenshot()
    with step("Screenshot error"):
        attach(
            screen,
            name=f"{url}|{datetime.now().strftime('%d.%m.%Y %H:%M')}",
            attachment_type=attachment_type.PNG
        )
    with step("Video error"):
        video_path = await page.video.path()
        await page.context.close() # Recording is finalized
        with open(video_path, "rb") as video_file:
            attach(
                video_file.read(),
                name=f"{url}|video",
                attachment_type=attachment_type.WEBM
            )

async def delete_video(page: Page) -> None:
    video_path = await page.video.path()
    if os.path.exists(video_path):
        os.remove(video_path)
