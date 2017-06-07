from django.db import models
from decimal import Decimal
from django.db.models import Sum, F, Min
from utils import datehelper as helper
from math import ceil
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User

from django.utils import timezone


class CategoryManager(models.Manager):

    def create_category(self, category_name):
        category = Category.objects.filter(name=category_name).first()
        if not category:
            category = Category.objects.create(name=category_name)
        return category


class BalanceManager(models.Manager):


    def create_income(self, **kwargs):
        category = kwargs.get('category')
        amount = kwargs.get('amount')
        date = kwargs.get('date')
        if type(date) is str:
            date = helper.from_str_to_date(date, '%m/%d/%Y')
        balance = kwargs.get('balance')
        income = Income.objects.create(
                category=category,
                amount=amount,
                date=date,
                balance=balance,
                date_created=helper.today()
                )
        balance.total_income += Decimal(amount)
        self.calculate_balance_values(balance)
        balance.save()
        return income

    def create_expense(self, **kwargs):
        category = kwargs.get('category')
        amount = kwargs.get('amount')
        date = kwargs.get('date')
        if type(date) is str:
            date = helper.from_str_to_date(date, '%m/%d/%Y')
        balance = kwargs.get('balance')
        expense = Expense.objects.create(
                category=category,
                amount=amount,
                date=date,
                balance=balance,
                date_created=helper.today()
                )
        balance.total_expense += Decimal(amount)
        budget = balance.budget.filter(completed=False).last()
        if budget:
            if budget.date_created <= date:
                balance.remaining_budget -= Decimal(amount)
        self.calculate_balance_values(balance)
        balance.save()
        return expense

    def create_savings_goal(self, **kwargs):
        amount = kwargs.get('amount')
        date = kwargs.get('end_date')
        if type(date) is str:
            date = helper.from_str_to_date(date, '%m/%d/%Y')
        balance = kwargs.get('balance')
        savings_goal = SavingsGoal.objects.create(
                amount=amount,
                end_date=date,
                balance=balance,
                date_created=helper.today()
                )
        self.calculate_balance_values(balance)
        balance.save()
        return savings_goal

    def create_budget(self, **kwargs):
        amount = kwargs.get('amount')
        date = kwargs.get('end_date')
        if type(date) is str:
            date = helper.from_str_to_date(date, '%m/%d/%Y')
        balance = kwargs.get('balance')
        budget = Budget.objects.create(
                amount=amount,
                end_date=date,
                balance=balance,
                date_created=helper.today()
                )
        balance.remaining_budget = Decimal(amount)
        self.calculate_balance_values(balance)
        balance.save()
        return budget

    def calculate_balance_values(self, balance):
        savings_goal = balance.savings_goals.filter(completed=False).last()
        budget = balance.budget.filter(completed=False).last()
        if savings_goal and budget:
            days_by_end_goal_date = savings_goal.end_date - helper.today()
            if savings_goal.end_date < budget.end_date:
                if savings_goal.end_date == helper.today():
                    if balance.remaining_budget > savings_goal:
                        balance.remaining_budget - savings_goal.amount
                        balance.total_savings += savings_goal.amount
                        savings_goal.completed = True
                else:
                    balance.recommended_expenses_per_day = (
                        balance.remaining_budget / days_by_end_goal_date)
            elif savings_goal.end_date > budget.end_date:
                if budget.end_date == helper.today():
                    if balance.remaining_budget >= 0:
                        budget.completed = True
                else:
                    savings_per_day = (
                            savings_goal.amount / days_by_end_goal_date.days)
                    balance.target_savings_budget_end = savings_per_day * (
                            (budget.end_date - helper.today()).days)
                    balance.recommended_expenses_per_day = (
                        balance.remaining_budget -
                        balance.target_savings_budget_end)/(
                                    (budget.end_date - helper.today()).days)
            else:
                if budget.end_date == helper.today() and \
                        savings_goal.end_date == helper.today():
                    if balance.remaining_budget >= savings_goal.amount:
                        savings_goal.completed = True
                        balance.remaining_budget -= savings_goal.amount
                        balance.total_savings += savings_goal.amount
                        if balance.remaining_budget >= 0:
                            budget.completed = True
                else:
                    balance.recommended_expenses_per_day = (
                        balance.remaining_budget - savings_goal.amount) / (
                            (budget.end_date - helper.today()).days)
        elif savings_goal and not budget:
            end_date = savings_goal.end_date
            days_by_end_goal_date = (end_date - helper.today()).days
            savings_amount = savings_goal.amount

            if end_date == helper.today():
                if balance.total_amount >= savings_amount:
                    savings_goal.completed = True
                    savings_goal.save()
                    balance.total_savings += savings_amount
            else:
                balance.recommended_expenses_per_day = (
                    balance.total_amount -
                    savings_goal.amount)/days_by_end_goal_date
        elif budget and not savings_goal:
            if budget.end_date == helper.today():
                if balance.remaining_budget >= 0:
                    budget.completed = True
            else:
                balance.recommended_expenses_per_day = (
                    balance.remaining_budget / (budget.end_date - helper.today().days))

        balance.total_amount = balance.total_income - (
                balance.total_expense -
                balance.total_savings)
        if savings_goal and budget:
            if savings_goal.completed and budget.completed:
                balance.recommended_expenses_per_day = 0.00
        if balance.expenses.first() and balance.expenses.first().date != helper.today():
            balance.average_expenses_per_day = balance.expenses.total_amount()['total_amount'] / (
                (helper.today() -
                    balance.expenses.aggregate(min_date=Min(F('date')))['min_date']).days)
            balance.end_date_available_funds = timedelta(days=ceil(
                balance.total_amount / balance.average_expenses_per_day)) + helper.today()


