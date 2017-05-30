# -*- coding: utf-8 -*-
# Generated by Django 1.11rc1 on 2017-05-28 21:59
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal_account', '0010_auto_20170528_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='savingsgoal',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=19),
        ),
    ]