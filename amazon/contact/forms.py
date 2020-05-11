from django import forms
from .models import Contact


class Contact_Form(forms.ModelForm):
    #name = forms.CharField()
    #email = forms.EmailField()

    class Meta:
        model = Contact
        fields = ['name', 'email']
