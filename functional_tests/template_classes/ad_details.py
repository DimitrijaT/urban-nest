# from django.urls import reverse
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from functional_tests.template_classes.abstract_page import AbstractPage


class AdDetailedPage(AbstractPage):

    def add_product_to_cart(self):
        wait = WebDriverWait(self.browser, 10)
        add_to_cart_button = wait.until(EC.presence_of_element_located((By.ID, 'add_to_cart_button')))
        self.browser.execute_script("arguments[0].scrollIntoView();", add_to_cart_button)
        time.sleep(1)
        add_to_cart_button.click()
