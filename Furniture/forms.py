from django import forms
from .models import FurnitureAd, UrbanNestUser, OrderItem, ShoppingCart, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class FurnitureAdForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FurnitureAdForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

        # Override widget for ad_duration_to field
        self.fields['ad_duration_to'].widget = forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control datepicker'}
        )

    class Meta:
        model = FurnitureAd
        exclude = ["user", "seller", "views", "status"]


# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UrbanNestUserForm(forms.ModelForm):
    class Meta:
        model = UrbanNestUser
        fields = (
            "first_name",
            "last_name",
            "photo",
            "address",
            "city",
            "postal_code",
            "province",
            "country",
            "phone_number",
        )
