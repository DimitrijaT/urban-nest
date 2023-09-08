# from django.urls import reverse
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from functional_tests.template_classes.abstract_page import AbstractPage


class AdListPage(AbstractPage):

    def choose_advertised_furniture(self):
        furniture_div = self.browser.find_element(By.ID, 'furniture_container')
        furniture_div.find_elements(By.TAG_NAME, 'a')[0].click()
