"""Base Page Object class encapsulating common driver setup, explicit waits, and logging."""

import logging

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import settings


class BasePage:
    """Base class for all Page Objects. Handles driver setup, explicit waits, and logging."""

    def __init__(self, browser: WebDriver, timeout: float | None = None) -> None:
        self.browser = browser
        self.timeout = timeout or settings.default_timeout
        self.wait = WebDriverWait(self.browser, self.timeout)
        self.logger = logging.getLogger(self.__class__.__name__)

    def wait_until_visible(self, locator: tuple[str, str]) -> WebElement:
        """Wait until an element located by locator is visible on the page."""
        self.logger.debug("Waiting for visibility of element located by: %s", locator)
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_until_clickable(self, locator: tuple[str, str]) -> WebElement:
        """Wait until an element located by locator is clickable."""
        self.logger.debug("Waiting for element to be clickable: %s", locator)
        return self.wait.until(EC.element_to_be_clickable(locator))

    def get_title(self) -> str:
        """Return the current browser page title."""
        title = self.browser.title
        self.logger.debug("Current page title: '%s'", title)
        return title

    def get_current_url(self) -> str:
        """Return the current browser URL."""
        return self.browser.current_url
