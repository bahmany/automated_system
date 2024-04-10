from datetime import datetime

from mongoengine import Document, IntField, DateTimeField, ReferenceField, StringField, DictField


class AmareTolidNehieh2(Document):
    dateOfPost = DateTimeField(default=datetime.now())
    dateOfAmar = DateTimeField(default=datetime.now())


class AmareTolidNehieh2Items(Document):
    amarelink = ReferenceField(AmareTolidNehieh2)
    dateOfPost = DateTimeField(default=datetime.now())
    desc = DictField()

