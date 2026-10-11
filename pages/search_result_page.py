"""Page Object for the eBay Search Results Page."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.components.header_component import HeaderComponent


class EbaySearchResultPage(BasePage):
    """Page Object representing the eBay search results page."""

    RESULTS_CONTAINER: tuple[str, str] = (By.CLASS_NAME, "srp-results")

    def __init__(self, browser: WebDriver, timeout: float | None = None) -> None:
        super().__init__(browser, timeout)
        self.header = HeaderComponent(browser, timeout)

    @allure.step("Wait for search results to load for item: '{item}'")
    def wait_for_search_results(self, item: str) -> str:
        """Wait for the requested query and visible results before returning the title."""
        self.logger.info("Waiting for search results page for: '%s'", item)
        self.wait.until(lambda driver: item.casefold() in driver.title.casefold())
        self.wait_until_visible(self.RESULTS_CONTAINER)
        return self.get_title()

    def get_title(self) -> str:
        """Wait for page readiness and return title."""
        self.wait.until(EC.title_contains("eBay"))
        return super().get_title()

    def search_item(self, item: str) -> None:
        """Delegate search to header component."""
        self.header.search_item(item)
