from django import forms
from .models import Credit

class CreditForm(forms.ModelForm):
    class Meta:
        model = Credit
        fields = ['customer', 'amount', 'description', 'due_date', 'is_paid']
