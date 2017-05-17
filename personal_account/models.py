from django.db import models
from decimal import Decimal


class Income(models.Model):
    category = models.TextField(default='')
    amount = models.DecimalField(
            max_digits=19,
            decimal_places=2,
            default=Decimal('0.00')
            )


class Expense(models.Model):
    category = models.TextField(default='')
    amount = models.DecimalField(
            max_digits=19,
            decimal_places=2,
            default=Decimal('0.00')
            )
