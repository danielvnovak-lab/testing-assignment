"""
Author: Alexander Paceskoski

T004 - Shopping Cart (F4).

Function IDs/Names: F4 Shopping Cart
Tester: Alexander Paceskoski

Scenario 1: adding a product updates the toast, header badge and totals.
Scenario 2: changing the quantity recalculates the totals.
Scenario 3: removing the item empties the cart.

Product under test: iPhone (product_id=40, $123.20 each incl. tax).
Each scenario is self-contained: it adds the product itself first.
"""
from collections.abc import Callable
from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver

from pages.cart_page import CartPage
from pages.product_page import ProductPage

UNIT_TOTAL: str = "$123.20"
TWO_UNITS_TOTAL: str = "$246.40"


def _add_iphone(driver: WebDriver, base_url: str) -> ProductPage:
    return ProductPage(driver, base_url).open().add_to_cart()


def test_scenario_1_add_to_cart_updates_badge_and_totals(
    driver: WebDriver, base_url: str, snap: Callable[[str], Path]
) -> None:
    product = _add_iphone(driver, base_url)
    snap("01_success_toast")

    toast: str = " ".join(product.toast_text().split())
    assert "success: you have added iphone to your shopping cart" in toast.lower()
    assert product.cart_badge_count() == "1", f"badge should show 1, got {product.cart_badge_count()!r}"

    cart = CartPage(driver, base_url).open()
    snap("02_cart_page_with_item")

    assert "iphone" in cart.totals_text().lower()
    assert cart.totals_contain(UNIT_TOTAL), f"expected total {UNIT_TOTAL} in cart"


def test_scenario_2_quantity_update_recalculates_total(
    driver: WebDriver, base_url: str, snap: Callable[[str], Path]
) -> None:
    _add_iphone(driver, base_url)
    cart = CartPage(driver, base_url).open()

    cart.set_quantity(2)
    snap("01_quantity_set_to_2")
    cart.update()
    snap("02_totals_updated")

    assert cart.totals_contain(TWO_UNITS_TOTAL), (
        f"expected total {TWO_UNITS_TOTAL}, got: {cart.totals_text()!r}"
    )


def test_scenario_3_remove_item_empties_cart(
    driver: WebDriver, base_url: str, snap: Callable[[str], Path]
) -> None:
    _add_iphone(driver, base_url)
    cart = CartPage(driver, base_url).open()
    assert not cart.is_empty(), "cart should contain the added item before removal"

    cart.remove_item()
    snap("01_cart_emptied")

    assert cart.is_empty(), "expected 'Your shopping cart is empty!' after removal"
