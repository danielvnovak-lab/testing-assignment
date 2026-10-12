"""
Author: Alexander Paceskoski

Product detail page, e.g. iPhone: route=product/product&product_id=40
"""

from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from pages.base_page import BasePage, Locator

# The iPhone used by the cart tests (verified to exist on the playground).
IPHONE_PRODUCT_ID: int = 40


class ProductPage(BasePage):
    ADD_TO_CART: Locator = (By.CSS_SELECTOR, "button.btn-cart.btn-block")
    TOAST: Locator = (By.CSS_SELECTOR, ".toast")

    def open(self, route: str = f"product/product&product_id={IPHONE_PRODUCT_ID}") -> Self:
        super().open(route)
        return self

    def add_to_cart(self) -> Self:
        # The page renders this button twice (one hidden duplicate for the
        # sticky header), so click the first one that is actually displayed.
        self.wait.until(
            lambda d: any(b.is_displayed() for b in d.find_elements(*self.ADD_TO_CART))
        )
        for button in self.driver.find_elements(*self.ADD_TO_CART):
            if button.is_displayed():
                button.click()
                break
        self.wait.until(ec.visibility_of_element_located(self.TOAST))
        return self

    def toast_text(self) -> str:
        """
        Text of the notification toast, e.g.
        'Success: You have added iPhone to your shopping cart!'.
        """
        texts = [t.text for t in self.driver.find_elements(*self.TOAST) if t.text.strip()]
        return "\n".join(texts).strip()
