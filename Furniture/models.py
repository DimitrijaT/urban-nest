from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField


class UrbanNestUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='images/users', null=True, blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    country = CountryField()
    phone_number = models.CharField(max_length=9)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Category(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='images/categories', null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class FurnitureAd(models.Model):
    seller = models.ForeignKey(UrbanNestUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    rating = models.IntegerField()
    description = models.TextField()
    price = models.IntegerField()
    currency = models.CharField(max_length=3)
    width = models.IntegerField()
    length = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    unit_weight = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/furnitures', null=True, blank=True)
    status = models.CharField(max_length=100)
    # auto_now_add is added automatically when creating a post
    creation_date = models.DateTimeField(auto_now_add=True)
    # auto_now is added automatically when editing a post
    last_modified_date = models.DateTimeField(auto_now=True)
    ad_duration_to = models.DateField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    buyer = models.ForeignKey(UrbanNestUser, on_delete=models.CASCADE, null=True, blank=True)
    furniture = models.ForeignKey(FurnitureAd, on_delete=models.CASCADE)
    # auto_now_add is added automatically when creating a post
    creation_date = models.DateTimeField(auto_now_add=True)

    class Status(models.TextChoices):
        PENDING = 'PE', _('Pending')
        ACCEPTED = 'AC', _('Accepted')
        CANCELLED = 'CA', _('Cancelled')
        DELIVERED = 'DE', _('Delivered')

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PENDING,
    )

    def is_status(self):
        return self.status in {
            self.Status.PENDING,
            self.Status.ACCEPTED,
            self.Status.CANCELLED,
            self.Status.DELIVERED,
        }


class ShoppingCart(models.Model):
    buyer = models.ForeignKey(UrbanNestUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    # auto_now_add is added automatically when creating a post
    creation_date = models.DateTimeField(auto_now_add=True)
    # auto_now is added automatically when editing a post
    last_modified_date = models.DateTimeField(auto_now=True)

    class Status(models.TextChoices):
        PENDING = 'PE', _('Pending')
        ACCEPTED = 'AC', _('Accepted')
        CANCELLED = 'CA', _('Cancelled')
        DELIVERED = 'DE', _('Delivered')

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.PENDING,
    )

    def is_status(self):
        return self.status in {
            self.Status.PENDING,
            self.Status.ACCEPTED,
            self.Status.CANCELLED,
            self.Status.DELIVERED,
        }

    def get_total_num_items(self):
        return self.items.count()

    def get_total_price(self):
        total = 0
        for item in self.items.all():
            total += item.price
        return total


#  Add Testimonials!

class Testimonials(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    image = models.ImageField(upload_to='images/testimonials', null=True, blank=True)
    # auto_now_add is added automatically when creating a post
    creation_date = models.DateTimeField(auto_now_add=True)
    # auto_now is added automatically when editing a post
    last_modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
