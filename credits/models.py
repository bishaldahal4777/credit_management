from django.db import models
from customers.models import Customer

# Create your models here.
class Credit(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)

class Payment(models.Model):
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.credit.customer.name} - {self.amount_paid}"