class FilterQuerySet(models.QuerySet):

    def by_day(self, day):
        if type(day) is str:
            day = helper.from_str_to_date(day, '%Y-%m-%d')
        return self.filter(date=day)

    def date_range(self, start_date, end_date):
        if type(start_date) is str:
            start_date = helper.from_str_to_date(start_date, '%Y-%m-%d')
        if type(end_date) is str:
            end_date = helper.from_str_to_date(end_date, '%Y-%m-%d')
        return self.filter(date__range=[start_date, end_date])

    def amount_per_category(self):
        return self.values(
                'category__name').annotate(amount_per_category=Sum('amount'))

    def total_amount(self):
        return self.aggregate(total_amount=Sum(F('amount')))


class Balance(models.Model):
    total_income = models.DecimalField(
            max_digits=19,
            decimal_places=2,
            default=Decimal(0.00)
            )
    total_expense = models.DecimalField(
            max_digits=19,
            decimal_places=2,
            default=Decimal(0.00)
            )
    total_amount = models.DecimalField(
            max_digits=19,
            decimal_places=2,
            default=Decimal(0.00)
            )
    recommended_expenses_per_day = models.DecimalField(
            max_digits=19,
            decimal_places=2,
            default=Decimal(0.00)
            )
    target_savings_budget_end = models.DecimalField(
            max_digits=19,
            decimal_places=2,
            default=Decimal(0.00)
            )
    total_savings = models.DecimalField(
            max_digits=19,
            decimal_places=2,
            default=Decimal(0.00)
            )
    remaining_budget = models.DecimalField(
            max_digits=19,
            decimal_places=2,
            default=Decimal(0.00)
            )
    average_expenses_per_day = models.DecimalField(
            max_digits=19,
            decimal_places=2,
            default=Decimal(0.00)
            )
    end_date_available_funds = models.DateField(default=timezone.now)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    date_created = models.DateField(default=timezone.now)
    objects = BalanceManager()

    class Meta(object):
        app_label = 'personal_finance'


@receiver(post_save, sender=User)
def create_user_balance(sender, instance, created, **kwargs):
    if created:
        Balance.objects.create(owner=instance)


@receiver(post_save, sender=User)
def save_user_balance(sender, instance, **kwargs):
    instance.balance.save()


class Category(models.Model):

    class Meta(object):
        app_label = 'personal_finance'

    name = models.CharField(max_length=300, unique=True)

    objects = CategoryManager()


class Income(models.Model):

    class Meta(object):
        app_label = 'personal_finance'

    balance = models.ForeignKey(
            Balance,
            default=None,
            on_delete=models.CASCADE,
            related_name='incomes'
            )
    category = models.ForeignKey(
            Category,
            default=None,
            on_delete=models.CASCADE
            )
    amount = models.DecimalField(
            max_digits=19,
            decimal_places=2,
            default=Decimal('0.00')
            )
    date = models.DateField()
    date_created = models.DateField(default=timezone.now)
    objects = FilterQuerySet.as_manager()


class Expense(models.Model):

    class Meta(object):
        app_label = 'personal_finance'

    balance = models.ForeignKey(
            Balance,
            default=None,
            on_delete=models.CASCADE,
            related_name='expenses'
            )
    category = models.ForeignKey(
            Category,
            default=None,
            on_delete=models.CASCADE
            )
    amount = models.DecimalField(
            max_digits=19,
            decimal_places=2,
            default=Decimal('0.00')
            )
    date = models.DateField()
    date_created = models.DateField(default=timezone.now)
    objects = FilterQuerySet.as_manager()


class SavingsGoal(models.Model):

    class Meta(object):
        app_label = 'personal_finance'

    balance = models.ForeignKey(
            Balance,
            default=None,
            on_delete=models.CASCADE,
            related_name='savings_goals'
            )
    amount = models.DecimalField(
            max_digits=19,
            decimal_places=2,
            default=Decimal('0.00')
            )
    end_date = models.DateField()
    date_created = models.DateField(default=timezone.now)
    completed = models.BooleanField(default=False)


class Budget(models.Model):

    class Meta(object):
        app_label = 'personal_finance'

    balance = models.ForeignKey(
            Balance,
            default=None,
            on_delete=models.CASCADE,
            related_name='budget'
            )
    amount = models.DecimalField(
            max_digits=19,
            decimal_places=2,
            default=Decimal('0.00')
            )
    end_date = models.DateField()
    date_created = models.DateField(timezone.now)
    completed = models.BooleanField(default=False)
