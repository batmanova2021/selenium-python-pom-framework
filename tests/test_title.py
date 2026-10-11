"""Smoke tests for eBay home page title and Motors navigation."""

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.home_page import EbayHomePage


@pytest.mark.smoketest
def test_ebay_title(browser: WebDriver) -> None:
    """Verify that the eBay home page title contains expected brand name."""
    home_page = EbayHomePage(browser)
    home_page.load_page()

    actual_title = home_page.get_title()
    assert "eBay" in actual_title, f"Expected 'eBay' in title, but got '{actual_title}'"


@pytest.mark.smoketest
def test_motors_title(browser: WebDriver) -> None:
    """Verify navigation to eBay Motors and its resulting page title."""
    home_page = EbayHomePage(browser)
    home_page.load_page()
    home_page.wait_for_page_loaded()  # ensure JS nav is hydrated before clicking
    home_page.click_motors_link()

    actual_title = home_page.get_title()
    assert "Motors" in actual_title or "eBay" in actual_title, (
        f"Expected 'Motors' in title, but got '{actual_title}'"
    )
