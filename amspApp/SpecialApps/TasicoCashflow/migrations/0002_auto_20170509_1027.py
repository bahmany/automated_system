# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('****Cashflow', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CashFlow****TaminIncommings',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('exp', models.TextField(max_length=1200, null=True, blank=True)),
                ('money_type', models.IntegerField()),
                ('money', models.DecimalField(decimal_places=2, max_digits=12)),
                ('dateOfRecieve', models.DateTimeField(default=datetime.datetime(2017, 5, 9, 10, 27, 32, 637006))),
            ],
        ),
        migrations.CreateModel(
            name='CashFlow****TaminPayments',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('exp', models.TextField(max_length=1200, null=True, blank=True)),
                ('pay_type', models.IntegerField()),
                ('pay', models.DecimalField(decimal_places=2, max_digits=12)),
                ('dateOfPay', models.DateTimeField(default=datetime.datetime(2017, 5, 9, 10, 27, 32, 635998))),
            ],
        ),
        migrations.AddField(
            model_name='cashflow****taminproject',
            name='****Date',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 9, 10, 27, 32, 634998)),
        ),
        migrations.AlterField(
            model_name='cashflow****taminproject',
            name='companyLink',
            field=models.ForeignKey(to='****Cashflow.CashFlow****TaminCompany', related_name='set_company'),
        ),
        migrations.AlterField(
            model_name='cashflow****taminproject',
            name='detailLink',
            field=models.ForeignKey(to='****Cashflow.CashFlow****TaminDetail', related_name='set_details'),
        ),
    ]
