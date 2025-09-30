from django.urls import path
from . import views

urlpatterns = [
    path('', views.credit_list, name='credit_list'),
    path('add/', views.add_credit, name='add_credit'),
    path('payments/add/', views.add_payment, name='add_payment'),
    path('payments/', views.payment_list, name='payment_list'),


]
