"""
Author: Alexander Paceskoski

Contact Us page: https://opencart.abstracta.us/index.php?route=information/contact
"""

from typing import Self

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ContactPage(BasePage):
    NAME = (By.ID, "input-name")
    EMAIL = (By.ID, "input-email")
    ENQUIRY = (By.ID, "input-enquiry")
    SUBMIT = (By.CSS_SELECTOR, "input[type=submit][value=Submit]")
    FEEDBACK = (By.CSS_SELECTOR, ".text-danger")

    def open(self, route: str = "information/contact") -> Self:
        super().open(route)
        return self

    def fill(self, name: str = "", email: str = "", enquiry: str = "") -> Self:
        if name:
            self.type(self.NAME, name)
        if email:
            self.type(self.EMAIL, email)
        if enquiry:
            self.type(self.ENQUIRY, enquiry)
        return self

    def submit(self) -> Self:
        self.click(self.SUBMIT)
        return self

    def wait_for_success(self) -> None:
        """
        The valid-submission flow ends on a dedicated success page.
        """
        self.wait.until(lambda d: "information/contact/success" in d.current_url)

    def wait_for_feedback(self) -> list[str]:
        """
        Wait for the inline validation messages to render, then return them.
        """
        self.wait.until(lambda d: self.find_all(self.FEEDBACK))
        return self.feedback_messages()

    def feedback_messages(self) -> list[str]:
        return [
            el.text.strip()
            for el in self.find_all(self.FEEDBACK)
            if el.text.strip()
        ]
