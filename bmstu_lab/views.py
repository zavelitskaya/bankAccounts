from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.utils import timezone
from django.http import Http404, JsonResponse
from django.db import connection
from .models import Contract, Account, AccountContract
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

def get_current_draft_account(user_id):
    """Получаем текущую заявку в статусе Draft для пользователя через ORM"""
    try:
        return Account.objects.get(created_by_id=user_id, status='DRAFT')
    except Account.DoesNotExist:
        return None

def get_cart_count(user_id):
    """Получаем количество услуг в корзине через ORM"""
    draft_account = get_current_draft_account(user_id)
    if draft_account:
        return AccountContract.objects.filter(account_id=draft_account.id).count()
    return 0

def contracts_list(request):
    """GET: Список всех услуг (договоров) с поиском через ORM"""
    search_query = request.GET.get('search', '').strip()
    
    # Берем активные договоры из БД через ORM
    contracts = Contract.objects.filter(is_active=True)
    
    if search_query:
        # Поиск через ORM
        contracts = contracts.filter(
            Q(client_name__icontains=search_query) |
            Q(contract_number__icontains=search_query) |
            Q(contract_type__icontains=search_query)
        )
    
    # Временно: user_id = 1 для демо
    user_id = 1
    cart_count = get_cart_count(user_id)
    has_draft_account = get_current_draft_account(user_id) is not None
    current_account_id = get_current_draft_account(user_id).id if has_draft_account else None
    
    return render(request, 'contracts_list.html', {
        'services': contracts,
        'cart_count': cart_count,
        'search_query': search_query,
        'has_draft_account': has_draft_account,
        'current_account_id': current_account_id
    })

def contract_detail(request, contract_id):
    """GET: Детальная информация об услуге через ORM"""
    contract = get_object_or_404(Contract, id=contract_id)
    
    return render(request, 'contract_detail.html', {
        'service': contract
    })

def cart(request, account_id):
    """GET: Страница заявки через ORM"""
    try:
        account = Account.objects.get(id=account_id)
        
        # Проверяем что заявка в статусе Draft и не удалена
        if account.status != 'DRAFT':
            # Если заявка не в статусе DRAFT (удалена или обработана) - редирект на главную
            return redirect('contracts_list')
        
    except Account.DoesNotExist:
        # Если заявка не существует - редирект на главную
        return redirect('contracts_list')
    
    # Получаем связи договоров с заявкой с информацией о основном договоре
    account_contracts = AccountContract.objects.filter(account_id=account_id).select_related('contract')
    
    # Подготавливаем данные для шаблона
    services_data = []
    for ac in account_contracts:
        services_data.append({
            'contract': ac.contract,
            'is_main_contract': ac.is_main_contract,
            'account_contract_id': ac.id  # ID связи для возможного обновления
        })
    
    return render(request, 'cart.html', {
        'application': account,
        'services_data': services_data,  # Меняем services на services_data
        'account_number': account.account_number
    })

def add_to_cart(request, contract_id):
    """Добавление услуги в заявку через ORM - обычный POST запрос"""
    if request.method == 'POST':
        # Временно: user_id = 1 для демо
        user_id = 1
        user = User.objects.get(id=user_id)
        
        # Получаем или создаем заявку через ORM
        draft_account = get_current_draft_account(user_id)
        if not draft_account:
            draft_account = Account.objects.create(
                status='DRAFT',
                created_by=user,
                updated_by=user
            )
        
        contract = get_object_or_404(Contract, id=contract_id)
        
        # Добавляем услугу в заявку через ORM
        account_contract, created = AccountContract.objects.get_or_create(
            account=draft_account,
            contract=contract,
            defaults={'is_main_contract': False}
        )
        
        # Перенаправляем обратно на список договоров
        return redirect('contracts_list')
    
    # Если GET запрос - просто перенаправляем на список
    return redirect('contracts_list')

@require_POST
def update_account_number(request, account_id):
    """POST: Сохранение номера счета через ORM"""
    account = get_object_or_404(Account, id=account_id)
    
    if account.status != 'DRAFT':
        return JsonResponse({'success': False, 'message': 'Заявка уже обработана'})
    
    data = json.loads(request.body)
    
    # Обновляем данные через ORM
    account.account_number = data.get('account_number')
    account.account_owner_code = data.get('account_owner_code')
    account.currency_code = data.get('currency_code')
    account.save()
    
    return JsonResponse({'success': True})

def delete_application(request, account_id):
    """POST: Удаление заявки через SQL UPDATE"""
    if request.method == 'POST':
        # Выполняем SQL UPDATE без ORM
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE account SET status = 'DELETED', completed_at = %s WHERE id = %s AND status = 'DRAFT'",
                [timezone.now(), account_id]
            )
            if cursor.rowcount == 0:
                # Если заявка не найдена или уже обработана - редирект на главную
                return redirect('contracts_list')
        
        return redirect('contracts_list')
    
    # GET запрос - показываем страницу заявки (но уже с проверками выше)
    return cart(request, account_id)