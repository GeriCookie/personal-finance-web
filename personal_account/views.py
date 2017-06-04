from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from utils import datehelper

from models.models import Balance, Category


def home_page(request):
    return render(request, 'home.html')


@login_required
def view_balance(request):
    balance = request.user.balance
    return render(request, 'balance.html', {
        'balance': balance,
    })


@login_required
def income(request):
    balance = request.user.balance
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


@login_required
def daily_income(request, date):
    balance = request.user.balance
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


@login_required
def weekly_income(request, start_date, end_date):
    balance = request.user.balance
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


@login_required
def montly_income(request, start_date, end_date):
    balance = request.user.balance
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


@login_required
def yearly_income(request, start_date, end_date):
    balance = request.user.balance
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


@login_required
def expenses(request):
    balance = request.user.balance
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


@login_required
def daily_expenses(request, date):
    balance = request.user.balance
    expenses = balance.expenses.by_day(date).amount_per_category()
    total_expenses = expenses.total_amount()
    days = datehelper.days_income_expense_daily_view(date)
    return render(request, 'expenses_daily.html', {
        'balance': balance,
        'expenses': expenses,
        'days': days,
        'total_expenses': total_expenses
    })


@login_required
def weekly_expenses(request, start_date, end_date):
    balance = request.user.balance
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


@login_required
def montly_expenses(request, start_date, end_date):
    balance = request.user.balance
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


@login_required
def yearly_expenses(request, start_date, end_date):
    balance = request.user.balance
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
