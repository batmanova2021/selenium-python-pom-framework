"""Check homepage recovery without depending on the live eBay service."""

from unittest.mock import Mock

import pytest
from selenium.common.exceptions import TimeoutException

from pages.home_page import EbayHomePage


def test_recovers_from_ebay_error_page(monkeypatch: pytest.MonkeyPatch) -> None:
    driver = Mock()
    page = EbayHomePage(driver)
    monkeypatch.setattr(page, "wait_for_page_loaded", Mock(side_effect=[TimeoutException(), None]))
    driver.find_elements.return_value = [Mock()]

    page.load_page()

    assert driver.get.call_count == 2
    driver.find_elements.assert_called_once_with(*page.ERROR_PAGE)


@pytest.mark.parametrize("error_page", [True, False])
def test_does_not_hide_persistent_or_unrelated_failures(
    error_page: bool, monkeypatch: pytest.MonkeyPatch
) -> None:
    driver = Mock()
    page = EbayHomePage(driver)
    monkeypatch.setattr(
        page, "wait_for_page_loaded", Mock(side_effect=TimeoutException("not ready"))
    )
    driver.find_elements.return_value = [Mock()] if error_page else []

    with pytest.raises(TimeoutException, match="not ready"):
        page.load_page()

    assert driver.get.call_count == (3 if error_page else 1)


def test_branded_error_title_is_not_homepage_readiness(monkeypatch: pytest.MonkeyPatch) -> None:
    driver = Mock()
    driver.title = "eBay"
    page = EbayHomePage(driver, timeout=0.01)
    visible = Mock(side_effect=TimeoutException("search field missing"))
    monkeypatch.setattr(page, "wait_until_visible", visible)

    with pytest.raises(TimeoutException, match="search field missing"):
        page.wait_for_page_loaded()

    visible.assert_called_once_with(page.header.SEARCH_FIELD)
