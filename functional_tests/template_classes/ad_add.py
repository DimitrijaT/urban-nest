from functional_tests.template_classes.abstract_page import AbstractPage
# from django.urls import reverse
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class PostAdPage(AbstractPage):

    def sell_product(self, data):
        time.sleep(5)
        wait = WebDriverWait(self.browser, 10)

        wait.until(EC.presence_of_element_located((By.ID, 'id_name'))).send_keys(data['name'])

        desired_category = data['category']
        category_option = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                     f'//select[@id="id_category"]/option[@value="{desired_category}"]')))
        category_option.click()

        wait.until(EC.presence_of_element_located((By.ID, 'id_rating'))).send_keys(data['rating'])
        wait.until(EC.presence_of_element_located((By.ID, 'id_description'))).send_keys(data['description'])
        wait.until(EC.presence_of_element_located((By.ID, 'id_price'))).send_keys(data['price'])

        # Select 'Currency' option
        desired_currency = data['currency']
        currency_option = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                     f'//select[@id="id_currency"]/option[@value="{desired_currency}"]')))
        currency_option.click()

        wait.until(EC.presence_of_element_located((By.ID, 'id_width'))).send_keys(data['width'])
        wait.until(EC.presence_of_element_located((By.ID, 'id_length'))).send_keys(data['length'])
        wait.until(EC.presence_of_element_located((By.ID, 'id_height'))).send_keys(data['height'])
        wait.until(EC.presence_of_element_located((By.ID, 'id_weight'))).send_keys(data['weight'])

        # Select 'Unit' option
        desired_measurement_unit = data['unit_weight']
        unit_option = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                 f'//select[@id="id_unit_weight"]/option[@value="{desired_measurement_unit}"]')))
        unit_option.click()

        datepicker = wait.until(EC.presence_of_element_located((By.ID, 'id_ad_duration_to')))
        datepicker.send_keys(data['ad_duration_to_day_and_month'])
        datepicker.send_keys(Keys.TAB)
        datepicker.send_keys(data['ad_duration_to_year'])

        # # Upload an image (assuming you have the image file path in data['image_path'])
        # image_input = self.browser.find_element(By.ID, 'id_image')
        # image_input.send_keys(data['image_path'])

        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        # Click the "Save Changes" button
        post_button = wait.until(EC.presence_of_element_located((By.ID, 'post_furniture_ad')))
        time.sleep(1)
        post_button.click()
