"""
Author: Karim Elkholy

T001 - User Login (F1) - all 5 scenarios.

Function IDs/Names: F1 User Login
Tester: Karim Elkholy

Scenario 1: successful login with the registered test account.
Scenario 2: unregistered email is rejected.
Scenario 3: empty login fields are rejected.
Scenario 4: wrong password for a registered account is rejected.
Scenario 5: the session persists across navigation.

Uses the account registered once per session by the `registered_user`
fixture (registration before login, F2 -> F1).
"""
import uuid
from collections.abc import Callable
from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver

from pages.account_page import AccountPage
from pages.base_page import BasePage
from pages.login_page import LoginPage


def test_scenario_1_successful_login(
    driver: WebDriver,
    base_url: str,
    snap: Callable[[str], Path],
    registered_user: dict[str, str],
) -> None:
    login = LoginPage(driver, base_url).open()
    login.login(registered_user["email"], registered_user["password"])
    snap("01_my_account_page")

    assert AccountPage(driver, base_url).is_loaded(), (
        "registered user should land on the My Account page"
    )


def test_scenario_2_unregistered_email_rejected(
    driver: WebDriver,
    base_url: str,
    snap: Callable[[str], Path],
    registered_user: dict[str, str],
) -> None:
    ghost_email = f"ghost.{uuid.uuid4().hex[:8]}@example.com"

    login = LoginPage(driver, base_url).open()
    login.login(ghost_email, registered_user["password"])
    warning: str = login.warning_text()  # waits for the warning banner to render
    snap("01_unregistered_email_warning")

    assert login.rejected_warning(), f"expected a rejection warning, got: {warning!r}"
    assert "account/login" in driver.current_url, "should stay on the login page"


def test_scenario_3_empty_login_fields_rejected(
    driver: WebDriver,
    base_url: str,
    snap: Callable[[str], Path],
) -> None:
    login = LoginPage(driver, base_url).open()
    login.login("", "")  # leave both fields empty and submit
    warning: str = login.warning_text()
    snap("01_empty_fields_warning")

    assert login.rejected_warning(), f"expected a rejection warning, got: {warning!r}"
    assert "account/login" in driver.current_url, "should stay on the login page"


def test_scenario_4_wrong_password_rejected(
    driver: WebDriver,
    base_url: str,
    snap: Callable[[str], Path],
    registered_user: dict[str, str],
) -> None:
    login = LoginPage(driver, base_url).open()
    login.login(registered_user["email"], "WrongPassword!999")
    warning: str = login.warning_text()  # waits for the warning banner to render
    snap("01_wrong_password_warning")

    assert login.rejected_warning(), f"expected a rejection warning, got: {warning!r}"
    assert "account/login" in driver.current_url, "should stay on the login page"


def test_scenario_5_session_persists_across_navigation(
    driver: WebDriver,
    base_url: str,
    snap: Callable[[str], Path],
    registered_user: dict[str, str],
) -> None:
    login = LoginPage(driver, base_url).open()
    login.login(registered_user["email"], registered_user["password"])
    assert AccountPage(driver, base_url).is_loaded(), "login should land on My Account"

    # Navigate away to the home page; the header must still show the
    # logged-in menu (Logout available, no Login/Register).
    base = BasePage(driver, base_url).open("common/home")
    base.open_my_account_menu(base.MENU_LOGOUT)
    snap("01_home_still_logged_in")

    # Return directly to the account route; no credentials required again.
    account = AccountPage(driver, base_url).open()
    snap("02_my_account_without_relogin")
    assert account.is_loaded(), "session should persist across navigation"
