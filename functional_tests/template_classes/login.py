from django.urls import reverse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from functional_tests.template_classes.abstract_page import AbstractPage


class LoginPage(AbstractPage):

    def navigate_to_login_page(self):
        self.browser.get(self.live_server_url)
        wait = WebDriverWait(self.browser, 10)
        login_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Please log in.')))
        login_button.click()
        time.sleep(2)

    def assert_login_page_url(self):
        login_page_url = self.live_server_url + reverse('login')
        assert self.browser.current_url == login_page_url, "Not on the login page"

    def login(self, username, password):
        wait = WebDriverWait(self.browser, 10)
        username_input = wait.until(EC.element_to_be_clickable((By.ID, 'id_username')))
        username_input.send_keys(username)
        password_input = wait.until(EC.element_to_be_clickable((By.ID, 'id_password')))
        password_input.send_keys(password)
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']")))
        login_button.click()
        time.sleep(2)

    def assert_index_page_url(self):
        index_page_url = self.live_server_url + reverse('index')
        # print(self.browser.current_url)
        # print(index_page_url)
        assert self.browser.current_url == index_page_url, "Not on the index page"
