"""
Author: Alexander Paceskoski

Category page with product sorting: route=product/category&path=20 (Desktops).
"""

import re
from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage, Locator

# The Desktops category holds 12 varied products - ideal for sorting checks.
# (Sorting used to run on Cameras on the previous playground, but that
# category holds only 2 products on the current demo.)
DESKTOPS_ROUTE = "product/category&path=20"


class CategoryPage(BasePage):
    SORT_DROPDOWN: Locator = (By.ID, "input-sort")
    PRODUCT_TITLES: Locator = (By.CSS_SELECTOR, ".product-thumb h4 a")
    PRODUCT_PRICES: Locator = (By.CSS_SELECTOR, ".product-thumb .price")

    def open(self, route: str = DESKTOPS_ROUTE) -> Self:
        super().open(route)
        return self

    def sort_by(self, option_text: str) -> Self:
        """
        Pick an option in the Sort By dropdown and wait for the reload.
        """
        select = Select(self.find(self.SORT_DROPDOWN))
        select.select_by_visible_text(option_text)
        self.wait.until(lambda d: "sort=" in d.current_url)
        self.wait.until(ec.element_to_be_clickable(self.SORT_DROPDOWN))
        return self

    def titles(self) -> list[str]:
        return [el.text.strip() for el in self.find_all(self.PRODUCT_TITLES) if el.text.strip()]

    def prices(self) -> list[float]:
        """
        The displayed price of each product, e.g. 146.0 for '$146.00'.

        Products on special render the current price first (price-new) and
        the struck-through old price after it, so the first match is the
        price OpenCart sorts by.
        """
        prices: list[float] = []
        for el in self.find_all(self.PRODUCT_PRICES):
            match = re.search(r"\$([\d,.]+)", el.text)
            if match:
                prices.append(float(match.group(1).replace(",", "")))
        return prices
