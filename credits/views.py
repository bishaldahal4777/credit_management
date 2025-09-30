from django.shortcuts import render, redirect
from .forms import CreditForm
from django.contrib.auth.decorators import login_required
from .models import Credit

@login_required
def add_credit(request):
    if request.method == 'POST':
        form = CreditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('credit_list')  # we will create this view next
    else:
        form = CreditForm()
    return render(request, 'credits/add_credit.html', {'form': form})

@login_required
def credit_list(request):
    # Show only credits for customers belonging to the logged-in shop
    credits = Credit.objects.filter(customer__shop=request.user).order_by('-date')
    return render(request, 'credits/credit_list.html', {'credits': credits})