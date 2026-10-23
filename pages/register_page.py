"""
Author: Karim Elkholy

Registration page: https://opencart.abstracta.us/index.php?route=account/register
"""
from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.base_page import BasePage, Locator

# This demo's success page reads 'Congratulations! Your new account has been
# successfully created!' (older OpenCart builds said 'Your Account Has Been
# Created!').
SUCCESS_MESSAGE: str = "Your new account has been successfully created!"


class RegisterPage(BasePage):
    FIRST_NAME: Locator = (By.ID, "input-firstname")
    LAST_NAME: Locator = (By.ID, "input-lastname")
    EMAIL: Locator = (By.ID, "input-email")
    TELEPHONE: Locator = (By.ID, "input-telephone")
    PASSWORD: Locator = (By.ID, "input-password")
    PASSWORD_CONFIRM: Locator = (By.ID, "input-confirm")
    # The agree checkbox is a plain input in the stock theme (no id, no
    # matching label), so click the checkbox itself.
    AGREE_CHECKBOX: Locator = (By.CSS_SELECTOR, 'input[name="agree"]')
    CONTINUE: Locator = (By.CSS_SELECTOR, "input[type=submit][value=Continue]")
    # The rejected-registration warning banner (e.g. duplicate email).
    ALERT: Locator = (By.CSS_SELECTOR, ".alert-danger")
    FIELD_ERRORS = (By.CSS_SELECTOR, ".text-danger")

    def open(self, route: str = "account/register") -> Self:
        super().open(route)
        return self

    def fill(
        self,
        first_name: str = "",
        last_name: str = "",
        email: str = "",
        telephone: str = "",
        password: str = "",
        password_confirm: str | None = None,
    ) -> Self:
        """
        Fill only the given fields, leaving the rest empty for validation tests.
        """
        if password_confirm is None:
            password_confirm = password
        values: list[tuple[Locator, str]] = [
            (self.FIRST_NAME, first_name),
            (self.LAST_NAME, last_name),
            (self.EMAIL, email),
            (self.TELEPHONE, telephone),
            (self.PASSWORD, password),
            (self.PASSWORD_CONFIRM, password_confirm),
        ]
        for locator, value in values:
            if value:
                self.type(locator, value)
        return self

    def submit(self) -> Self:
        """
        Agree to the privacy policy and click Continue (no success waiting).
        """
        self.click(self.AGREE_CHECKBOX)
        self.click(self.CONTINUE)
        return self

    def warning_text(self) -> str:
        """
        Text of the warning banner shown after a rejected registration.
        """
        return self.find(self.ALERT).text.strip()

    def register(
        self,
        first_name: str,
        last_name: str,
        email: str,
        telephone: str,
        password: str,
    ) -> Self:
        """
        Fill the registration form, agree to the privacy policy and submit.
        """
        self.fill(first_name, last_name, email, telephone, password)
        self.submit()
        self.wait.until(lambda d: self.contains_text(SUCCESS_MESSAGE))
        return self

    def is_successful(self) -> bool:
        return self.contains_text(SUCCESS_MESSAGE)

    def field_errors(self) -> list[str]:
        """
        Per-field validation errors shown after a rejected registration.
        """
        return [
            el.text.strip()
            for el in self.find_all(self.FIELD_ERRORS)
            if el.text.strip()
        ]

    def wait_for_field_errors(self) -> list[str]:
        """
        Wait for the per-field validation errors to render, then return them.
        """
        self.wait.until(lambda d: self.field_errors())
        return self.field_errors()

    def email_validation_message(self) -> str:
        """
        The browser's HTML5 validation tooltip text for the E-Mail field.
        """
        email: WebElement = self.driver.find_element(*self.EMAIL)
        return email.get_attribute("validationMessage") or ""
