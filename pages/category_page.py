"""
Author: Alexander Paceskoski

Category page with product sorting: route=product/category&path=33 (Cameras).
"""

import re
from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage, Locator

# The Cameras category holds 15 varied products - ideal for sorting checks.
CAMERAS_ROUTE = "product/category&path=33"


class CategoryPage(BasePage):
    SORT_DROPDOWN: Locator = (By.CSS_SELECTOR, "select[id^='input-sort']")
    PRODUCT_TITLES: Locator = (By.CSS_SELECTOR, ".product-thumb a.text-ellipsis-2")
    PRODUCT_PRICES: Locator = (By.CSS_SELECTOR, ".product-thumb .price")

    def open(self, route: str = CAMERAS_ROUTE) -> Self:
        super().open(route)
        return self

    def _visible_sort_select(self) -> Select:
        for element in self.find_all(self.SORT_DROPDOWN):
            if element.is_displayed():
                return Select(element)
        raise AssertionError("no visible Sort By dropdown found")

    def sort_by(self, option_text: str) -> Self:
        """
        Pick an option in the Sort By dropdown and wait for the reload.
        """
        select = self._visible_sort_select()
        select.select_by_visible_text(option_text)
        self.wait.until(lambda d: "sort=" in d.current_url)
        self.wait.until(ec.element_to_be_clickable(self.SORT_DROPDOWN))
        return self

    def titles(self) -> list[str]:
        return [el.text.strip() for el in self.find_all(self.PRODUCT_TITLES) if el.text.strip()]

    def prices(self) -> list[float]:
        """
        The displayed price of each product, e.g. 146.0 for '$146.00'.
        """
        prices: list[float] = []
        for el in self.find_all(self.PRODUCT_PRICES):
            match = re.search(r"\$([\d,.]+)", el.text)
            if match:
                prices.append(float(match.group(1).replace(",", "")))
        return prices
