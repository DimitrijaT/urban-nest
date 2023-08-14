from django.contrib import admin
from django.contrib.auth.models import User

from .models import UrbanNestUser, FurnitureAd, Product, ShoppingCart, Category, Testimonial, FAQ, Contact, About, \
    FrontCover
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# Register your models here.

class UrbanNestUserAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'first_name', 'last_name', 'address', 'city', 'postal_code', 'province', 'country', 'phone_number')

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        if obj and request.user == obj.user:
            return True
        return False


class FurnitureAdAdmin(admin.ModelAdmin):
    list_display = (
        'seller', 'name', 'category', 'rating', 'price', 'currency', 'creation_date', 'last_modified_date',
        'ad_duration_to')
    exclude = ('seller', 'views', 'status', 'creation_date', 'last_modified_date')

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        if obj and request.user == obj.seller.user:
            return True
        return False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

    def has_view_permission(self, request, obj=None):
        return True


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UrbanNestUserInline(admin.StackedInline):
    model = UrbanNestUser
    can_delete = False
    verbose_name_plural = "employee"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [UrbanNestUserInline]


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'creation_date', 'last_modified_date')

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        if obj and request.user == obj.buyer.user:
            return True
        return False


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'furniture', 'creation_date')

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        if obj and request.user == obj.buyer.user:
            return True
        return False


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(UrbanNestUser, UrbanNestUserAdmin)
admin.site.register(FurnitureAd, FurnitureAdAdmin)
admin.site.register(Testimonial)
admin.site.register(FAQ)
admin.site.register(Contact)
admin.site.register(About)
admin.site.register(FrontCover)
