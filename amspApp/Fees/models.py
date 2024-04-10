from datetime import datetime

from mongoengine import Document, IntField, DateTimeField, DictField, ReferenceField, StringField


class Fee(Document):
    dateOfPost = DateTimeField(default=datetime.now())
    positionID = IntField(required=True, )


class FeeItem(Document):
    dateOfPost = DateTimeField(default=datetime.now())
    positionID = IntField(required=True, )
    name1 = StringField(null=True, required=False)
    name2 = StringField(null=True, required=False)
    fee = IntField(required=True, )
    fee_with_vat = IntField(required=True, )
