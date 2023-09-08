import time
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from functional_tests.template_classes.abstract_page import AbstractPage


class ShoppingCartPage(AbstractPage):

    def open_shopping_cart_page(self):
        shopping_cart_button = self.browser.find_element(By.ID, 'open_shopping_cart')
        shopping_cart_button.click()

    def checkout_cart(self):
        # scroll to find the button
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        wait = WebDriverWait(self.browser, 10)
        checkout_button = wait.until(EC.element_to_be_clickable((By.ID, 'checkout_cart_items')))
        checkout_button.click()
