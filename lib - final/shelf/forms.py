from django import forms
from .models import BookInstance


class Loan_Form(forms.ModelForm):
    class Meta:
        model=BookInstance
        fields=(
            #'borrower',
            #'book',
            'due_back',
        )

class Renew_form(forms.Form):
    renewal_date=forms.DateField()

class Reserve_Form(forms.ModelForm):
    class Meta:
        model=BookInstance
        fields=(
            'reservations',
        )


