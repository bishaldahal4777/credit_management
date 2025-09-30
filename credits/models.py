from django.db import models
from customers.models import Customer
from django.contrib.auth.models import User

# Create your models here.
class Credit(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    unit_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_paid = models.BooleanField(default=False)  # True if fully paid
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)  # record exact datetime
    due_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # who entered the credit

    def save(self, *args, **kwargs):
        # auto-calculate total
        self.total_amount = self.quantity * self.unit_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer} - {self.product_name} - {self.total_amount}"

class Payment(models.Model):
    credit = models.ForeignKey(Credit, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.credit.customer.name} - {self.amount_paid}"
