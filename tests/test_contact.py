"""
Author: Alexander Paceskoski
Tester: Alexander Paceskoski

T005 - Contact Us (F5) - all 3 scenarios.

Function IDs/Names: F5 Contact Us
(https://ecommerce-playground.lambdatest.io/index.php?route=information/contact)

Scenario 1: submitting the contact form with valid data succeeds.
Scenario 2: submitting with an invalid email address shows a validation error.
Scenario 3: submitting with the enquiry box left empty shows a validation error.
"""
from collections.abc import Callable
from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver

from pages.contact_page import ContactPage

ENQUIRY_TEXT = "Hello, I would like to ask about product availability."


def test_scenario_1_valid_enquiry_is_accepted(
    driver: WebDriver, base_url: str, snap: Callable[[str], Path]
) -> None:
    contact = ContactPage(driver, base_url).open()
    contact.fill(name="John Doe", email="john.doe@example.com", enquiry=ENQUIRY_TEXT)
    contact.submit()
    contact.wait_for_success()
    snap("01_enquiry_sent")

    assert "information/contact/success" in driver.current_url, (
        "valid enquiry should land on the contact success page"
    )


def test_scenario_2_invalid_email_shows_error(
    driver: WebDriver, base_url: str, snap: Callable[[str], Path]
) -> None:
    contact = ContactPage(driver, base_url).open()
    contact.fill(name="John Doe", email="not-an-email", enquiry=ENQUIRY_TEXT)
    contact.submit()
    feedback: list[str] = contact.wait_for_feedback()
    snap("01_invalid_email_error")

    assert "E-Mail Address does not appear to be valid!" in feedback, (
        f"expected invalid-email error, got: {feedback!r}"
    )
    assert "information/contact" in driver.current_url, "should stay on the contact page"


def test_scenario_3_empty_enquiry_shows_error(
    driver: WebDriver, base_url: str, snap: Callable[[str], Path]
) -> None:
    contact = ContactPage(driver, base_url).open()
    contact.fill(name="John Doe", email="john.doe@example.com")  # enquiry left empty
    contact.submit()
    feedback: list[str] = contact.wait_for_feedback()
    snap("01_empty_enquiry_error")

    assert "Enquiry must be between 10 and 3000 characters!" in feedback, (
        f"expected empty-enquiry error, got: {feedback!r}"
    )
    assert "information/contact" in driver.current_url, "should stay on the contact page"
