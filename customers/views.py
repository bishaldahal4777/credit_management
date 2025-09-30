from django.shortcuts import render, redirect
from .models import Customer
from .forms import CustomerForm
from django.contrib.auth.decorators import login_required

@login_required
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.shop = request.user  # link to logged-in shop
            customer.save()
            return redirect('customer_overview')
    else:
        form = CustomerForm()
    return render(request, 'customers/add_customer.html', {'form': form})
