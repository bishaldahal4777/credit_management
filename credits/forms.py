from django import forms
from .models import Credit
from .models import Payment


class CreditForm(forms.ModelForm):
    class Meta:
        model = Credit
        fields = ['customer', 'amount', 'description', 'due_date', 'is_paid']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['credit', 'amount_paid']