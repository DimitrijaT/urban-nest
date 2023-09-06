from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from Furniture.models import Category, FrontCover, FurnitureAd, UrbanNestUser, About, Contact, MessageThread, \
    ShoppingCart, Message
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.test import Client
import time


class IndexPage(StaticLiveServerTestCase):
    port: int = 8000
    host = 'localhost'

    # Runs before every test function
    def setUp(self):
        self.browser = webdriver.Chrome()

        self.frontCover = FrontCover.objects.create(
            active=True,
            title='test_title',
            subtitle_1='test_subtitle_1',
            subtitle_2='test_subtitle_2',
            buy_button='test_buy_button_text',
            sell_button='test_sell_button_text',
            cover_page=None
        )

        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpassword2'
        )

        self.urbanNestUser = UrbanNestUser.objects.create(
            user=self.user,
            first_name='test_first_name',
            last_name='test_last_name',
            phone_number='test_phone_number',
            address='test_address',
            city='test_city',
            country='test_country',
        )
        self.urbanNestUser2 = UrbanNestUser.objects.create(
            user=self.user2,
            first_name='test_first_name2',
            last_name='test_last_name2',
            phone_number='test_phone_number2',
            address='test_address2',
            city='test_city2',
            country='test_country2',
        )

        self.shopping_cart = ShoppingCart.objects.create(
            buyer=self.urbanNestUser,
        )
        self.shopping_cart2 = ShoppingCart.objects.create(
            buyer=self.urbanNestUser2,
        )
        self.category = Category.objects.create(
            name='test_category',
            photo=None
        )
        self.ad = FurnitureAd.objects.create(
            seller=self.urbanNestUser,
            name='Test Furniture',
            category=self.category,
            rating=4,
            description='Test description',
            price=100,
            currency='USD',
            width=50,
            length=60,
            height=70,
            weight=30,
            unit_weight='kg',
            ad_duration_to='2023-12-31',
            views=0,
            active=True
        )
        self.ad2 = FurnitureAd.objects.create(
            seller=self.urbanNestUser2,
            name='Test Furniture',
            category=self.category,
            rating=4,
            description='Test description',
            price=100,
            currency='USD',
            width=50,
            length=60,
            height=70,
            weight=30,
            unit_weight='kg',
            ad_duration_to='2023-12-31',
            views=0,
            active=True
        )
        self.urbanNestUser.shopping_cart = self.shopping_cart
        self.urbanNestUser2.shopping_cart = self.shopping_cart2

        self.about = About.objects.create(
            title='test_title',
            description='test_description',
            image=None
        )
        self.contact = Contact.objects.create(
            user=self.urbanNestUser,
            name='test_name',
            email='test_email',
            message='test_message'
        )
        self.thread = MessageThread.objects.create(
            seller=self.urbanNestUser,
            customer=self.urbanNestUser2,
            furniture_ad=self.ad,
            title='test_title',
            active=True)

    # Runs after every test function
    def tearDown(self):
        self.browser.close()

    # def test_foo(self):
    #     self.assertEqual(1, 1)

    def test_index_page_is_displayed(self):
        self.browser.get(self.live_server_url)
        time.sleep(20)
