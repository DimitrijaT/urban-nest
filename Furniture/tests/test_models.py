from django.contrib.auth.models import User
from django.test import TestCase

from Furniture.models import FurnitureAd, UrbanNestUser, ShoppingCart, Category, Product


class TestModels(TestCase):

    def setUp(self):
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

        self.category = Category.objects.create(
            name='test_category',
        )

        self.ad = FurnitureAd.objects.create(
            seller=self.urbanNestUser2,
            name='Test Furniture',
            category=self.category,
            rating=4,
            description='Test description',
            price=500,
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
            price=1000,
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
        self.category = Category.objects.create(
            name='test_category',
            photo=None
        )

    def create_shopping_cart_and_add_products_to_cart(self):
        self.shopping_cart = ShoppingCart.objects.create(buyer=self.urbanNestUser)
        self.urbanNestUser.shopping_cart = self.shopping_cart

        product1 = Product.objects.create(buyer=self.urbanNestUser, furniture=self.ad)
        product2 = Product.objects.create(buyer=self.urbanNestUser, furniture=self.ad2)

        self.shopping_cart.items.add(product1)
        self.shopping_cart.items.add(product2)

    def test_total_items_in_shopping_cart(self):
        self.create_shopping_cart_and_add_products_to_cart()

        self.assertEqual(self.shopping_cart.get_total_num_items(), 2)

    def test_total_price_in_shopping_cart(self):
        self.create_shopping_cart_and_add_products_to_cart()

        self.assertEqual(self.shopping_cart.get_total_price(), 1500)
