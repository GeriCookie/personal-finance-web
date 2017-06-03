from django.shortcuts import redirect, render
from personal_account.models import Balance, Category
from utils import datehelper


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
    new_income_date = request.POST.get('income_date', '')
    category = Category.objects.create_category(new_income_category)
    Balance.objects.create_income(
            category=category,
            amount=new_income_amount,
            date=new_income_date,
            balance=balance
    )

    return redirect(f'/balance/{balance.id}/income/')


def income(request, balance_id):
    balance = Balance.objects.get(id=balance_id)
    incomes = balance.incomes.all().select_related('category')
    days = datehelper.days_income_expense_view()
    if request.method == 'POST':
        category_name = request.POST.get('income_category', '')
        amount = request.POST.get('income_amount', '')
        date = request.POST.get('income_date', '')
        category = Category.objects.create_category(category_name)
        Balance.objects.create_income(
                category=category,
                amount=amount,
                date=date,
                balance=balance
        )
        return redirect(f'/balance/{balance.id}/income/')
    return render(request, 'income.html', {
            'balance': balance,
            'incomes': incomes,
            'days': days
            })


def daily_income(request, balance_id, date):
    balance = Balance.objects.get(id=balance_id)
    incomes = balance.incomes.by_day(
                date).amount_per_category()
    total_income = incomes.total_amount()
    days = datehelper.days_income_expense_daily_view(date)
    return render(request, 'income_daily.html', {
        'balance': balance,
        'incomes': incomes,
        'days': days,
        'total_income': total_income
    })


def weekly_income(request, balance_id, start_date, end_date):
    balance = Balance.objects.get(id=balance_id)
    incomes = balance.incomes.date_range(
            start_date, end_date).amount_per_category()
    total_income = incomes.total_amount()
    days = datehelper.days_income_expense_weekly_view(start_date, end_date)
    return render(request, 'income_weekly.html', {
        'balance': balance,
        'incomes': incomes,
        'days': days,
        'total_income': total_income
    })


def montly_income(request, balance_id, start_date, end_date):
    balance = Balance.objects.get(id=balance_id)
    incomes = balance.incomes.date_range(
            start_date, end_date).amount_per_category()
    total_income = incomes.total_amount()
    days = datehelper.days_income_expense_monthly_view(start_date, end_date)
    return render(request, 'income_monthly.html', {
        'balance': balance,
        'incomes': incomes,
        'days': days,
        'total_income': total_income
    })


def yearly_income(request, balance_id, start_date, end_date):
    balance = Balance.objects.get(id=balance_id)
    incomes = balance.incomes.date_range(
            start_date, end_date).amount_per_category()
    total_income = incomes.total_amount()
    days = datehelper.days_income_expense_yearly_view(start_date, end_date)
    return render(request, 'income_yearly.html', {
        'balance': balance,
        'incomes': incomes,
        'days': days,
        'total_income': total_income
    })


def expenses(request, balance_id):
    balance = Balance.objects.get(id=balance_id)
    expenses = balance.expenses.all().select_related('category')
    days = datehelper.days_income_expense_view()
    if request.method == 'POST':
        category_name = request.POST.get('expense_category', '')
        amount = request.POST.get('expense_amount', '')
        date = request.POST.get('expense_date', '')
        category = Category.objects.create_category(category_name)
        Balance.objects.create_expense(
                category=category,
                amount=amount,
                date=date,
                balance=balance
        )
        return redirect(f'/balance/{balance.id}/expenses/')
    return render(request, 'expenses.html', {
            'balance': balance,
            'expenses': expenses,
            'days': days
        })


def daily_expenses(request, balance_id, date):
    balance = Balance.objects.get(id=balance_id)
    expenses = balance.expenses.by_day(date).amount_per_category()
    total_expenses = expenses.total_amount()
    days = datehelper.days_income_expense_daily_view(date)
    return render(request, 'expenses_daily.html', {
        'balance': balance,
        'expenses': expenses,
        'days': days,
        'total_expenses': total_expenses
    })


def weekly_expenses(request, balance_id, start_date, end_date):
    balance = Balance.objects.get(id=balance_id)
    expenses = balance.expenses.date_range(
            start_date, end_date).amount_per_category()
    total_expenses = expenses.total_amount()
    days = datehelper.days_income_expense_weekly_view(start_date, end_date)
    return render(request, 'expenses_weekly.html', {
        'balance': balance,
        'expenses': expenses,
        'days': days,
        'total_expenses': total_expenses
    })


def montly_expenses(request, balance_id, start_date, end_date):
    balance = Balance.objects.get(id=balance_id)
    expenses = balance.expenses.date_range(
            start_date, end_date).amount_per_category()
    total_expenses = expenses.total_amount()
    days = datehelper.days_income_expense_monthly_view(start_date, end_date)
    return render(request, 'expenses_monthly.html', {
        'balance': balance,
        'expenses': expenses,
        'days': days,
        'total_expenses': total_expenses
    })


def yearly_expenses(request, balance_id, start_date, end_date):
    balance = Balance.objects.get(id=balance_id)
    expenses = balance.expenses.date_range(
            start_date, end_date).amount_per_category()
    total_expenses = expenses.total_amount()
    days = datehelper.days_income_expense_yearly_view(start_date, end_date)
    return render(request, 'expenses_yearly.html', {
        'balance': balance,
        'expenses': expenses,
        'days': days,
        'total_expenses': total_expenses
    })
