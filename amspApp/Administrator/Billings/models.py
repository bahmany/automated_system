from django.db import models
from datetime import datetime
from amspApp.Administrator.Customers.models import Billing_Customer


class Billing_Strategies(models.Model):
    Title = models.TextField(blank=False, null=False)
    createdUserID = models.IntegerField(null=False, blank=False)
    dateOfPost = models.DateTimeField(default=datetime.now(), blank=True)
    """
    TypeOfBilling :
       1 : daily
       2 : monthly
       3 : yearly
       4 : specific times,, it needs startDate and enddate
       5 : no limitation
       6 : days for example 60 days from when payment completed
    """
    Billing_Stat_Choices = (
        ("1", "توسعه"),
        ("2", "پیشرفته"),
        ("3", "نامحدود")
    )
    TypeOfBilling = models.IntegerField(default=2, choices=Billing_Stat_Choices)
    days = models.IntegerField(default=30)
    daysOfTrial = models.IntegerField(default=30)
    StorageMb = models.IntegerField(default=10240)
    CostPerUser = models.BigIntegerField(default=750000)  # rial
    exp = models.TextField(blank=True, null=True)
    isDeleted = models.BooleanField(default=False, blank=True)
    isPublished = models.BooleanField(default=False, blank=True)




    def __str__(self):
        return u'{0}'.format(self.Title)


"""
بابت هر پرداختی که کاربر انجام میدهد
یک رکورد ساخته می شود
سیستم تاریخ آخرین پرداخت به علاوه نوع استراتژی را چک میکند
و مجوز استفاده را میدهد یا نمی دهد
"""
class Billing_Payments(models.Model):
    createdUserID = models.IntegerField(null=False, blank=False)
    dateOfPost = models.DateTimeField(default=datetime.now(), blank=True)
    billingStrategyLink = models.ForeignKey(Billing_Strategies, blank=False, null=False,)
    customerLink = models.ForeignKey(Billing_Customer, blank=False, null=False)
    """
    loadedPrice :
    پولی که کاربر پرداخت کرده است

    """
    loadedPrice = models.BigIntegerField(null=False, blank=False)
    bankID = models.CharField(max_length=40)
    paymentType = (
        ("1", 'پرداخت آنلاین'), # آنلاین
        ("2", 'فیش بانکی'),#
        ("3", 'پرداخت نقدی'),#
        ("4", 'پرداخت اولیه قرارداد'),# هنگامی که قرارداد بسته می شود و پیش پرداخت می دهند
        ("5", 'پرداخت مرحله ای قرارداد'),#
        ("6", 'پرداخت نهایی قرارداد'),#
        ("7", 'هدیه'),#
    )
    """
    مانده حساب کاربر
    زمانی ممکن است کاربر بیشتر از مبلغ انتخاب واریز شده پول  پرداخت نماید
سناریو اینگونه است که
کاربر مبلغی را واریز می کند
مبلغ به محض این که بحساب واریز شد طرح انتخابیش فعال می شود
و بعد از فعال شدن مبلغ مابع التفاوت در فیلد زیر ذخیره میشود

    """
    totalPrice = models.BigIntegerField(null=True, blank=True, default=0)
    exp = models.TextField()
    Title = models.CharField(max_length=600)




    def __str__(self):
        return u'{0}'.format(self.Title)