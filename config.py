"""Centralized configuration module for test environment and timeouts."""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    """Framework configuration settings with environment variable overrides."""

    base_url: str = os.getenv("EBAY_BASE_URL", "https://www.ebay.com")
    default_timeout: float = float(os.getenv("SELENIUM_TIMEOUT", "10.0"))
    page_load_timeout: float = float(os.getenv("SELENIUM_PAGE_LOAD_TIMEOUT", "30.0"))
    script_timeout: float = float(os.getenv("SELENIUM_SCRIPT_TIMEOUT", "30.0"))
    default_browser: str = os.getenv("SELENIUM_BROWSER", "chrome")
    default_headless: bool = os.getenv("SELENIUM_HEADLESS", "false").lower() in (
        "true",
        "1",
        "yes",
    )


settings = Settings()
