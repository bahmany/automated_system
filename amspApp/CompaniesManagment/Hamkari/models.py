from datetime import datetime
from mongoengine import DynamicDocument, IntField, DateTimeField, StringField, DictField, ListField, ObjectIdField, \
    ReferenceField, BooleanField

__author__ = 'mohammad'


class Hamkari(DynamicDocument):
    userID = IntField(required=True)
    dateOfPost = DateTimeField(default=datetime.now(), required=False)
    startDate = DateTimeField(required=False)
    endDate = DateTimeField(required=False)
    title = StringField(required=True)
    exp = StringField(required=True)
    publish = BooleanField(default=False)

class HamkariJobs(DynamicDocument):
    hamkariID = ReferenceField(Hamkari, required=True)
    name = StringField(required=True)
    dateOfPost = DateTimeField(default=datetime.now(), required=False)
    positionID = IntField(required=True)
    exp = StringField(required=True)
    extraFields = ListField()
    extra = DictField(required=False)
    publish = BooleanField(default=False)


class RequestHamkari(DynamicDocument):
    userID = IntField(required=True)
    hamkariID = ReferenceField(Hamkari, required=True)
    jobID = ReferenceField(HamkariJobs, required=True)
    """
    1= dar daste barresi
    2= azmoon
    3= mosahebeh
    4= pass
    5= fail
    """
    type = IntField(required=False, default=1)
    dateOfPost = DateTimeField(default=datetime.now(), required=False)
    extra = DictField(required=False)

