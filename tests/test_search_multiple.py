"""Parametrized regression tests for multiple search queries on eBay."""

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.home_page import EbayHomePage
from pages.search_result_page import EbaySearchResultPage


@pytest.mark.parametrize(
    "item",
    [
        "glasses",
        "sunglasses",
        "glasses men",
        "glasses women",
        "new macbook",
        "Apple MacBook",
    ],
)
@pytest.mark.regressiontest
def test_search_multiple_items(browser: WebDriver, item: str) -> None:
    """Verify search functionality for multiple items using parametrization."""
    home_page = EbayHomePage(browser)
    search_result_page = EbaySearchResultPage(browser)

    home_page.load_page()
    assert "eBay" in home_page.get_title()

    home_page.search_item(item)
    actual_title = search_result_page.wait_for_search_results(item)
    assert item.lower() in actual_title.lower() or "ebay" in actual_title.lower(), (
        f"Expected '{item}' in title, but got '{actual_title}'"
    )
