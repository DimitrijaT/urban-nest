from django.test import SimpleTestCase
from django.urls import reverse, resolve
from Furniture.views import index, details, category, adlist, add_furniture_ad, about, contact, register_request, \
    dashboard_home, shopping_cart, add_to_cart, remove_from_cart, checkout, my_orders, offers, offer_accept, \
    offer_decline, delete_furniture_ad, edit_furniture_ad, edit_settings, dashboard_report, dashboard_messages, \
    dashboard_thread_detail, checkout_success, create_thread, faq


class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('index')
        # print(resolve(url))
        self.assertEquals(resolve(url).func, index)

    def test_about_url_resolves(self):
        url = reverse('about')
        self.assertEquals(resolve(url).func, about)

    def test_contact_url_resolves(self):
        url = reverse('contact')
        self.assertEquals(resolve(url).func, contact)

    def test_ad_details_url_resolves(self):
        url = reverse('addetails', args=['primary_key'])
        self.assertEquals(resolve(url).func, details)

    def test_view_categories_url_resolves(self):
        url = reverse('adcategory')
        self.assertEquals(resolve(url).func, category)

    def test_category_list_url_resolves(self):
        url = reverse('adlist', args=['primary_key'])
        self.assertEquals(resolve(url).func, adlist)

    def test_add_furniture_view_url_resolves(self):
        url = reverse('add_furniture_ad')
        self.assertEquals(resolve(url).func, add_furniture_ad)

    def test_edit_furniture_view_url_resolves(self):
        url = reverse('edit_furniture_ad', args=[1])
        self.assertEquals(resolve(url).func, edit_furniture_ad)

    def test_shopping_cart_url_resolves(self):
        url = reverse('shopping_cart')
        self.assertEquals(resolve(url).func, shopping_cart)

    def test_register_request_url_resolves(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register_request)

    def test_edit_settings_url_resolves(self):
        url = reverse('edit_settings')
        self.assertEquals(resolve(url).func, edit_settings)

    def test_dashboard_home_url_resolves(self):
        url = reverse('dashboard_home')
        self.assertEquals(resolve(url).func, dashboard_home)

    def test_dashboard_report_url_resolves(self):
        url = reverse('dashboard_report')
        self.assertEquals(resolve(url).func, dashboard_report)

    def test_dashboard_messages_url_resolves(self):
        url = reverse('dashboard_messages')
        self.assertEquals(resolve(url).func, dashboard_messages)

    def test_dashboard_thread_detail_url_resolves(self):
        url = reverse('dashboard_thread_detail', args=[1])  # Replace 1 with a valid thread_pk
        self.assertEquals(resolve(url).func, dashboard_thread_detail)

    def test_my_orders_url_resolves(self):
        url = reverse('my_orders')
        self.assertEquals(resolve(url).func, my_orders)

    def test_offers_url_resolves(self):
        url = reverse('offers')
        self.assertEquals(resolve(url).func, offers)

    def test_delete_furniture_ad_url_resolves(self):
        url = reverse('delete_furniture_ad', args=[1])
        self.assertEquals(resolve(url).func, delete_furniture_ad)

    def test_offer_accept_url_resolves(self):
        url = reverse('offer_accept', args=[1])
        self.assertEquals(resolve(url).func, offer_accept)

    def test_offer_decline_url_resolves(self):
        url = reverse('offer_decline', args=[1])
        self.assertEquals(resolve(url).func, offer_decline)

    def test_add_to_cart_url_resolves(self):
        url = reverse('add_to_cart', args=[1])
        self.assertEquals(resolve(url).func, add_to_cart)

    def test_remove_from_cart_url_resolves(self):
        url = reverse('remove_from_cart', args=[1])
        self.assertEquals(resolve(url).func, remove_from_cart)

    def test_checkout_url_resolves(self):
        url = reverse('checkout')
        self.assertEquals(resolve(url).func, checkout)

    def test_checkout_success_url_resolves(self):
        url = reverse('checkout_success')
        self.assertEquals(resolve(url).func, checkout_success)

    def test_create_thread_url_resolves(self):
        url = reverse('create_thread', args=[1])
        self.assertEquals(resolve(url).func, create_thread)

    def test_faq_url_resolves(self):
        url = reverse('faq')
        self.assertEquals(resolve(url).func, faq)
