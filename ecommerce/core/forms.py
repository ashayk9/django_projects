from django import forms

PAYMENT_CHOICES = (
    ('S','Stripe'),
    ('P', 'Paypal')
)


class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'adress line 1'}))
    appartment_address = forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder':'adress line 2'}))
    zip = forms.CharField()
    same_billing_address = forms.BooleanField(required=False)
    #save_info = forms.BooleanField(widget=forms.CheckboxInput())
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
