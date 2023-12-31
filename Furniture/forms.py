from django import forms
from .models import FurnitureAd, UrbanNestUser, Product, ShoppingCart, Category, MessageThread, Message
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# import django_filters


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
        exclude = ["user", "seller", "views", "status", "active"]


# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

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

    def __init__(self, *args, **kwargs):
        super(UrbanNestUserForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

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


class ThreadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ThreadForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = MessageThread
        fields = (
            "title",
        )


class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

        # Customize the "message" field widget
        self.fields['message'].widget.attrs.update({
            'class': 'form-control',
            'rows': 1,  # Display only 1 row initially
            'placeholder': 'Type your message here...',
            'style': 'resize: none;'  # Disable text area resizing
        })

    class Meta:
        model = Message
        fields = ("message",)

    # Override the label for the "message" field
    message = forms.CharField(label='', widget=forms.Textarea)
