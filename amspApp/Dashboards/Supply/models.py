from datetime import datetime

from mongoengine import *


class GoodsProviders(Document):
    dateOfPost = DateTimeField(default=datetime.now())
    extra = DictField()


class SupplementCategories(Document):
    dateOfPost = DateTimeField(default=datetime.now())
    name = StringField(required=True)
    code = IntField(required=True)
    parent = ReferenceField("self", null=True)
