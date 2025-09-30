from django.shortcuts import render, redirect
from .forms import CreditForm
from django.contrib.auth.decorators import login_required

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
