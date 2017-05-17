# -*- coding: utf-8 -*-
# Generated by Django 1.11rc1 on 2017-05-17 22:17
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.TextField(default='')),
                ('amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=19)),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.TextField(default='')),
                ('amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=19)),
            ],
        ),
    ]
