from django import forms
from .models import Credit
from .models import Payment


class CreditForm(forms.ModelForm):
    class Meta:
        model = Credit
        fields = ['customer', 'product_name', 'quantity', 'unit_amount', 'is_paid', 'description', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['credit', 'amount_paid']