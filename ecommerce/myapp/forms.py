from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=250)

    class Meta:
        model = User
        fields = ('username','firstname','lastname','email','password1','password2')
