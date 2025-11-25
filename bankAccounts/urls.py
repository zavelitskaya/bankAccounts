from django.contrib import admin
from django.urls import path
from bmstu_lab import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.contracts_list, name='contracts_list'),
    path('contracts/<int:contract_id>/', views.contract_detail, name='contract_detail'),
    path('accounts/<int:account_id>/', views.cart, name='cart'),
    path('accounts/<int:account_id>/delete/', views.delete_application, name='delete_application'),
    path('contracts/<int:contract_id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('accounts/<int:account_id>/update-account-number/', views.update_account_number, name='update_account_number'),
]