"""Page Object for the eBay Home Page."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC

from config import settings
from pages.base_page import BasePage
from pages.components.header_component import HeaderComponent


class EbayHomePage(BasePage):
    """Page Object representing the eBay home page."""

    URL: str = settings.base_url
    TITLE_KEYWORD: str = "eBay"

    # Locators specific to the home page body
    MAIN_CONTENT: tuple[str, str] = (By.ID, "mainContent")

    def __init__(self, browser: WebDriver, timeout: float | None = None) -> None:
        super().__init__(browser, timeout)
        self.header = HeaderComponent(browser, timeout)

    @allure.step("Navigate to eBay Home Page")
    def load_page(self) -> None:
        """Navigate to the eBay home page."""
        self.logger.info("Navigating to URL: %s", self.URL)
        self.browser.get(self.URL)

    @allure.step("Wait for Home Page to load")
    def wait_for_page_loaded(self) -> None:
        """Wait until page title contains the expected keyword."""
        self.wait.until(EC.title_contains(self.TITLE_KEYWORD))

    def get_title(self) -> str:
        """Wait for page readiness and return the title."""
        self.wait_for_page_loaded()
        return super().get_title()

    # Convenience delegations to the header component
    def search_item(self, item: str) -> None:
        """Delegate search to header component."""
        self.header.search_item(item)

    def click_motors_link(self) -> None:
        """Delegate motors navigation to header component."""
        self.header.click_motors_link()
