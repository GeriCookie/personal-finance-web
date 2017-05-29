from django.shortcuts import redirect, render
from personal_account.models import Income, Expense, Balance, Category
from datetime import datetime, timedelta
from datetime import date as new_date
from django.db.models import F, Sum
from calendar import monthrange


def home_page(request):
    return render(request, 'home.html')


def view_balance(request, balance_id):
    balance = Balance.objects.get(id=balance_id)
    return render(request, 'balance.html', {
        'balance': balance,
        'count': 5
    })


def new_balance(request):
    balance = Balance.objects.create()
    new_income_category = request.POST.get('income_category', '')
    new_income_amount = request.POST.get('income_amount', '')
    new_income_date = request.POST.get('income_date', '')
    category = Category.objects.filter(name=new_income_category).first()
    if not category:
        category = Category.objects.create(name=new_income_category)
    Income.objects.create(
            category=category,
            amount=new_income_amount,
            date=datetime.strptime(new_income_date, '%m/%d/%Y'),
            balance=balance
    )
    balance.save(income_added=True)

    return redirect(f'/balance/{balance.id}/income/')


def income(request, balance_id):
    balance = Balance.objects.get(id=balance_id)
    days = {}
    days['today'] = datetime.strftime(datetime.today(), '%Y-%m-%d')
    start_week = datetime.today() - timedelta(days=datetime.today().weekday())
    end_week = start_week + timedelta(days=6)
    days['start_week'] = datetime.strftime(start_week, '%Y-%m-%d')
    days['end_week'] = datetime.strftime(end_week, '%Y-%m-%d')
    monthdays = monthrange(datetime.today().year, datetime.today().month)
    start_month_date = new_date(
            datetime.today().year,
            datetime.today().month,
            1)
    end_month_date = new_date(
            datetime.today().year,
            datetime.today().month,
            monthdays[1]
    )
    days['start_month'] = datetime.strftime(start_month_date, '%Y-%m-%d')
    days['end_month'] = datetime.strftime(end_month_date, '%Y-%m-%d')
    start_year = new_date(datetime.today().year, 1, 1)
    end_year = new_date(datetime.today().year, 12, 31)
    days['start_year'] = datetime.strftime(start_year, '%Y-%m-%d')
    days['end_year'] = datetime.strftime(end_year, '%Y-%m-%d')
    if request.method == 'POST':
        category_name = request.POST.get('income_category', '')
        amount = request.POST.get('income_amount', '')
        date = request.POST.get('income_date', '')
        category = Category.objects.filter(name=category_name).first()
        if not category:
            category = Category.objects.create(name=category_name)
        Income.objects.create(
                category=category,
                amount=amount,
                date=datetime.strptime(date, '%m/%d/%Y'),
                balance=balance
        )
        balance.save(income_added=True)
        return redirect(f'/balance/{balance.id}/income/')
    return render(request, 'income.html', {
            'balance': balance,
            'days': days
            })


def daily_income(request, balance_id, date):
    balance = Balance.objects.get(id=balance_id)
    date = datetime.strptime(date, '%Y-%m-%d')
    incomes = balance.incomes.filter(date=date).values(
            'category__name').annotate(amount_per_category=Sum('amount'))
    total_income = incomes.aggregate(total_income=Sum(F('amount')))
    days = {}
    days['current_day'] = datetime.strftime(date, '%d %b %Y')
    days['prev_day'] = datetime.strftime(date - timedelta(days=1), '%Y-%m-%d')
    days['next_day'] = datetime.strftime(date + timedelta(days=1), '%Y-%m-%d')
    return render(request, 'income_daily.html', {
        'balance': balance,
        'incomes': incomes,
        'days': days,
        'total_income': total_income
    })


def weekly_income(request, balance_id, start_date, end_date):
    balance = Balance.objects.get(id=balance_id)
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    incomes = balance.incomes.filter(
            date__range=[start_date, end_date]).values(
            'category__name').annotate(amount_per_category=Sum('amount'))
    total_income = incomes.aggregate(total_income=Sum(F('amount')))
    days = {}

    days['current_week_start'] = datetime.strftime(
            start_date, '%d %b %Y'
    )
    days['current_week_end'] = datetime.strftime(
            end_date, '%d %b %Y'
    )
    days['prev_week_end'] = datetime.strftime(
            start_date - timedelta(days=1), '%Y-%m-%d'
    )
    days['prev_week_start'] = datetime.strftime(
            start_date - timedelta(days=7), '%Y-%m-%d'
    )
    days['next_week_start'] = datetime.strftime(
            end_date + timedelta(days=1), '%Y-%m-%d'
    )
    days['next_week_end'] = datetime.strftime(
            end_date + timedelta(days=7), '%Y-%m-%d'
    )
    return render(request, 'income_weekly.html', {
        'balance': balance,
        'incomes': incomes,
        'days': days,
        'total_income': total_income
    })


