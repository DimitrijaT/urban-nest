from django.contrib import admin
from .models import UrbanNestUser, FurnitureAd, OrderItem, ShoppingCart, Category


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
        'seller', 'name', 'category', 'rating', 'price', 'currency', 'status', 'creation_date', 'last_modified_date',
        'ad_duration_to')

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


admin.site.register(UrbanNestUser, UrbanNestUserAdmin)
admin.site.register(FurnitureAd, FurnitureAdAdmin)
admin.site.register(OrderItem)
admin.site.register(ShoppingCart)
