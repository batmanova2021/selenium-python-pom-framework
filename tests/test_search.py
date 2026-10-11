"""Regression tests for single item search on eBay."""

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.home_page import EbayHomePage
from pages.search_result_page import EbaySearchResultPage


@pytest.mark.regressiontest
def test_search_sunglasses(browser: WebDriver) -> None:
    """Verify that searching for 'sunglasses' loads results matching the query."""
    home_page = EbayHomePage(browser)
    search_result_page = EbaySearchResultPage(browser)
    search_item = "sunglasses"

    home_page.load_page()
    assert "eBay" in home_page.get_title()

    home_page.search_item(search_item)
    actual_title = search_result_page.wait_for_search_results(search_item)
    assert search_item.lower() in actual_title.lower(), (
        f"Expected '{search_item}' in title, but got '{actual_title}'"
    )
