from django.shortcuts import render
from datetime import date
from django.http import JsonResponse
import random
import string
from django.conf import settings

def get_image_url(image_name):
    """Функция для получения правильного URL картинки из MinIO"""
    return f"http://localhost:9000/bankaccounts/{image_name}"

SERVICES = [
    {
        'id': 1,
        'number': 'Д-001', 
        'client': 'ООО "Центр кибернетической интеграции и облачных решений будущего"',
        'service_type': 'РКО',
        'image_url': "http://localhost:9000/bankaccounts/rko.png",
        'description': 'Расчетно-кассовое обслуживание для малого бизнеса',
        'start_date': '2024-01-15',
        'end_date': '2025-01-14',
        'status': 'Активен'

    },
    {
        'id': 2,
        'client': 'ИП Иванов А.С.',
        'number': 'Д-002', 
        'service_type': 'Зарплатный проект',
        'image_url': "http://localhost:9000/bankaccounts/salary.png",
        'description': 'Зарплатный проект для индивидуального предпринимателя',
        'start_date': '2024-02-01',
        'end_date': '2025-01-31', 
        'status': 'Активен'
    },
    {
        'id': 3, 
        'client': 'ОАО "Агентство стратегического планирования и трансформации бизнес-процессов"',
        'number': 'Д-003',
        'service_type': 'Эквайринг',
        'image_url': "http://localhost:9000/bankaccounts/acquiring.png",
        'description': 'Торговый эквайринг для розничной сети',
        'start_date': '2024-03-10',
        'end_date': '2025-03-09',
        'status': 'Активен'
    }
]

APPLICATION = {
    'id': 1,
    'account_number': '40702810123456789013',
    'services': [1, 2],
    'main_service_id': 1
}

def contracts_list(request):
    """Список всех услуг (договоров)"""
    return render(request, 'contracts_list.html', {
        'services': SERVICES,
        'cart_count': len(APPLICATION['services'])
    })

def contract_detail(request, contract_id):
    """Детальная информация об услуге (договоре)"""
    service = next((s for s in SERVICES if s['id'] == contract_id), None)
    
    if not service:
        return render(request, '404.html', status=404)
    
    return render(request, 'contract_detail.html', {
        'service': service
    })

def cart(request, application_id):
    """Страница заявки"""
    if application_id != APPLICATION['id']:
        return render(request, '404.html', status=404)
    
    # Получаем услуги, которые входят в заявку
    application_services = [s for s in SERVICES if s['id'] in APPLICATION['services']]
    
    return render(request, 'cart.html', {
        'application': APPLICATION,
        'services': application_services,
        'all_services': SERVICES
    })
