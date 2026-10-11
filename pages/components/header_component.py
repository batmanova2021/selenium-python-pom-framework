"""Component Object representing the eBay universal header navigation bar."""

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage


class HeaderComponent(BasePage):
    """Encapsulates the global header, search input, and top navigation links."""

    SEARCH_FIELD: tuple[str, str] = (By.ID, "gh-ac")
    SEARCH_BUTTON: tuple[str, str] = (By.ID, "gh-btn")
    MOTORS_LINK: tuple[str, str] = (By.PARTIAL_LINK_TEXT, "Motors")

    @allure.step("Search for item: '{item}'")
    def search_item(self, item: str) -> None:
        """Type search item and submit using ENTER key."""
        self.logger.info("Searching for item: '%s'", item)
        search_field = self.wait_until_visible(self.SEARCH_FIELD)
        search_field.clear()
        search_field.send_keys(item + Keys.ENTER)

    @allure.step("Clear search input")
    def clear_search_field(self) -> None:
        """Clear search input field."""
        self.logger.info("Clearing search input field")
        search_field = self.wait_until_visible(self.SEARCH_FIELD)
        search_field.clear()

    @allure.step("Click search button")
    def click_search_button(self) -> None:
        """Click the primary search button."""
        self.logger.info("Clicking search button")
        search_button = self.wait_until_clickable(self.SEARCH_BUTTON)
        search_button.click()

    @allure.step("Click Motors navigation link")
    def click_motors_link(self) -> None:
        """Click on the eBay Motors header link."""
        self.logger.info("Clicking Motors header link")
        self.wait_until_visible(self.MOTORS_LINK)
        motors_link = self.wait_until_clickable(self.MOTORS_LINK)
        motors_link.click()
