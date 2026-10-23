"""
Author: Alexander Paceskoski

Product detail page, e.g. iPhone: route=product/product&product_id=40
"""

from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from pages.base_page import BasePage, Locator

# The iPhone used by the cart tests (product 40 on the old LambdaTest
# playground and on the current demo alike).
IPHONE_PRODUCT_ID: int = 40


class ProductPage(BasePage):
    ADD_TO_CART: Locator = (By.ID, "button-cart")
    # Stock OpenCart confirms the add with a green banner above the content.
    SUCCESS_BANNER: Locator = (By.CSS_SELECTOR, ".alert-success")

    def open(self, route: str = f"product/product&product_id={IPHONE_PRODUCT_ID}") -> Self:
        super().open(route)
        return self

    def add_to_cart(self) -> Self:
        self.click(self.ADD_TO_CART)
        self.wait.until(ec.visibility_of_element_located(self.SUCCESS_BANNER))
        return self

    def toast_text(self) -> str:
        """
        Text of the add-to-cart success banner, e.g.
        'Success: You have added iPhone to your shopping cart!'.
        """
        texts = [t.text for t in self.driver.find_elements(*self.SUCCESS_BANNER) if t.text.strip()]
        return "\n".join(texts).strip()
