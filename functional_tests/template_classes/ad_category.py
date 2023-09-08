# from django.urls import reverse
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from functional_tests.template_classes.abstract_page import AbstractPage


class CategoryPage(AbstractPage):

    def open_ad_category_page(self):
        wait = WebDriverWait(self.browser, 10)
        button = wait.until(EC.element_to_be_clickable((By.ID, 'open_furniture_category_list')))
        button.click()

    def choose_category(self):
        category_div = self.browser.find_element(By.ID, 'categories_container')
        category_div.find_elements(By.TAG_NAME, 'a')[0].click()
