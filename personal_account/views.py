from django.shortcuts import redirect, render
from personal_account.models import Income, Expense, Balance


def home_page(request):
    return render(request, 'home.html')


def view_balance(request, balance_id):
    balance = Balance.objects.get(id=balance_id)
    return render(request, 'balance.html', {
        'balance': balance,
    })


def new_balance(request):
    balance = Balance.objects.create()
    new_income_category = request.POST.get('income_category', '')
    new_income_amount = request.POST.get('income_amount', '')
    Income.objects.create(
            category=new_income_category,
            amount=new_income_amount,
            balance=balance
    )
    balance.save(income_added=True)

    return redirect(f'/balance/{balance.id}/')


def add_income(request, balance_id):
    balance = Balance.objects.get(id=balance_id)
    if request.method == 'POST':
        category = request.POST.get('income_category', '')
        amount = request.POST.get('income_amount', '')
        Income.objects.create(
                category=category,
                amount=amount,
                balance=balance
        )
        balance.save(income_added=True)
        return redirect(f'/balance/{balance.id}/')
    return render(request, 'add_income.html', {
            'balance': balance
            })


def add_expense(request, balance_id):
    balance = Balance.objects.get(id=balance_id)
    if request.method == 'POST':
        category = request.POST.get('expense_category', '')
        amount = request.POST.get('expense_amount', '')
        Expense.objects.create(
                category=category,
                amount=amount,
                balance=balance
        )
        balance.save(expense_added=True)
        return redirect(f'/balance/{balance.id}/')
    return render(request, 'add_expense.html', {
            'balance': balance
        })
