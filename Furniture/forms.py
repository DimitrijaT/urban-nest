from django import forms
from .models import FurnitureAd, UrbanNestUser, OrderItem, ShoppingCart, Category


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