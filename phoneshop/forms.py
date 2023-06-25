from django.forms import ModelForm
from .models import Order, Payment
from django import forms


class OrderForm(ModelForm):
    class Meta:
        model=Order
        fields=('first_name', 'last_name', 'telephone_number', 'phone_model', 'description')



class PaymentForm(forms.ModelForm):
    class Meta:
        model=Payment
        fields=("amount", "email")