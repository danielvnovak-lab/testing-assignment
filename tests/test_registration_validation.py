"""
Author: Karim Elkholy

T002 - User Registration (F2) - all 4 scenarios.

Function IDs/Names: F2 User Registration
Tester: Karim Elkholy

Scenario 1: successful registration with a unique email.
Scenario 2: registering an email that is already in use is rejected.
Scenario 3: mismatched password confirmation is rejected.
Scenario 4: submitting with all required fields empty shows per-field
            validation errors.
"""
import uuid
from collections.abc import Callable
from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from pages.register_page import RegisterPage

TEST_PASSWORD = "S3cure!Pass2026"


def test_scenario_1_successful_registration(
    driver: WebDriver,
    base_url: str,
    snap: Callable[[str], Path],
) -> None:
    register = RegisterPage(driver, base_url).open()
    email = f"t002.{uuid.uuid4().hex[:8]}@example.com"
    register.register("John", "Doe", email, "+61400000000", TEST_PASSWORD)
    snap("01_registration_success")

    assert register.is_successful(), "expected the account-created success message"


def test_scenario_2_email_already_registered_rejected(
    driver: WebDriver,
    base_url: str,
    snap: Callable[[str], Path],
) -> None:
    email = f"t002.{uuid.uuid4().hex[:8]}@example.com"

    # First registration creates the account; log out afterwards.
    RegisterPage(driver, base_url).open().register(
        "John", "Doe", email, "+61400000000", TEST_PASSWORD
    )
    BasePage(driver, base_url).logout()

    # Try to register the same email again.
    second = RegisterPage(driver, base_url).open()
    second.fill("John", "Doe", email, "+61400000000", TEST_PASSWORD)
    second.submit()
    warning: str = second.warning_text()
    snap("01_email_already_registered_warning")

    assert "already registered" in warning.lower(), (
        f"expected 'already registered' warning, got: {warning!r}"
    )
    assert "account/register" in driver.current_url, "should stay on the registration page"


def test_scenario_3_passwords_do_not_match_rejected(
    driver: WebDriver,
    base_url: str,
    snap: Callable[[str], Path],
) -> None:
    register = RegisterPage(driver, base_url).open()
    register.fill(
        first_name="John",
        last_name="Doe",
        email=f"t002.{uuid.uuid4().hex[:8]}@example.com",
        telephone="+61400000000",
        password="S3cure!Pass2026",
        password_confirm="Different!123",
    )
    register.submit()
    errors: list[str] = register.wait_for_field_errors()
    snap("01_password_mismatch_error")

    assert "Password confirmation does not match password!" in errors, (
        f"expected mismatch error, got: {errors!r}"
    )
    assert "account/register" in driver.current_url, "should stay on the registration page"


def test_scenario_4_empty_required_fields_show_errors(
    driver: WebDriver,
    base_url: str,
    snap: Callable[[str], Path],
) -> None:
    register = RegisterPage(driver, base_url).open()
    register.submit()  # everything left empty
    errors: list[str] = register.wait_for_field_errors()
    snap("01_empty_fields_validation_errors")

    for expected in (
        "First Name must be between 1 and 32 characters!",
        "Last Name must be between 1 and 32 characters!",
        "E-Mail Address does not appear to be valid!",
        "Telephone must be between 3 and 32 characters!",
        "Password must be between 4 and 20 characters!",
    ):
        assert expected in errors, f"missing validation error {expected!r} in {errors!r}"
    assert "account/register" in driver.current_url, "should stay on the registration page"
