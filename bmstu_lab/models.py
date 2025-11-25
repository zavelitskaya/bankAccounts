from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Contract(models.Model):
    CONTRACT_TYPES = [
        ('RKO', 'Расчетно-кассовое обслуживание'),
        ('SALARY', 'Зарплатный проект'),
        ('ACQUIRING', 'Эквайринг'),
    ]
    
    contract_number = models.CharField(max_length=50, unique=True)
    client_name = models.CharField(max_length=500)
    contract_type = models.CharField(max_length=50, choices=CONTRACT_TYPES)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    image_url = models.URLField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_contracts', blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_contracts', blank=True, null=True)

    def __str__(self):
        return self.contract_number

    class Meta:
        db_table = 'contract'

class Account(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Черновик'),
        ('DELETED', 'Удалён'),
        ('FORMED', 'Сформирован'), 
        ('COMPLETED', 'Завершён'),
        ('REJECTED', 'Отклонён'),
    ]
    
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='DRAFT')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_accounts',blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_accounts',blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    moderator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                 related_name='moderated_accounts')
    account_number = models.CharField(max_length=34, blank=True, null=True)
    currency_code = models.IntegerField(blank=True, null=True)
    account_owner_code = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.account_number or f"Account {self.id}"

    class Meta:
        db_table = 'account'

class AccountContract(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, db_column='account_id')
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, db_column='contract_id')
    is_main_contract = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.account} – {self.contract}"

    class Meta:
        db_table = 'account_contract'
        unique_together = ('account', 'contract')