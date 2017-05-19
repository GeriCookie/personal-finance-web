from django.shortcuts import redirect, render
from personal_account.models import Income, Expense, Balance


def home_page(request):
    return render(request, 'home.html')


def view_balance(request):
    incomes = Income.objects.all()
    expenses = Expense.objects.all()
    return render(request, 'balance.html', {
        'incomes': incomes,
        'expenses': expenses
    })


def new_balance(request):
    balance = Balance.objects.create()
    new_income_category = request.POST.get('income_category', '')
    new_income_amount = request.POST.get('income_amount', '')
    new_expense_category = request.POST.get('expense_category', '')
    new_expense_amount = request.POST.get('expense_amount', '')
    if new_income_category and new_income_amount:
        Income.objects.create(
                category=new_income_category,
                amount=new_income_amount,
                balance=balance
        )

    if new_expense_category and new_expense_amount:
        Expense.objects.create(
                category=new_expense_category,
                amount=new_expense_amount,
                balance=balance
        )
    return redirect('/personal_account/the-only-balance-in-the-world/')
