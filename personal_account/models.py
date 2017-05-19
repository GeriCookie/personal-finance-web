from django.db import models
from decimal import Decimal


class Balance(models.Model):
    total_income = models.DecimalField(
            max_digits=19,
            decimal_places=2,
            default=0.00
    )
    total_expenses = models.DecimalField(
            max_digits=19,
            decimal_places=2,
            default=0.00
    )
    total_amount = models.DecimalField(
            max_digits=19,
            decimal_places=2,
            default=0.00
    )


class Income(models.Model):
    balance = models.ForeignKey(Balance, default=None, on_delete=models.CASCADE)
    category = models.TextField(default='')
    amount = models.DecimalField(
            max_digits=19,
            decimal_places=2,
            default=Decimal('0.00')
            )


class Expense(models.Model):
    balance = models.ForeignKey(Balance, default=None, on_delete=models.CASCADE)
    category = models.TextField(default='')
    amount = models.DecimalField(
            max_digits=19,
            decimal_places=2,
            default=Decimal('0.00')
            )
