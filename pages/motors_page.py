"""Page Object for the eBay Motors landing page."""

from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from pages.components.header_component import HeaderComponent


class EbayMotorsPage(BasePage):
    """Encapsulate readiness of the Motors destination."""

    def wait_for_page_loaded(self) -> None:
        """Require the Motors title and the working site header."""
        self.wait.until(EC.title_contains("Motors"))
        self.wait_until_visible(HeaderComponent.SEARCH_FIELD)

    def get_title(self) -> str:
        """Return the title only after the Motors page is ready."""
        self.wait_for_page_loaded()
        return super().get_title()
