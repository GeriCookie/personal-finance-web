from django.db import models
from decimal import Decimal
import datetime


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

    def save(self, *args, **kwargs):
        income_added = kwargs.pop('income_added', '')
        expense_added = kwargs.pop('expense_added', '')
        if income_added:
            self.total_income = self.total_income + \
                    self.incomes.last().amount
        if expense_added:
            self.total_expense = self.total_expense + \
                    self.expenses.last().amount
        self.total_amount = self.total_income - self.total_expense
        super(Balance, self).save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return f'{self.name}'

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
    date = models.DateField(default=datetime.date.today)

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
    date = models.DateField(default=datetime.date.today)
