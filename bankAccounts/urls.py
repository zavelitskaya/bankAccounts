from django.contrib import admin
from django.urls import path
from bmstu_lab import views

urlpatterns = [
    path('', views.contracts_list, name='contracts_list'),
    path('contracts/<int:contract_id>/', views.contract_detail, name='contract_detail'),
    path('application/<int:application_id>/', views.cart, name='cart'),
]