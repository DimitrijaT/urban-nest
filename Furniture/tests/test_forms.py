from django.contrib.auth.models import User
from django.test import TestCase

from Furniture.forms import FurnitureAdForm, ThreadForm, MessageForm, UrbanNestUserForm, NewUserForm
from Furniture.models import Category, UrbanNestUser, FurnitureAd


class TestForms(TestCase):

    def test_furniture_ad_form_valid_data(self):
        self.category = Category.objects.create(
            name='test_category',
            photo=None
        )
        form = FurnitureAdForm(data={
            'name': 'Test Furniture',
            'category': self.category.id,
            'rating': 4,
            'description': 'Test description',
            'price': 100,
            'currency': 'USD',
            'width': 50,
            'length': 60,
            'height': 70,
            'weight': 30,
            'unit_weight': 'kg',
            'ad_duration_to': '2023-09-10'
        })
        self.assertTrue(form.is_valid())

    def test_furniture_ad_form_no_data(self):
        form = FurnitureAdForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 12)

    def test_new_user_form_valid_data(self):
        form = NewUserForm(data={
            'username': 'test_username',
            'email': 'test_email@gmail.com',
            'password1': 'test_password',
            'password2': 'test_password',
        })
        self.assertTrue(form.is_valid())

    def test_new_user_form_no_data(self):
        form = NewUserForm(data={})
        self.assertFalse(form.is_valid())
        self.assertTrue(len(form.errors), 4)

    def test_urban_nest_user_valid_data(self):
        form = UrbanNestUserForm(data={
            "first_name": "test_first_name",
            "last_name": "test_last_name",
            "address": "test_address",
            "city": "test_city",
            "postal_code": "1000",
            "province": "test_province",
            "country": "MK",
            "phone_number": "123456789",
        })
        self.assertTrue(form.is_valid())

    def test_urban_nest_user_no_data(self):
        form = UrbanNestUserForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 8)

    def test_thread_form_valid_data(self):
        form = ThreadForm(data={
            'title': 'Test title',
        })
        self.assertTrue(form.is_valid())

    def test_thread_form_no_data(self):
        form = ThreadForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)

    def test_message_form_valid_data(self):
        form = MessageForm(data={
            'message': 'Test title',
        })
        self.assertTrue(form.is_valid())

    def test_message_form_no_data(self):
        form = MessageForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