def montly_income(request, balance_id, start_date, end_date):
    balance = Balance.objects.get(id=balance_id)
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    incomes = balance.incomes.filter(
            date__range=[start_date, end_date]).values(
            'category__name').annotate(amount_per_category=Sum('amount'))
    total_income = incomes.aggregate(total_income=Sum(F('amount')))
    days = {}

    days['current_month_start'] = datetime.strftime(
            start_date, '%d %b %Y'
    )
    days['current_month_end'] = datetime.strftime(
            end_date, '%d %b %Y'
    )
    prev_month_end_date = start_date - timedelta(days=1)
    days['prev_month_end'] = datetime.strftime(
            prev_month_end_date, '%Y-%m-%d'
    )
    prev_month_days = monthrange(
            prev_month_end_date.year,
            prev_month_end_date.month)
    days['prev_month_start'] = datetime.strftime(
            start_date - timedelta(days=prev_month_days[1]), '%Y-%m-%d'
    )
    next_month_start_date = end_date + timedelta(days=1)
    days['next_month_start'] = datetime.strftime(
            next_month_start_date, '%Y-%m-%d'
    )
    next_month_days = monthrange(
            next_month_start_date.year,
            next_month_start_date.month)
    days['next_month_end'] = datetime.strftime(
            end_date + timedelta(days=next_month_days[1]), '%Y-%m-%d'
    )
    return render(request, 'income_monthly.html', {
        'balance': balance,
        'incomes': incomes,
        'days': days,
        'total_income': total_income
    })


def yearly_income(request, balance_id, start_date, end_date):
    balance = Balance.objects.get(id=balance_id)
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    incomes = balance.incomes.filter(
            date__range=[start_date, end_date]).values(
            'category__name').annotate(amount_per_category=Sum('amount'))
    total_income = incomes.aggregate(total_income=Sum(F('amount')))
    days = {}

    days['current_year_start'] = datetime.strftime(
            start_date, '%d %b %Y'
    )
    days['current_year_end'] = datetime.strftime(
            end_date, '%d %b %Y'
    )
    prev_year_end_date = start_date - timedelta(days=1)
    days['prev_year_end'] = datetime.strftime(
            prev_year_end_date, '%Y-%m-%d'
    )
    days['prev_year_start'] = datetime.strftime(
            new_date(prev_year_end_date.year, 1, 1), '%Y-%m-%d'
    )
    next_year_start_date = end_date + timedelta(days=1)
    days['next_year_start'] = datetime.strftime(
            next_year_start_date, '%Y-%m-%d'
    )
    days['next_year_end'] = datetime.strftime(
            new_date(next_year_start_date.year, 12, 31), '%Y-%m-%d'
    )
    return render(request, 'income_yearly.html', {
        'balance': balance,
        'incomes': incomes,
        'days': days,
        'total_income': total_income
    })


def expenses(request, balance_id):
    balance = Balance.objects.get(id=balance_id)
    days = {}
    days['today'] = datetime.strftime(datetime.today(), '%Y-%m-%d')
    start_week = datetime.today() - timedelta(days=datetime.today().weekday())
    end_week = start_week + timedelta(days=6)
    days['start_week'] = datetime.strftime(start_week, '%Y-%m-%d')
    days['end_week'] = datetime.strftime(end_week, '%Y-%m-%d')
    monthdays = monthrange(datetime.today().year, datetime.today().month)
    start_month_date = new_date(
            datetime.today().year,
            datetime.today().month,
            1)
    end_month_date = new_date(
            datetime.today().year,
            datetime.today().month,
            monthdays[1]
    )
    days['start_month'] = datetime.strftime(start_month_date, '%Y-%m-%d')
    days['end_month'] = datetime.strftime(end_month_date, '%Y-%m-%d')
    start_year = new_date(datetime.today().year, 1, 1)
    end_year = new_date(datetime.today().year, 12, 31)
    days['start_year'] = datetime.strftime(start_year, '%Y-%m-%d')
    days['end_year'] = datetime.strftime(end_year, '%Y-%m-%d')
    if request.method == 'POST':
        category_name = request.POST.get('expense_category', '')
        amount = request.POST.get('expense_amount', '')
        date = request.POST.get('expense_date', '')
        category = Category.objects.filter(name=category_name).first()
        if not category:
            category = Category.objects.create(name=category_name)
        Expense.objects.create(
                category=category,
                amount=amount,
                date=datetime.strptime(date, '%m/%d/%Y'),
                balance=balance
        )
        balance.save(expense_added=True)
        return redirect(f'/balance/{balance.id}/expenses/')
    return render(request, 'expenses.html', {
            'balance': balance,
            'days': days
        })


