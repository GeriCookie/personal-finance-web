from django.db import models
from decimal import Decimal


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
                    self.income_set.last().amount
        if expense_added:
            self.total_expense = self.total_expense + \
                    self.expense_set.last().amount
        self.total_amount = self.total_income - self.total_expense
        super(Balance, self).save(*args, **kwargs)


class Income(models.Model):
    balance = models.ForeignKey(
            Balance,
            default=None,
            on_delete=models.CASCADE
        )
    category = models.TextField(default='')
    amount = models.DecimalField(
            max_digits=19,
            decimal_places=2,
            default=Decimal('0.00')
            )


class Expense(models.Model):
    balance = models.ForeignKey(
            Balance,
            default=None,
            on_delete=models.CASCADE
        )
    category = models.TextField(default='')
    amount = models.DecimalField(
            max_digits=19,
            decimal_places=2,
            default=Decimal('0.00')
            )
