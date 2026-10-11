"""PyTest fixtures and configuration for Selenium test suite."""

from collections.abc import Generator
import logging
import platform
import re
import subprocess
from typing import Any

import allure
from allure_commons.types import AttachmentType
import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from config import settings

logger = logging.getLogger(__name__)


def _get_chrome_user_agent() -> str:
    """Determine a valid non-headless User-Agent matching the host platform and Chrome version."""
    system = platform.system()
    major_version = "130"
    candidate_commands = [
        "google-chrome --version",
        "chromium --version",
        r"/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version",
    ]
    for cmd in candidate_commands:
        try:
            raw = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode()
            matched = re.search(r"(\d+)\.", raw)
            if matched:
                major_version = matched.group(1)
                break
        except Exception:
            pass

    if system == "Darwin":
        return (
            f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            f"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{major_version}.0.0.0 Safari/537.36"
        )
    if system == "Windows":
        return (
            f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            f"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{major_version}.0.0.0 Safari/537.36"
        )
    return (
        f"Mozilla/5.0 (X11; Linux x86_64) "
        f"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{major_version}.0.0.0 Safari/537.36"
    )


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register command line options for pytest."""
    parser.addoption(
        "--browser",
        action="store",
        default=settings.default_browser,
        help="Browser to run tests: chrome or firefox",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=settings.default_headless,
        help="Run browser in headless mode",
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo[None]
) -> Generator[None, Any, None]:
    """Capture test outcome to check for failures in fixtures."""
    outcome = yield
    rep: pytest.TestReport = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture
def browser(request: pytest.FixtureRequest) -> Generator[webdriver.Remote, None, None]:
    """
    Initialize and tear down WebDriver instance using Selenium Manager.
    Supports Chrome and Firefox, headless execution, and failure screenshots.
    """
    browser_name: str = str(request.config.getoption("--browser"))
    headless: bool = bool(request.config.getoption("--headless"))
    driver: webdriver.Remote

    logger.info("Initializing browser: %s (headless=%s)", browser_name, headless)

    if browser_name.lower() == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        if headless:
            chrome_options.add_argument("--headless=new")
            ua = _get_chrome_user_agent()
            chrome_options.add_argument(f"user-agent={ua}")

        chrome_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=chrome_options)

    elif browser_name.lower() == "firefox":
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")
        firefox_options.set_preference("dom.webdriver.enabled", False)
        firefox_options.set_preference("useAutomationExtension", False)
        if headless:
            firefox_options.add_argument("-headless")

        driver = webdriver.Firefox(options=firefox_options)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    # Set uniform viewport size for cross-browser consistency
    driver.set_window_size(1920, 1080)
    if not headless:
        driver.maximize_window()

    # Configure timeouts for network flakiness resilience
    driver.set_page_load_timeout(settings.page_load_timeout)
    driver.set_script_timeout(settings.script_timeout)

    yield driver

    # Attach screenshot and logs if the test failed
    rep_call = getattr(request.node, "rep_call", None)
    if rep_call and rep_call.failed:
        logger.error("Test %s failed. Capturing diagnostics...", request.node.name)
        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"Failure_Screenshot_{browser_name}",
            attachment_type=AttachmentType.PNG,
        )
        if hasattr(driver, "get_log"):
            try:
                browser_logs = driver.get_log("browser")
                log = "".join([f"{entry['level']}: {entry['message']}\n" for entry in browser_logs])
                allure.attach(log, name="Browser_Console_Logs", attachment_type=AttachmentType.TEXT)
            except (WebDriverException, KeyError, AttributeError):
                pass

    logger.info("Terminating browser session for: %s", request.node.name)
    driver.quit()
