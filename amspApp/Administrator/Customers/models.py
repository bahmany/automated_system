from django.db import models
from datetime import datetime


class Billing_Customer(models.Model):
    userID = models.IntegerField(null=False, blank=False)
    dateOfPost = models.DateTimeField(default=datetime.now(), blank=True)
    subdomainName = models.CharField(max_length=30, unique=True, blank=False)
    customerName = models.CharField(max_length=50, blank=False)
    username = models.CharField(max_length=50, blank=False)
    password = models.CharField(max_length=50, blank=False)
    customerMobile = models.CharField(max_length=13, blank=False)
    customerEmail = models.CharField(max_length=60, blank=False)
    address = models.TextField(blank=True, null=True)
    exp = models.TextField(blank=True, null=True)
    isDeleted = models.BooleanField(default=False, blank=True)
    isSuspended = models.BooleanField(default=False, blank=True)
    defaultLoginPage = models.CharField(max_length=50, blank=False)
    defaultTemplate = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return u'{0}'.format(self.customerName)





class UserCustomer(models.Model):
    userID = models.IntegerField(null=False, blank=False, unique=True)
    customerID = models.IntegerField(null=False, blank=False)


