from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField


class UrbanNestUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='images/users', null=True, blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    country = CountryField()
    phone_number = PhoneNumberField(blank=True)
    shopping_cart = models.ForeignKey('ShoppingCart', on_delete=models.CASCADE, null=True, blank=True)

    # every user has a shopping cart, it is empty by default
    # when a user adds an item to the shopping cart, the item is added to the shopping cart

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
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField()
    price = models.IntegerField()
    CURRENCY_CHOICES = [
        ('MKD', 'Denar'),
        ('EUR', 'Euro'),
        ('USD', 'Dollar'),
        # Add more currencies as needed
    ]

    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    width = models.IntegerField()
    length = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    UNIT_CHOICES = [
        ('kg', 'Kilograms'),
        ('lb', 'Pounds'),
    ]
    unit_weight = models.CharField(max_length=100, choices=UNIT_CHOICES)
    image = models.ImageField(upload_to='images/furnitures', null=True, blank=True)
    # auto_now_add is added automatically when creating a post
    creation_date = models.DateTimeField(auto_now_add=True)
    # auto_now is added automatically when editing a post
    last_modified_date = models.DateTimeField(auto_now=True)
    ad_duration_to = models.DateField()
    views = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    buyer = models.ForeignKey(UrbanNestUser, on_delete=models.CASCADE, null=True, blank=True)
    furniture = models.ForeignKey(FurnitureAd, on_delete=models.CASCADE)
    # auto_now_add is added automatically when creating a post
    creation_date = models.DateTimeField(auto_now_add=True)

    class Status(models.TextChoices):
        IN_CART = 'IC', _('In Shopping Cart')
        PENDING = 'PE', _('Pending')
        ACCEPTED = 'AC', _('Accepted')
        CANCELLED = 'CA', _('Cancelled')
        DELIVERED = 'DE', _('Delivered')

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.IN_CART,
    )

    def is_status(self):
        return self.status in {
            self.Status.IN_CART,
            self.Status.PENDING,
            self.Status.ACCEPTED,
            self.Status.CANCELLED,
            self.Status.DELIVERED,
        }


class ShoppingCart(models.Model):
    buyer = models.OneToOneField(UrbanNestUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, blank=True)

    # auto_now_add is added automatically when creating a post
    creation_date = models.DateTimeField(auto_now_add=True)
    # auto_now is added automatically when editing a post
    last_modified_date = models.DateTimeField(auto_now=True)

    def get_total_num_items(self):
        return self.items.count()

    def get_total_price(self):
        total = 0
        for item in self.items.all():
            total += item.furniture.price
        return total

    def __str__(self):
        return f'{self.buyer.first_name} {self.buyer.last_name}\'s shopping cart'


#  Add Testimonials!

class Testimonial(models.Model):
    user = models.ForeignKey(UrbanNestUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/testimonials', null=True, blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    quote = models.TextField()
    nickname = models.CharField(max_length=100)

    # auto_now_add is added automatically when creating a post
    creation_date = models.DateTimeField(auto_now_add=True)
    # auto_now is added automatically when editing a post
    last_modified_date = models.DateTimeField(auto_now=True)
    visible = models.BooleanField(default=False)

    def __str__(self):
        return self.nickname


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    # auto_now_add is added automatically when creating a post
    creation_date = models.DateTimeField(auto_now_add=True)
    # auto_now is added automatically when editing a post
    last_modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question


class Contact(models.Model):
    user = models.ForeignKey(UrbanNestUser, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    # auto_now_add is added automatically when creating a post
    creation_date = models.DateTimeField(auto_now_add=True)
    # auto_now is added automatically when editing a post
    last_modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class About(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='images/about', null=True, blank=True)
    # auto_now_add is added automatically when creating a post
    creation_date = models.DateTimeField(auto_now_add=True)
    # auto_now is added automatically when editing a post
    last_modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class FrontCover(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=255)
    subtitle_1 = models.CharField(max_length=255)
    subtitle_2 = models.CharField(max_length=255)
    buy_button = models.CharField(max_length=255)
    sell_button = models.CharField(max_length=255)
    cover_page = models.ImageField(upload_to='images/front_cover', null=True, blank=True)
    # auto_now_add is added automatically when creating a post
    creation_date = models.DateTimeField(auto_now_add=True)
    # auto_now is added automatically when editing a post
    last_modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
