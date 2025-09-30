from django.shortcuts import render, redirect
from .forms import CreditForm
from django.contrib.auth.decorators import login_required
from .models import Credit, Payment
from .forms import CreditForm, PaymentForm
from django.db.models import Q
from django.utils import timezone

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
    search_query = request.GET.get('q', '')  # search term
    if search_query:
        credits = Credit.objects.filter(
            Q(customer__name__icontains=search_query),
            customer__shop=request.user
        ).order_by('-date')
    else:
        credits = Credit.objects.filter(customer__shop=request.user).order_by('-date')

    today = timezone.now().date()  # current date
    return render(request, 'credits/credit_list.html', {
        'credits': credits,
        'search_query': search_query,
        'today': today,   # pass today to template
    })

@login_required
def add_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            # Check if credit is fully paid
            total_paid = sum(p.amount_paid for p in payment.credit.payment_set.all())
            if total_paid >= payment.credit.amount:
                payment.credit.is_paid = True
                payment.credit.save()
            return redirect('payment_list')
    else:
        form = PaymentForm()
    return render(request, 'credits/add_payment.html', {'form': form})

@login_required
def payment_list(request):
    # Show payments for credits belonging to the logged-in shop
    payments = Payment.objects.filter(credit__customer__shop=request.user).order_by('-payment_date')
    return render(request, 'credits/payment_list.html', {'payments': payments})

