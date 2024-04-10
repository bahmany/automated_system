from django.utils import timezone
from mongoengine import *


class TraceCategory(Document):
    dateOfPost = DateTimeField(default=timezone.now())
    positionID = IntField(required=True)
    name = StringField(required=True, null=False)
    """
        traceType 
            1= kharide avalieh va enteghal az odoo
            2= az/be anbarhaye hamkaran system
            3= az/be farayandhaye tolid 
            4= az/be department 
    """
    traceType = IntField()
    """
        isItSource
            True  = it is source
            False = it is destination
    """
    isItSource = BooleanField(default=False)
    exp = DictField()


class TraceTypes(Document):
    dateOfPost = DateTimeField(default=timezone.now())
    positionID = IntField(required=True)
    name = StringField(required=True, null=False)
    destination = ReferenceField(TraceCategory, required=True)
    source = ReferenceField(TraceCategory, required=True)
    exp = DictField()
    permittedUsers = ListField()


class TraceEntry(Document):
    dateOfPost = DateTimeField(default=timezone.now())
    positionID = IntField(required=True)
    tracetype = ReferenceField(TraceTypes, required=True)
    parent = ReferenceField("self", required=False)
    details = DictField()
