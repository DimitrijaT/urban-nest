from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from Furniture.models import Category, FrontCover, UrbanNestUser, About, Contact, ShoppingCart, FurnitureAd
from functional_tests.common_database import CommonDatabaseSetup
from functional_tests.common_methods import CommonMethods
from functional_tests.template_classes.ad_add import PostAdPage
from functional_tests.template_classes.ad_category import CategoryPage
from functional_tests.template_classes.ad_details import AdDetailedPage
from functional_tests.template_classes.ad_list import AdListPage
from functional_tests.template_classes.dashboard_home import DashboardHomePage
from functional_tests.template_classes.login import LoginPage
from functional_tests.template_classes.shopping_cart import ShoppingCartPage
from functional_tests.template_classes.shopping_cart_wizard_details import OrderDetailsPage
from django.test import TransactionTestCase


class SeleniumSellProduct(StaticLiveServerTestCase, CommonDatabaseSetup):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)
        self.setUpDatabase()

    # Runs after every test function
    def tearDown(self):
        self.browser.close()
        self.tearDownDatabase()
        if hasattr(self, 'db_connection'):
            self.db_connection.close()

    def test_sell_a_product(self):
        CommonMethods.login(self.browser, self.live_server_url)

        dashboard_home_page = DashboardHomePage(self.browser, self.live_server_url)
        dashboard_home_page.open_dashboard_home_page()
        dashboard_home_page.open_sell_furniture_ad_page()

        post_ad_page = PostAdPage(self.browser, self.live_server_url)
        post_ad_page.sell_product(data={
            'name': 'Test Furniture',
            'category': 1,
            'rating': 4,
            'description': 'Test description',
            'price': 100,
            'currency': "MKD",
            'width': 50,
            'length': 60,
            'height': 70,
            'weight': 30,
            'unit_weight': 'kg',
            'ad_duration_to_day_and_month': '2911',
            'ad_duration_to_year': '2025',
        })

        dashboard_home_page.assert_product_is_up_for_sale()
        # Wait until the response is received
        WebDriverWait(self.browser, 2).until(
            lambda driver: driver.find_element(By.TAG_NAME, "body")
        )

    # def test_foo(self):
    #     self.assertEqual(1, 1)
    #
    # def test_index_page_is_displayed(self):
    #     self.browser.get(self.live_server_url)
    #     # time.sleep(20)
    #     div = self.browser.find_element(By.ID, 'front_cover_title_div')
    #     self.assertEquals(div.find_element(By.ID, 'title_text').text, 'test_title')
    #
    # def test_press_login(self):
    #     self.browser.get(self.live_server_url)
    #     wait = WebDriverWait(self.browser, 10)
    #     login_button = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Please log in.')))
    #     login_button.click()
    #     login_page_url = self.live_server_url + reverse('login')
    #     self.assertEquals(self.browser.current_url, login_page_url)
    #
