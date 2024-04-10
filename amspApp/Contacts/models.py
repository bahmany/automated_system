from datetime import datetime
from mongoengine import Document, IntField, DictField, DateTimeField, ListField, StringField, ReferenceField

__author__ = 'mohammad'


class Contacts(Document):
    userID = IntField(required=True)
    fields = ListField()
    publish = DictField()
    dateOfPost = DateTimeField(default=datetime.now())
    extra = DictField()


class ContactsGroups(Document):
    userID = IntField(required=True)
    name = StringField()
    dateOfPost = DateTimeField(default=datetime.now())
    extra = DictField()


class ContactsGroupItems(Document):
    group = ReferenceField(ContactsGroups)
    member = ReferenceField(Contacts)
    userID = IntField(required=True)
    dateOfPost = DateTimeField(default=datetime.now())
    extra = DictField()



