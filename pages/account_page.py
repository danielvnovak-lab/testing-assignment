"""
Author: Karim Elkholy

My Account dashboard: https://ecommerce-playground.lambdatest.io/index.php?route=account/account
"""

from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from pages.base_page import BasePage, Locator


class AccountPage(BasePage):
    CONTENT: Locator = (By.ID, "content")

    def open(self, route: str = "account/account") -> Self:
        super().open(route)
        return self

    def is_loaded(self) -> bool:
        """
        True once the My Account dashboard is visible for the logged-in user.
        """
        try:
            self.wait.until(ec.url_contains("route=account/account"))
            self.wait.until(lambda d: "my account" in self.find(self.CONTENT).text.lower())
            return True
        except Exception:
            return False
