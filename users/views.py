from time import timezone
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from credits.models import Credit, Payment
from django.db.models import Sum
from customers.models import Customer
from credits.utils import customer_balance
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("dashboard")  # redirect to home page
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "users/login.html")

@login_required
def dashboard(request):
    # Total credit for this shop
    total_credit = Credit.objects.filter(customer__shop=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Total paid for this shop
    total_paid = Payment.objects.filter(credit__customer__shop=request.user).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    
    # Total due
    total_due = total_credit - total_paid

    context = {
        'total_credit': total_credit,
        'total_paid': total_paid,
        'total_due': total_due,
    }
    return render(request, 'users/dashboard.html', context)

@login_required
def customer_overview(request):
    search_query = request.GET.get('q', '')  # get search term from URL
    if search_query:
        customers = Customer.objects.filter(shop=request.user, name__icontains=search_query)
    else:
        customers = Customer.objects.filter(shop=request.user)

    customer_data = []
    for customer in customers:
        balance = customer_balance(customer)
        credits = customer.credit_set.all()
        overdue = any([credit.due_date < timezone.now().date() and not credit.is_paid for credit in credits])
        customer_data.append({'customer': customer, 'balance': balance, 'overdue': overdue})
    
    return render(request, 'users/customer_overview.html', {'customer_data': customer_data, 'search_query': search_query})
