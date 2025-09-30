from django.db.models import Sum
from .models import Credit, Payment
from django.utils import timezone

def customer_balance(customer):
    total_credit = Credit.objects.filter(customer=customer).aggregate(Sum('amount'))['amount__sum'] or 0
    total_paid = Payment.objects.filter(credit__customer=customer).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    return total_credit - total_paid

def is_overdue(credit):
    if not credit.is_paid and credit.due_date < timezone.now().date():
        return True
    return False