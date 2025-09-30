from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from credits.models import Credit, Payment
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

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
