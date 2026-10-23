"""
Author: Karim Elkholy

T003 - Product Search (F3) - all 3 scenarios.

Function IDs/Names: F3 Product Search
Tester: Karim Elkholy

Scenario 1: search using an exact product name ('iPhone').
Scenario 2: search using a partial keyword ('Mac').
Scenario 3: search for a non-existent product ('hi12345abc').
"""
from collections.abc import Callable
from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver

from pages.search_page import SearchPage

TEST_ID = "T003"

EXACT_KEYWORD = "iPhone"
PARTIAL_KEYWORD = "Mac"
NONEXISTENT_KEYWORD = "hi12345abc"


def test_scenario_1_search_exact_product_name(
    driver: WebDriver, base_url: str, snap: Callable[[str], Path]
) -> None:
    search = SearchPage(driver, base_url).open().search(EXACT_KEYWORD)
    snap("t003_scenario_1")

    titles: list[str] = search.result_titles()
    assert titles, f"expected results for {EXACT_KEYWORD!r}, got none"
    assert all(EXACT_KEYWORD.lower() in t.lower() for t in titles), f"unexpected results: {titles}"


def test_scenario_2_search_partial_keyword(
    driver: WebDriver, base_url: str, snap: Callable[[str], Path]
) -> None:
    search = SearchPage(driver, base_url).open().search(PARTIAL_KEYWORD)
    snap("t003_scenario_2")

    titles: list[str] = search.result_titles()
    assert titles, f"expected results for partial keyword {PARTIAL_KEYWORD!r}"
    assert all(PARTIAL_KEYWORD.lower() in t.lower() for t in titles), (
        f"partial keyword should match products containing 'Mac', got: {titles}"
    )


def test_scenario_3_search_nonexistent_product(
    driver: WebDriver, base_url: str, snap: Callable[[str], Path]
) -> None:
    search = SearchPage(driver, base_url).open().search(NONEXISTENT_KEYWORD)
    snap("t003_scenario_3")

    assert search.has_no_results(), (
        "a non-existent product must not render any result cards"
    )
    assert search.result_titles() == [], "a non-existent product must not return results"
