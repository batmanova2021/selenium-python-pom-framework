"""Page Object for the eBay Home Page."""

import allure
from selenium.common.exceptions import TimeoutException
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
    ERROR_PAGE: tuple[str, str] = (
        By.XPATH,
        "//*[contains(normalize-space(.), 'Something went wrong on our end') and not(*)]",
    )

    def __init__(self, browser: WebDriver, timeout: float | None = None) -> None:
        super().__init__(browser, timeout)
        self.header = HeaderComponent(browser, timeout)

    @allure.step("Navigate to eBay Home Page")
    def load_page(self) -> None:
        """Navigate to the eBay home page."""
        self.logger.info("Navigating to URL: %s", self.URL)
        self.browser.get(self.URL)
        for attempt in range(3):
            try:
                self.wait_for_page_loaded()
                return
            except TimeoutException:
                if attempt == 2 or not self.browser.find_elements(*self.ERROR_PAGE):
                    raise
                self.logger.warning("eBay returned its error page; retrying homepage load")
                self.browser.get(self.URL)

    @allure.step("Wait for Home Page to load")
    def wait_for_page_loaded(self) -> None:
        """Require the real homepage header, not just an eBay-branded error title."""
        self.wait.until(EC.title_contains(self.TITLE_KEYWORD))
        self.wait_until_visible(HeaderComponent.SEARCH_FIELD)

    def get_title(self) -> str:
        """Wait for page readiness and return the title."""
        self.wait.until(EC.title_contains(self.TITLE_KEYWORD))
        return super().get_title()

    # Convenience delegations to the header component
    def search_item(self, item: str) -> None:
        """Delegate search to header component."""
        self.header.search_item(item)

    def click_motors_link(self) -> None:
        """Delegate motors navigation to header component."""
        self.header.click_motors_link()
