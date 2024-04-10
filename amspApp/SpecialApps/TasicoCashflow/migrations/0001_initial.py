# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CashFlow****TaminCompany',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='CashFlow****TaminDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=60)),
                ('moneyPercentWhenOpenLC', models.DecimalField(decimal_places=2, max_digits=12)),
                ('moneyPercentWhenTransfer', models.DecimalField(decimal_places=2, max_digits=12)),
                ('moneyPercentWhenLC', models.DecimalField(decimal_places=2, max_digits=12)),
                ('daysFromFactoryToShip', models.IntegerField()),
                ('daysFromShipToIranPort', models.IntegerField()),
                ('daysFromIranPortToFactory', models.IntegerField()),
                ('moneyPercentHazineh', models.DecimalField(decimal_places=2, max_digits=12)),
                ('moneyPercentMaliateArzesh', models.DecimalField(decimal_places=2, max_digits=12)),
                ('moneyPercentTarafeh', models.DecimalField(decimal_places=2, max_digits=12)),
                ('moneyRialHamelPerTon', models.DecimalField(decimal_places=2, max_digits=12)),
                ('daysFromShippingToLC', models.IntegerField()),
                ('lcType', models.IntegerField()),
                ('moneyRialPerTon', models.DecimalField(decimal_places=2, max_digits=12)),
                ('moneyRialGhalPerTon', models.DecimalField(decimal_places=2, max_digits=12)),
                ('moneyRialOtherShimiaieePerTon', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
        ),
        migrations.CreateModel(
            name='CashFlow****TaminProject',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=60)),
                ('tonValue', models.DecimalField(decimal_places=2, max_digits=12)),
                ('companyLink', models.ForeignKey(to='****Cashflow.CashFlow****TaminCompany')),
                ('detailLink', models.ForeignKey(to='****Cashflow.CashFlow****TaminDetail')),
            ],
        ),
    ]
