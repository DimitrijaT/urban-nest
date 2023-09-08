# from django.urls import reverse
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from functional_tests.template_classes.abstract_page import AbstractPage


class DashboardHomePage(AbstractPage):

    def open_dashboard_home_page(self):
        self.browser.get(self.live_server_url)
        wait = WebDriverWait(self.browser, 10)
        dashboard_button = wait.until(EC.element_to_be_clickable((By.ID, 'open_dashboard_button')))
        dashboard_button.click()

    def open_sell_furniture_ad_page(self):
        wait = WebDriverWait(self.browser, 10)
        sell_button = wait.until(EC.element_to_be_clickable((By.ID, 'sell_furniture')))
        sell_button.click()

    def assert_product_is_up_for_sale(self):
        wait = WebDriverWait(self.browser, 10)
        furniture_ad_div = wait.until(EC.element_to_be_clickable((By.ID, 'furniture_ad_tbody')))
        # check if it has a child div (tr)
        assert furniture_ad_div.find_element(By.TAG_NAME, 'tr')
