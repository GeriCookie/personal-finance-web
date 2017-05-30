from django.db import models
from decimal import Decimal
from calendar import monthrange
from datetime import date


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

    def save(self, *args, **kwargs):
        income_added = kwargs.pop('income_added', '')
        expense_added = kwargs.pop('expense_added', '')
        savings_goal_added = kwargs.pop('savings_goal_added', '')
        today = date.today()
        savings_goal = self.savings_goals.filter(completed=False).first()
        days_by_end_goal_date = 1
        days_by_the_end_of_the_month = monthrange(today.year,
                    today.month)[1] - today.day
        savings_amount = 0
        if savings_goal:
            end_date = savings_goal.end_date
            days_by_end_goal_date = (end_date - today).days
            if days_by_end_goal_date == 0:
                days_by_end_goal_date = 1
            savings_amount = savings_goal.amount

            if end_date == today:
                if self.total_amount >= savings_amount:
                    savings_goal.completed = True
                    savings_goal.save()
                    self.total_savings = self.total_savings + savings_amount
                    savings_amount = 0


        if income_added:
            self.total_income = self.total_income + \
                    self.incomes.last().amount

        if expense_added:
            self.total_expense = self.total_expense + \
                    self.expenses.last().amount

        if savings_goal_added:
            savings_goal = self.savings_goals.first()
            total_days = savings_goal.end_date - today
            if total_days:
                savings_per_day = savings_goal.amount/total_days.days
                self.target_savings_month_end = savings_per_day * days_by_the_end_of_the_month
        
        self.total_amount = self.total_income - self.total_expense - self.total_savings
        self.recommended_expenses_per_day = (self.total_amount -
                self.target_savings_month_end) / days_by_the_end_of_the_month

        super(Balance, self).save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=300, unique=True)

   # def __str__(self):
    #    return f'{self.name}'


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
