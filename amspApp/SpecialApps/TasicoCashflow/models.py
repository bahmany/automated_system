from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from mongoengine import Document, DateTimeField, StringField, IntField, ListField


class CashFlow****TaminCompany(models.Model):
    name = models.CharField(null=False, blank=False, max_length=60, )


class CashFlow****TaminDetail(models.Model):
    name = models.CharField(null=False, blank=False, max_length=60, )
    moneyPercentWhenOpenLC = models.DecimalField(max_digits=12, decimal_places=2)
    moneyPercentWhenTransfer = models.DecimalField(max_digits=12, decimal_places=2)
    moneyPercentWhenLC = models.DecimalField(max_digits=12, decimal_places=2)
    daysFromFactoryToShip = models.IntegerField()
    daysFromShipToIranPort = models.IntegerField()
    daysFromIranPortToFactory = models.IntegerField()
    moneyPercentHazineh = models.DecimalField(max_digits=12, decimal_places=2)
    moneyPercentMaliateArzesh = models.DecimalField(max_digits=12, decimal_places=2)
    moneyPercentTarafeh = models.DecimalField(max_digits=12, decimal_places=2)
    moneyRialHamelPerTon = models.DecimalField(max_digits=12, decimal_places=2)
    daysFromShippingToLC = models.IntegerField()
    lcType = models.IntegerField()  # 1= import 2= dekheli
    moneyRialPerTon = models.DecimalField(max_digits=12, decimal_places=2)
    moneyRialGhalPerTon = models.DecimalField(max_digits=12, decimal_places=2)
    moneyRialOtherShimiaieePerTon = models.DecimalField(max_digits=12, decimal_places=2)



class CashFlow****TaminProject(models.Model):
    name = models.CharField(null=False, blank=False, max_length=60, )
    companyLink = models.ForeignKey(CashFlow****TaminCompany, related_name='set_company')
    detailLink = models.ForeignKey(CashFlow****TaminDetail, related_name='set_details')
    ****Date = models.DateTimeField(default=datetime.now())
    tonValue = models.DecimalField(max_digits=12, decimal_places=2)

class CashFlow****TaminPayments(models.Model):
    name = models.CharField(null=False, blank=False, max_length=60, )
    exp = models.TextField(max_length=1200, null=True, blank=True,)
    """
    pay_type
    1 = hoghogh
    2 = tankhah
    3 = LC Payment
    """
    pay_type = models.IntegerField()
    pay = models.DecimalField(max_digits=16, decimal_places=2)
    dateOfPay = models.DateTimeField(default=datetime.now())

class CashFlow****TaminIncommings(models.Model):
    name = models.CharField(null=False, blank=False, max_length=60, )
    exp = models.TextField(max_length=1200, null=True, blank=True,)

    """
    pay_type
    1 = check
    2 = soode banki
    3 = LC
    """
    money_type = models.IntegerField()
    money = models.DecimalField(max_digits=16, decimal_places=2)
    dateOfRecieve = models.DateTimeField(default=datetime.now())


class CashFlow****TaminAllDateTmp(Document):
    projectID = IntField()
    current = DateTimeField()
    current_dayname = StringField()
    current_sh = StringField()
    current_sh_day = IntField()
    current_sh_month = IntField()
    current_sh_year = IntField()
    income = IntField()
    incomeDetails = ListField()
    pay = IntField()
    payDetails = ListField()
    total = IntField()