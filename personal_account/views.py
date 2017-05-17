from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    return render(request, 'home.html', {
        'new_income_category': request.POST.get('income_category', ''),
        'new_income_amount': request.POST.get('income_amount', ''),
        'new_expense_category': request.POST.get('expense_category', ''),
        'new_expense_amount': request.POST.get('expense_amount', ''),
        'total_expenses': request.POST.get('expense_amount', ''),
        'account_balance': request.POST.get('income_amount', ''),

        })
