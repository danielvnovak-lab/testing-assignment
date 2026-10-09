"""
Author: Karim Elkholy

Product search via the header search bar (route=product/search).
"""

from typing import Self

from selenium.webdriver.common.by import By

from pages.base_page import BasePage, Locator

NO_RESULTS_MESSAGE: str = "There is no product that matches the search criteria."


class SearchPage(BasePage):
    SEARCH_INPUT: Locator = (By.CSS_SELECTOR, "input[name=search]")
    SEARCH_BUTTON: Locator = (By.CSS_SELECTOR, "button.type-text")
    RESULT_TITLES: Locator = (By.CSS_SELECTOR, ".product-thumb a.text-ellipsis-2")
    PAGE_TITLE: Locator = (By.CSS_SELECTOR, "h1")

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

    def has_no_results_message(self) -> bool:
        return self.contains_text(NO_RESULTS_MESSAGE)
