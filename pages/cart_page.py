"""
Author: Alexander Paceskoski

Shopping cart page: https://ecommerce-playground.lambdatest.io/index.php?route=checkout/cart
"""

from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from pages.base_page import BasePage, Locator

EMPTY_MESSAGE: str = "Your shopping cart is empty!"


class CartPage(BasePage):
    QUANTITY_INPUT: Locator = (By.CSS_SELECTOR, 'input[name^="quantity"]')
    # Bootstrap tooltips move title= to data-original-title= after hover.
    UPDATE_BUTTON: Locator = (
        By.CSS_SELECTOR,
        'button[data-original-title="Update"], button[title="Update"]',
    )
    REMOVE_BUTTON: Locator = (
        By.CSS_SELECTOR,
        'button[data-original-title="Remove"], button[title="Remove"]',
    )

    def open(self, route: str = "checkout/cart") -> Self:
        super().open(route)
        return self

    def set_quantity(self, quantity: int) -> Self:
        field = self.find(self.QUANTITY_INPUT)
        field.clear()
        field.send_keys(str(quantity))
        return self

    def update(self) -> Self:
        self.click(self.UPDATE_BUTTON)
        # The cart table is re-rendered (reload or AJAX); wait for the
        # quantity field to be back and usable.
        self.wait.until(ec.element_to_be_clickable(self.QUANTITY_INPUT))
        return self

    def remove_item(self) -> Self:
        self.click(self.REMOVE_BUTTON)
        self.wait.until(lambda d: self.contains_text(EMPTY_MESSAGE))
        return self

    def totals_text(self) -> str:
        """
        Text of the cart totals table (Sub-Total / Eco Tax / VAT / Total).
        """
        tables = self.find_all((By.CSS_SELECTOR, "table"))
        for table in tables:
            if "total" in table.text.lower():
                return table.text
        return ""

    def totals_contain(self, amount: str) -> bool:
        """
        Wait until the totals table shows `amount` (after add/update).
        """
        self.wait.until(lambda d: amount in self.totals_text())
        return True

    def is_empty(self) -> bool:
        return self.contains_text(EMPTY_MESSAGE)
