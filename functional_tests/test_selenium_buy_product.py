# from django.contrib.auth.models import User
# from django.contrib.staticfiles.testing import LiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
#
# from Furniture.models import FurnitureAd
# from functional_tests.common_database import CommonDatabaseSetup
# from functional_tests.common_methods import CommonMethods
# from functional_tests.template_classes.ad_category import CategoryPage
# from functional_tests.template_classes.ad_details import AdDetailedPage
# from functional_tests.template_classes.ad_list import AdListPage
# from functional_tests.template_classes.dashboard_home import DashboardHomePage
# from functional_tests.template_classes.login import LoginPage
# from functional_tests.template_classes.shopping_cart import ShoppingCartPage
# from functional_tests.template_classes.shopping_cart_wizard_details import OrderDetailsPage
#
#
# class SeleniumBuyProduct(LiveServerTestCase, CommonDatabaseSetup):
#     def setUp(self):
#         self.browser = webdriver.Chrome()
#         self.browser.implicitly_wait(3)
#         self.setUpDatabase()
#
#     # Runs after every test function
#     def tearDown(self):
#         self.browser.close()
#         self.tearDownDatabase()
#         if hasattr(self, 'db_connection'):
#             self.db_connection.close()
#
#     def test_buy_a_product(self):
#         self.ad = FurnitureAd.objects.create(
#             seller=self.urbanNestUser2,
#             name='Test Furniture',
#             category=self.category,
#             rating=4,
#             description='Test description',
#             price=100,
#             currency='USD',
#             width=50,
#             length=60,
#             height=70,
#             weight=30,
#             unit_weight='kg',
#             ad_duration_to='2023-12-31',
#             views=0,
#             active=True
#         )
#         self.ad.save()
#         CommonMethods.login(self.browser, self.live_server_url)
#
#         category_page = CategoryPage(self.browser, self.live_server_url)
#         category_page.open_ad_category_page()
#         category_page.choose_category()
#
#         ad_list_page = AdListPage(self.browser, self.live_server_url)
#         ad_list_page.choose_advertised_furniture()
#
#         ad_detailed_page = AdDetailedPage(self.browser, self.live_server_url)
#         ad_detailed_page.add_product_to_cart()
#
#         shopping_cart_page = ShoppingCartPage(self.browser, self.live_server_url)
#         shopping_cart_page.open_shopping_cart_page()
#         shopping_cart_page.checkout_cart()
#
#         checkout_page = OrderDetailsPage(self.browser, self.live_server_url)
#         checkout_page.order_products()
#         checkout_page.assert_order_is_created()
#         # Wait until the response is received
#         WebDriverWait(self.browser, 2).until(
#             lambda driver: driver.find_element(By.TAG_NAME, "body")
#         )
