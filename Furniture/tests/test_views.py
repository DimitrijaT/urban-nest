from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from Furniture.models import Category, FrontCover, FurnitureAd, UrbanNestUser, About, Contact, MessageThread, \
    ShoppingCart, Message
from Furniture.views import index, details, category, adlist, add_furniture_ad, about, contact, register_request, \
    dashboard_home, shopping_cart, add_to_cart, remove_from_cart, checkout, my_orders, offers, offer_accept, \
    offer_decline, delete_furniture_ad, edit_furniture_ad, edit_settings, dashboard_report, dashboard_messages, \
    dashboard_thread_detail, checkout_success, create_thread, faq


class TestViews(TestCase):

    def setUp(self):
        # setup code
        self.client = Client(enforce_csrf_checks=False)

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

    def login_as_test_user(self):
        # self.client.login(username='testuser', password='testpassword')
        self.client.force_login(self.user)
    #
    #
    # def test_index_GET(self):
    #     # test code
    #     response = self.client.get(reverse('index'))
    #
    #     # assertions
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'index.html')
    #
    # def test_about_GET(self):
    #     # test code
    #     response = self.client.get(reverse('about'))
    #     # assertions
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'about.html')
    #
    # def test_contact_GET(self):
    #     # test code
    #     response = self.client.get(reverse('contact'))
    #     # assertions
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'contact.html')
    #
    # def test_addetails_GET(self):
    #     # test code
    #     response = self.client.get(reverse('addetails', args=['1']))
    #     # assertions
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'ad-details.html')
    #
    # def test_adcategory_GET(self):
    #     # test code
    #     response = self.client.get(reverse('adcategory'))
    #     # assertions
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'ad-category.html')
    #
    # def test_adlist_GET(self):
    #     # test code
    #     response = self.client.get(reverse('adlist', args=['1']))
    #     # assertions
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'ad-list.html')
    #
    # def test_ad_form_input_page_GET(self):
    #     self.login_as_test_user()
    #     # test code
    #     response = self.client.get(reverse('add_furniture_ad'))
    #     # assertions
    #     self.assertEquals(response.status_code, 200)
    #
    #     self.assertTemplateUsed(response, 'ad-add.html')
    #
    # def test_ad_edit_GET(self):
    #     self.login_as_test_user()
    #     # test code
    #     response = self.client.get(reverse('edit_furniture_ad', args=['1']))
    #     # assertions
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'ad-edit.html')
    #
    # def test_shopping_cart_GET(self):
    #     self.login_as_test_user()
    #     # test code
    #     response = self.client.get(reverse('shopping_cart'))
    #     # assertions
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'shopping-cart.html')
    #
    # def test_register_GET(self):
    #     # test code
    #     response = self.client.get(reverse('register'))
    #     # assertions
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'registration/register.html')
    #
    # def test_edit_settings_GET(self):
    #     self.login_as_test_user()
    #     # test code
    #     response = self.client.get(reverse('edit_settings'))
    #     # assertions
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'registration/edit_settings.html')
    #
    # def test_dashboard_home_GET(self):
    #     self.login_as_test_user()
    #     # test code
    #     response = self.client.get(reverse('dashboard_home'))
    #     # assertions
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'dashboard/dashboard-home.html')
    #
    # def test_dashboard_report_GET(self):
    #     self.login_as_test_user()
    #     # test code
    #     response = self.client.get(reverse('dashboard_report'))
    #     # assertions
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'dashboard/dashboard-report.html')
    #
    # def test_dashboard_messages_GET(self):
    #     self.login_as_test_user()
    #     # test code
    #     response = self.client.get(reverse('dashboard_messages'))
    #     # assertions
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'dashboard/dashboard-messages.html')
    #
    # def test_dashboard_thread_detail_GET(self):
    #     self.login_as_test_user()
    #     # test code
    #     response = self.client.get(reverse('dashboard_thread_detail', args=['1']))
    #     # assertions
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'dashboard/dashboard-thread-detail.html')
    #
    # def test_my_orders_GET(self):
    #     self.login_as_test_user()
    #     # test code
    #     response = self.client.get(reverse('my_orders'))
    #     # assertions
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'dashboard/dashboard-my-orders.html')
    #
    # def test_offers_GET(self):
    #     self.login_as_test_user()
    #     # test code
    #     response = self.client.get(reverse('offers'))
    #     # assertions
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'dashboard/dashboard-offers.html')
    #
    # def test_checkout_page_GET(self):
    #     self.login_as_test_user()
    #     # test code
    #     response = self.client.get(reverse('checkout'))
    #     # assertions
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'shopping-cart-wizard-details.html')
    #
    # def test_checkout_success_GET(self):
    #     self.login_as_test_user()
    #     # test code
    #     response = self.client.get(reverse('checkout_success'))
    #     # assertions
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'shopping-cart-wizard-success.html')
    #
    # def test_create_thread_GET(self):
    #     self.login_as_test_user()
    #     # test code
    #     response = self.client.get(reverse('create_thread', args=[1]))
    #     # assertions
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'create-thread.html')
    #
    # def test_faq_GET(self):
    #     # test code
    #     response = self.client.get(reverse('faq'))
    #     # assertions
    #     self.assertEquals(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'faq.html')
    #
    # def test_add_valid_furniture_to_cart_GET(self):
    #     self.login_as_test_user()
    #     # test code
    #     response = self.client.get(reverse('add_to_cart', args=[self.ad2.id]))
    #     # assertions
    #
    #     self.assertEquals(response.status_code, 302)
    #     self.assertEquals(self.shopping_cart.items.count(), 1)
    #
    # def test_add_own_product_to_cart_invalid_GET(self):
    #     self.login_as_test_user()
    #     # test code
    #     response = self.client.get(reverse('add_to_cart', args=[self.ad.id]))
    #     # assertions
    #     self.assertEquals(response.status_code, 302)
    #     self.assertEquals(self.shopping_cart.items.count(), 0)
    #
    # def test_remove_from_cart_GET(self):
    #     self.test_add_valid_furniture_to_cart_GET()
    #     # test code
    #     response = self.client.get(reverse('remove_from_cart', args=["1"]))
    #     # assertions
    #     self.assertEquals(response.status_code, 302)
    #     self.assertEquals(self.shopping_cart.items.count(), 0)
    #
    # def test_remove_from_cart_invalid_GET(self):
    #     self.test_add_valid_furniture_to_cart_GET()
    #     # test code
    #     response = self.client.get(reverse('remove_from_cart', args=["2"]))
    #     # assertions
    #     self.assertEquals(response.status_code, 404)
    #     self.assertEquals(self.shopping_cart.items.count(), 1)
    #
    # def test_add_furniture_ad_POST(self):
    #     self.login_as_test_user()
    #     form = {
    #         'name': 'Test Furniture 3',
    #         'category': self.category.id,
    #         'rating': 4,
    #         'description': 'Test description',
    #         'price': 100,
    #         'currency': 'USD',
    #         'width': 50,
    #         'length': 60,
    #         'height': 70,
    #         'weight': 30,
    #         'unit_weight': 'kg',
    #         'ad_duration_to': '2023-09-10',
    #     }
    #
    #     # test code
    #     response = self.client.post(reverse('add_furniture_ad'), data=form, follow=True)
    #
    #     # assertions
    #     self.assertRedirects(response, reverse('dashboard_home'))
    #
    #     self.assertEqual(FurnitureAd.objects.count(), 3)
    #
    #     ad = FurnitureAd.objects.get(name='Test Furniture 3')
    #     self.assertEquals(ad.pk, 3)
    #
    # def test_contact_us_POST_is_authenticated(self):
    #     self.login_as_test_user()
    #     form = {
    #         'user': self.urbanNestUser,
    #         'name': 'test_name',
    #         'email': 'test_email',
    #         'message': 'test_message'
    #     }
    #
    #     response = self.client.post(reverse('contact'), data=form, follow=True)
    #
    #     self.assertTemplateUsed(response, 'contact.html')
    #     self.assertEqual(Contact.objects.count(), 2)
    #
    # def test_contact_us_POST_is_not_authenticated(self):
    #     form = {
    #         'name': 'test_name',
    #         'email': 'test_email',
    #         'message': 'test_message'
    #     }
    #
    #     response = self.client.post(reverse('contact'), data=form, follow=True)
    #
    #     self.assertTemplateUsed(response, 'contact.html')
    #     self.assertEqual(Contact.objects.count(), 2)
    #
    # def test_edit_furniture_ad_POST(self):
    #     self.login_as_test_user()
    #     form = {
    #         'name': 'Edited Furniture',
    #         'category': self.category.id,
    #         'rating': 4,
    #         'description': 'Test description',
    #         'price': 100,
    #         'currency': 'USD',
    #         'width': 50,
    #         'length': 60,
    #         'height': 70,
    #         'weight': 30,
    #         'unit_weight': 'kg',
    #         'ad_duration_to': '2023-09-10',
    #     }
    #
    #     # test code
    #     response = self.client.post(reverse('edit_furniture_ad', args=[self.ad.id]), data=form, follow=True)
    #
    #     # assertions
    #     self.assertRedirects(response, reverse('dashboard_home'))
    #
    #     self.assertEqual(FurnitureAd.objects.count(), 2)
    #
    #     self.ad.refresh_from_db()
    #     self.assertEquals(self.ad.name, 'Edited Furniture')
    #
    # def test_create_new_thread_POST(self):
    #     self.login_as_test_user()
    #     form = {
    #         'title': 'New Thread Title',
    #     }
    #
    #     # test code
    #     response = self.client.post(reverse('create_thread', args=[self.ad2.id]), data=form, follow=True)
    #
    #     # assertions
    #     self.assertRedirects(response, reverse('dashboard_messages'))
    #
    #     self.assertEqual(MessageThread.objects.count(), 2)
    #
    #     thread = MessageThread.objects.get(title='New Thread Title')
    #     self.assertEquals(thread.pk, 2)
    #
    #     self.assertNotEquals(thread.seller, thread.customer)
    #
    # def test_create_new_thread_to_yourself_POST_invalid(self):
    #     self.login_as_test_user()
    #     form = {
    #         'title': 'New Thread Title',
    #     }
    #
    #     # test code
    #     response = self.client.post(reverse('create_thread', args=[self.ad.id]), data=form, follow=True)
    #
    #     # assertions
    #     self.assertEquals(response.status_code, 200)
    #
    # def test_add_thread_message(self):
    #     self.login_as_test_user()
    #     form = {
    #         'message': 'New Message',
    #     }
    #
    #     # test codes
    #     response = self.client.post(reverse('dashboard_thread_detail',
    #                                         args=[self.thread.id]),
    #                                 data=form,
    #                                 follow=True)
    #
    #     # assertions
    #     self.assertRedirects(response, reverse('dashboard_thread_detail', args=[self.thread.id]),)
    #
    #     self.assertEqual(Message.objects.count(), 1)
    #
    #     message = Message.objects.get(message='New Message')
    #     self.assertEquals(message.pk, 1)
