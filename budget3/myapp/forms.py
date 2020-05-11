from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,ExpenseInfo
from django.forms import ModelForm


class SignUpForm(UserCreationForm, forms.ModelForm):

    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    dob = forms.DateField(help_text='required Format: yyyy-mm-dd')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'dob', 'password1', 'password2',)


class ExpensesForm(forms.ModelForm):
    # expenditure = forms.IntegerField()
    # cost = forms.IntegerField()
    # date = forms.DateField(help_text='required Format:yyyy-mm-dd')

    class Meta:
        model = ExpenseInfo
        fields = ('expenditure', 'intake', 'date_added',)
