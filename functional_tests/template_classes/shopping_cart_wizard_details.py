import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from functional_tests.template_classes.abstract_page import AbstractPage


class OrderDetailsPage(AbstractPage):

    def order_products(self):
        wait = WebDriverWait(self.browser, 10)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        pay_now_button = wait.until(EC.presence_of_element_located((By.ID, 'pay_now_button')))
        pay_now_button.click()

    def assert_order_is_created(self):
        wait = WebDriverWait(self.browser, 10)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        order_created = wait.until(EC.presence_of_element_located((By.ID, 'payment_confirmed_screen')))
        assert order_created.text == 'Payment Confirmed'
