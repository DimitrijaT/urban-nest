"""
URL configuration for UrbanNest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Furniture.views import index, details, category, adlist, add_furniture_ad, about, contact, register_request, \
    dashboard_home, shopping_cart, add_to_cart, remove_from_cart, checkout, my_orders, offers, offer_accept, \
    offer_decline, delete_furniture_ad, edit_furniture_ad, edit_settings, dashboard_report, dashboard_messages, \
    dashboard_thread_detail, checkout_success, create_thread, faq
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', index, name='index'),
                  path('index/', index, name='index'),
                  path('about/', about, name='about'),
                  path('contact/', contact, name='contact'),
                  path('ad/details/<str:pk>', details, name='addetails'),
                  path('ad/category', category, name='adcategory'),
                  path('ad/adlist/<str:pk>/', adlist, name='adlist'),
                  path('ad/add_furniture_ad', add_furniture_ad, name='add_furniture_ad'),
                  path('ad/edit/<int:ad_id>/', edit_furniture_ad, name='edit_furniture_ad'),
                  path("shopping_cart", shopping_cart, name="shopping_cart"),
                  path("register", register_request, name="register"),
                  path('edit_settings/', edit_settings, name='edit_settings'),
                  path("accounts/", include("django.contrib.auth.urls")),  # new
                  path("dashboard/home", dashboard_home, name="dashboard_home"),
                  path("dashboard/report", dashboard_report, name="dashboard_report"),
                  path("dashboard/messages", dashboard_messages, name="dashboard_messages"),
                  path("dashboard/thread_detail/<int:thread_pk>", dashboard_thread_detail, name="dashboard_thread_detail"),
                  path("dashboard/my_orders", my_orders, name="my_orders"),
                  path("dashboard/offers", offers, name="offers"),
                  path("delete_furniture_ad/<int:ad_id>", delete_furniture_ad, name="delete_furniture_ad"),
                  path("offer_accept/<int:product_id>", offer_accept, name="offer_accept"),
                  path("offer_decline/<int:product_id>", offer_decline, name="offer_decline"),
                  path('add_to_cart/<int:furniture_id>/', add_to_cart, name='add_to_cart'),
                  path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
                  path('checkout/', checkout, name='checkout'),
                  # path('checkout_wizard/', checkout_wizard, name='checkout_wizard'),
                  path('checkout_success/', checkout_success, name='checkout_success'),
                  path('create_thread/<int:furniture_id>', create_thread, name='create_thread'),
                  path('faq/', faq, name='faq'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
