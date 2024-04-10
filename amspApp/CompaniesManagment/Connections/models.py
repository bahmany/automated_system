from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import TextField
from mongoengine import Document, IntField, ReferenceField, DateTimeField, StringField, DictField, DynamicDocument, ListField

from amspApp.CompaniesManagment.Charts.models import Chart
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.models import Company
from amspApp.Letter.models import Letter
from amspApp.amspUser.models import MyUser
from django.utils import timezone

__author__ = 'mohammad'

from django.db import models
from django.utils.translation import ugettext_lazy as _


"""

ems
"""


class Connections(Document):
    userID = IntField()
    companyID = IntField()
    dateOfPost = DateTimeField(default=timezone.now())
    databaseEngine = StringField(required=True)
    connectionType = StringField(required=True)
    hostAddress = StringField(required=True)
    hostPort = StringField(required=False, null=True, default="1433")
    hostInstanceName = StringField(required=False, null=True)
    username = StringField(required=False, null=True)
    password = StringField(required=False, null=True)
    databaseName = StringField(required=False, null=True)
    extra = DictField()

class ConnectionPools(Document):
    userID = IntField(required=True)
    companyID = IntField(required=True)
    dateOfPost = DateTimeField(default=timezone.now())
    connection = ReferenceField(Connections, required=True)
    name = StringField(required=True)
    exp = StringField(required=False, null=True)
    pythonCode = StringField(required=False, null=True)
    extra = DictField(required=False, null=True)
    sqls = ListField(required=False, null=True)




