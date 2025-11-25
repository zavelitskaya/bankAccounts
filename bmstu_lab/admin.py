from django.contrib import admin
from .models import Contract, Account, AccountContract

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['contract_number', 'client_name', 'contract_type', 'is_active', 'start_date']
    list_filter = ['contract_type', 'is_active', 'start_date']
    search_fields = ['contract_number', 'client_name']
    
    fieldsets = [
        ('Основная информация', {
            'fields': ['contract_number', 'client_name', 'contract_type', 'description']
        }),
        ('Даты и статус', {
            'fields': ['start_date', 'end_date', 'is_active']
        }),
        ('Дополнительно', {
            'fields': ['image_url', 'created_by', 'updated_by'],
            'classes': ['collapse']
        }),
    ]

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'account_number', 'created_by', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['account_number', 'created_by__username']
    
    fieldsets = [
        ('Основная информация', {
            'fields': ['status', 'account_number', 'currency_code', 'account_owner_code']
        }),
        ('Модерация', {
            'fields': ['moderator', 'completed_at']
        }),
        ('Системные', {
            'fields': ['created_by', 'updated_by'],
            'classes': ['collapse']
        }),
    ]

@admin.register(AccountContract)
class AccountContractAdmin(admin.ModelAdmin):
    list_display = ['id', 'account', 'contract', 'is_main_contract']
    list_filter = ['is_main_contract']
    search_fields = ['account__account_number', 'contract__contract_number']