from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('customers/', views.customer_overview, name='customer_overview'),
    path('login/', views.user_login, name='login'),

]
