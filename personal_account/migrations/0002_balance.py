# -*- coding: utf-8 -*-
# Generated by Django 1.11rc1 on 2017-05-18 13:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal_account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_income', models.DecimalField(decimal_places=2, default=0.0, max_digits=19)),
                ('total_expenses', models.DecimalField(decimal_places=2, default=0.0, max_digits=19)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=19)),
            ],
        ),
    ]