from django.db import models
from decimal import Decimal
from django.db.models import Sum, F
from utils import datehelper as helper

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User


class CategoryManager(models.Manager):

    def create_category(self, category_name):
        category = Category.objects.filter(name=category_name).first()
        if not category:
            category = Category.objects.create(name=category_name)
        return category


class BalanceQuerySet(models.QuerySet):

    def get_incomes(self, balance_id):
        return self.get(id=balance_id).incomes.all()

    def get_expenses(self, balance_id):
        return self.get(id=balance_id).expenses.all()


class BalanceManager(models.Manager):

    def get_queryset(self):
        return BalanceQuerySet(self.model, using=self._db)

    def get_incomes(self, balance_id):
        return self.get_queryset().get_incomes(balance_id)

    def get_expenses(self, balance_id):
        return self.get_queryset().get_expenses(balance_id)

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
                balance=balance
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
                balance=balance
                )
        balance.total_expense += Decimal(amount)
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
                balance=balance
                )
        self.calculate_balance_values(balance)
        balance.save()
        return savings_goal

    def calculate_balance_values(self, balance):
        savings_goal = balance.savings_goals.filter(completed=False).first()
        days_by_end_goal_date = 1
        savings_amount = 0
        today = helper.today()
        if savings_goal:
            end_date = savings_goal.end_date
            days_by_end_goal_date = (end_date - today).days
            savings_amount = savings_goal.amount

            if end_date == today:
                if balance.total_amount >= savings_amount:
                    savings_goal.completed = True
                    savings_goal.save()
                    balance.total_savings += savings_amount
        balance.total_amount = balance.total_income - (
                balance.total_expense -
                balance.total_savings)
        if savings_goal and end_date != today:
            balance.recommended_expenses_per_day = (
                    balance.total_amount -
                    savings_amount) / days_by_end_goal_date


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
    target_savings_month_end = models.DecimalField(
            max_digits=19,
            decimal_places=2,
            default=Decimal(0.00)
            )
    total_savings = models.DecimalField(
            max_digits=19,
            decimal_places=2,
            default=Decimal(0.00)
            )
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    objects = BalanceManager()


@receiver(post_save, sender=User)
def create_user_balance(sender, instance, created, **kwargs):
    if created:
        Balance.objects.create(owner=instance)


@receiver(post_save, sender=User)
def save_user_balance(sender, instance, **kwargs):
    instance.balance.save()


class Category(models.Model):
    name = models.CharField(max_length=300, unique=True)

    objects = CategoryManager()


class Income(models.Model):
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
    objects = FilterQuerySet.as_manager()


class Expense(models.Model):
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
    objects = FilterQuerySet.as_manager()


class SavingsGoal(models.Model):
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
    completed = models.BooleanField(default=False)
