from datetime import datetime

from mongoengine import Document, DateTimeField, IntField, DictField


class MorekhasiSaati(Document):
    dateOfPost = DateTimeField(default=datetime.now())
    creator_position = IntField()
    exp = DictField(default={})
