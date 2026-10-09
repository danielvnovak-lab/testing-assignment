"""
Author: Karim Elkholy

Login page: https://ecommerce-playground.lambdatest.io/index.php?route=account/login
"""

from typing import Self

from selenium.webdriver.common.by import By

from pages.base_page import BasePage, Locator


class LoginPage(BasePage):
    EMAIL: Locator = (By.ID, "input-email")
    PASSWORD: Locator = (By.ID, "input-password")
    SUBMIT: Locator = (By.CSS_SELECTOR, "input[type=submit][value=Login]")
    FORGOTTEN_LINK: Locator = (By.CSS_SELECTOR, 'a[href*="account/forgotten"]')
    # The page carries a decorative .alert-info banner; the login warning is
    # the .alert-danger / .alert-warning element.
    ALERT: Locator = (By.CSS_SELECTOR, ".alert-danger, .alert-warning")

    def open(self, route: str = "account/login") -> Self:
        super().open(route)
        return self

    def login(self, email: str, password: str) -> Self:
        self.type(self.EMAIL, email)
        self.type(self.PASSWORD, password)
        self.click(self.SUBMIT)
        return self

    def warning_text(self) -> str:
        """
        Text of the warning banner shown after a failed login.
        """
        return self.find(self.ALERT).text.strip()

    def rejected_warning(self) -> bool:
        """
        True when the login was rejected.

        Accepts both site responses: the 'No match' warning and the
        'account has exceeded allowed number of login attempts' warning
        (the site rate-limits failed logins per IP).
        """
        warning = self.warning_text().lower()
        return "no match" in warning or "exceeded allowed number of login attempts" in warning

    def forgotten_password_link_text(self) -> str:
        return self.find(self.FORGOTTEN_LINK).text.strip()
