from django import forms

from .models import Product


class RawForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField()
    price = forms.DecimalField(max_digits=100, decimal_places=2)