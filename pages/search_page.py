"""
Author: Karim Elkholy

Product search via the header search bar (route=product/search).
"""

from typing import Self

from selenium.webdriver.common.by import By

from pages.base_page import BasePage, Locator

RESULT_CARDS: Locator = (By.CSS_SELECTOR, ".product-thumb")


class SearchPage(BasePage):
    SEARCH_INPUT: Locator = (By.CSS_SELECTOR, "#search input[name='search']")
    SEARCH_BUTTON: Locator = (By.CSS_SELECTOR, "#search button[type='button']")
    RESULT_TITLES: Locator = (By.CSS_SELECTOR, "#content .product-thumb h4 a")
    # Scoped to #content: the header logo is also an <h1> in the stock theme.
    PAGE_TITLE: Locator = (By.CSS_SELECTOR, "#content h1")

    def open(self, route: str = "common/home") -> Self:
        super().open(route)
        return self

    def search(self, term: str) -> Self:
        """
        Type a keyword into the header search bar and submit.
        """
        self.type(self.SEARCH_INPUT, term)
        self.click(self.SEARCH_BUTTON)
        self.wait.until(lambda d: f"search - {term.lower()}" in self.find(self.PAGE_TITLE).text.lower())
        return self

    def result_titles(self) -> list[str]:
        return [el.text.strip() for el in self.find_all(self.RESULT_TITLES) if el.text.strip()]

    def has_no_results(self) -> bool:
        """
        True when the results page renders zero product cards.

        Older OpenCart builds showed 'There is no product that matches the
        search criteria.' here; the current demo renders no message, so the
        absence of result cards is the observable outcome.
        """
        return not self.driver.find_elements(*RESULT_CARDS)
