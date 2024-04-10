# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('****Cashflow', '0002_auto_20170509_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashflow****taminincommings',
            name='dateOfRecieve',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 25, 15, 49, 55, 984624)),
        ),
        migrations.AlterField(
            model_name='cashflow****taminincommings',
            name='money',
            field=models.DecimalField(max_digits=16, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='cashflow****taminpayments',
            name='dateOfPay',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 25, 15, 49, 55, 984351)),
        ),
        migrations.AlterField(
            model_name='cashflow****taminpayments',
            name='pay',
            field=models.DecimalField(max_digits=16, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='cashflow****taminproject',
            name='****Date',
            field=models.DateTimeField(default=datetime.datetime(2021, 10, 25, 15, 49, 55, 984010)),
        ),
    ]
