"""Guard against search false positives and missing result content."""

from unittest.mock import Mock

import pytest
from selenium.common.exceptions import TimeoutException

from pages.search_result_page import EbaySearchResultPage


def test_branded_title_without_query_is_not_search_success() -> None:
    driver = Mock()
    driver.title = "Error Page | eBay"
    page = EbaySearchResultPage(driver, timeout=0.01)

    with pytest.raises(TimeoutException):
        page.wait_for_search_results("glasses")


def test_query_title_without_results_is_not_search_success() -> None:
    driver = Mock()
    driver.title = "Glasses | eBay"
    driver.find_element.side_effect = TimeoutException("results missing")
    page = EbaySearchResultPage(driver, timeout=0.01)

    with pytest.raises(TimeoutException, match="results missing"):
        page.wait_for_search_results("glasses")


def test_search_requires_visible_results() -> None:
    driver = Mock()
    driver.title = "Glasses | eBay"
    driver.find_element.return_value.is_displayed.return_value = True
    page = EbaySearchResultPage(driver, timeout=0.01)

    assert page.wait_for_search_results("glasses") == "Glasses | eBay"
    driver.find_element.assert_called_once_with(*page.RESULTS_CONTAINER)
