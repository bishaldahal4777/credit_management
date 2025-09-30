from django.db.models import Sum
from .models import Credit, Payment

def customer_balance(customer):
    total_credit = Credit.objects.filter(customer=customer).aggregate(Sum('amount'))['amount__sum'] or 0
    total_paid = Payment.objects.filter(credit__customer=customer).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    return total_credit - total_paid
