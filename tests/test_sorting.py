"""
Author: Alexander Paceskoski
Tester: Alexander Paceskoski

T006 - Product Sorting (F6) - all 3 scenarios.

Function IDs/Names: F6 Product Sorting
(Sort By dropdown on the Desktops category page:
 https://opencart.abstracta.us/index.php?route=product/category&path=20)

Scenario 1: sorting in alphabetical order (Name A - Z).
Scenario 2: sorting in ascending price order (Price Low > High).
Scenario 3: sorting in descending price order (Price High > Low).
"""
from collections.abc import Callable
from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver

from pages.category_page import CategoryPage

ALPHABETICAL = "Name (A - Z)"
PRICE_ASC = "Price (Low > High)"
PRICE_DESC = "Price (High > Low)"


def test_scenario_1_sort_alphabetical_order(
    driver: WebDriver, base_url: str, snap: Callable[[str], Path]
) -> None:
    page = CategoryPage(driver, base_url).open()
    page.sort_by(ALPHABETICAL)
    titles: list[str] = page.titles()
    snap("01_sorted_alphabetically")

    assert len(titles) >= 5, f"expected a full product list, got {len(titles)}"
    assert titles == sorted(titles, key=str.lower), (
        f"products should be in alphabetical order, got: {titles}"
    )


def test_scenario_2_sort_price_ascending(
    driver: WebDriver, base_url: str, snap: Callable[[str], Path]
) -> None:
    page = CategoryPage(driver, base_url).open()
    page.sort_by(PRICE_ASC)
    prices: list[float] = page.prices()
    snap("01_sorted_price_ascending")

    assert len(prices) >= 5, f"expected a full product list, got {len(prices)}"
    assert prices == sorted(prices), f"prices should be ascending, got: {prices}"


def test_scenario_3_sort_price_descending(
    driver: WebDriver, base_url: str, snap: Callable[[str], Path]
) -> None:
    page = CategoryPage(driver, base_url).open()
    page.sort_by(PRICE_DESC)
    prices: list[float] = page.prices()
    snap("01_sorted_price_descending")

    assert len(prices) >= 5, f"expected a full product list, got {len(prices)}"
    assert prices == sorted(prices, reverse=True), f"prices should be descending, got: {prices}"