def daily_expenses(request, balance_id, date):
    balance = Balance.objects.get(id=balance_id)
    date = datetime.strptime(date, '%Y-%m-%d')
    expenses = balance.expenses.filter(date=date).values(
            'category__name').annotate(amount_per_category=Sum('amount'))
    total_expenses = expenses.aggregate(total_expenses=Sum(F('amount')))
    days = {}
    days['current_day'] = datetime.strftime(date, '%d %b %Y')
    days['prev_day'] = datetime.strftime(date - timedelta(days=1), '%Y-%m-%d')
    days['next_day'] = datetime.strftime(date + timedelta(days=1), '%Y-%m-%d')
    return render(request, 'expenses_daily.html', {
        'balance': balance,
        'expenses': expenses,
        'days': days,
        'total_expenses': total_expenses
    })


def weekly_expenses(request, balance_id, start_date, end_date):
    balance = Balance.objects.get(id=balance_id)
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    expenses = balance.expenses.filter(
            date__range=[start_date, end_date]).values(
            'category__name').annotate(amount_per_category=Sum('amount'))
    total_expenses = expenses.aggregate(total_expenses=Sum(F('amount')))
    days = {}

    days['current_week_start'] = datetime.strftime(
            start_date, '%d %b %Y'
    )
    days['current_week_end'] = datetime.strftime(
            end_date, '%d %b %Y'
    )
    days['prev_week_end'] = datetime.strftime(
            start_date - timedelta(days=1), '%Y-%m-%d'
    )
    days['prev_week_start'] = datetime.strftime(
            start_date - timedelta(days=7), '%Y-%m-%d'
    )
    days['next_week_start'] = datetime.strftime(
            end_date + timedelta(days=1), '%Y-%m-%d'
    )
    days['next_week_end'] = datetime.strftime(
            end_date + timedelta(days=7), '%Y-%m-%d'
    )
    return render(request, 'expenses_weekly.html', {
        'balance': balance,
        'expenses': expenses,
        'days': days,
        'total_expenses': total_expenses
    })


def montly_expenses(request, balance_id, start_date, end_date):
    balance = Balance.objects.get(id=balance_id)
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    expenses = balance.expenses.filter(
            date__range=[start_date, end_date]).values(
            'category__name').annotate(amount_per_category=Sum('amount'))
    total_expenses = expenses.aggregate(total_expenses=Sum(F('amount')))
    days = {}

    days['current_month_start'] = datetime.strftime(
            start_date, '%d %b %Y'
    )
    days['current_month_end'] = datetime.strftime(
            end_date, '%d %b %Y'
    )
    prev_month_end_date = start_date - timedelta(days=1)
    days['prev_month_end'] = datetime.strftime(
            prev_month_end_date, '%Y-%m-%d'
    )
    prev_month_days = monthrange(
            prev_month_end_date.year,
            prev_month_end_date.month)
    days['prev_month_start'] = datetime.strftime(
            start_date - timedelta(days=prev_month_days[1]), '%Y-%m-%d'
    )
    next_month_start_date = end_date + timedelta(days=1)
    days['next_month_start'] = datetime.strftime(
            next_month_start_date, '%Y-%m-%d'
    )
    next_month_days = monthrange(
            next_month_start_date.year,
            next_month_start_date.month)
    days['next_month_end'] = datetime.strftime(
            end_date + timedelta(days=next_month_days[1]), '%Y-%m-%d'
    )
    return render(request, 'expenses_monthly.html', {
        'balance': balance,
        'expenses': expenses,
        'days': days,
        'total_expenses': total_expenses
    })


def yearly_expenses(request, balance_id, start_date, end_date):
    balance = Balance.objects.get(id=balance_id)
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    expenses = balance.expenses.filter(
            date__range=[start_date, end_date]).values(
            'category__name').annotate(amount_per_category=Sum('amount'))
    total_expenses = expenses.aggregate(total_expenses=Sum(F('amount')))
    days = {}

    days['current_year_start'] = datetime.strftime(
            start_date, '%d %b %Y'
    )
    days['current_year_end'] = datetime.strftime(
            end_date, '%d %b %Y'
    )
    prev_year_end_date = start_date - timedelta(days=1)
    days['prev_year_end'] = datetime.strftime(
            prev_year_end_date, '%Y-%m-%d'
    )
    days['prev_year_start'] = datetime.strftime(
            new_date(prev_year_end_date.year, 1, 1), '%Y-%m-%d'
    )
    next_year_start_date = end_date + timedelta(days=1)
    days['next_year_start'] = datetime.strftime(
            next_year_start_date, '%Y-%m-%d'
    )
    days['next_year_end'] = datetime.strftime(
            new_date(next_year_start_date.year, 12, 31), '%Y-%m-%d'
    )
    return render(request, 'expenses_yearly.html', {
        'balance': balance,
        'expenses': expenses,
        'days': days,
        'total_expenses': total_expenses
    })
