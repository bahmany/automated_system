from datetime import datetime

from mongoengine import *


class RequestGood(Document):
    positionID = IntField(required=True, )
    dateOfPost = DateTimeField(default=datetime.now(), )
    rgPriority = IntField(required=True, )  # 1= فوری      ۲=عادی
    rgType = IntField(required=True, )
    draft = BooleanField(default=True)
    exp = DictField()

class RequestGoodSigns(Document):
    requestGoodLink = ReferenceField(RequestGood, required=True)
    positionID = IntField(required=True, )
    dateOfPost = DateTimeField(default=datetime.now(), )
    signStepID = IntField(required=True, )
    comment = StringField(required=False, null=True)
    exp = DictField()





class RequestGoodItems(Document):
    requestGoodLink = ReferenceField(RequestGood, required=True)
    positionID = IntField(required=True, )
    dateOfPost = DateTimeField(default=datetime.now(), )
    exp = DictField()


class RequestGoodItemsHamkaran(Document):
    dateOfPost = DateTimeField(default=datetime.now(), )
    # Serial = IntField(required=False, )
    # partTreeRef = IntField(required=False, )
    # PartRef = IntField(required=False, )
    # PartCode = StringField(required=False, )
    # PartName = StringField(required=False, )
    # PartNo = StringField(required=False, )
    # UnitName = StringField(required=False, )
    # Title = StringField(required=False, )
    # Parent = StringField(required=False, )
    exp = DictField()

