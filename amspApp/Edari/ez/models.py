from datetime import datetime

from mongoengine import Document, IntField, DateTimeField, DictField, ReferenceField, StringField


class Ez(Document):
    positionID = IntField(required=True, )
    dateOfPost = DateTimeField(default=datetime.now())
    tarikheAnjam = DateTimeField(null=True, required=False)
    JahateAnjameh = StringField(null=True, required=False)
    Sharh = StringField(null=True, required=False)
    desc = DictField()
    """
    typeOf :
        1 = draft
        2 = confirm
    """
    typeOf = IntField(required=True, )



class EzSigns(Document):
    EzLink = ReferenceField(Ez)
    positionID = IntField()
    dateOfPost = DateTimeField(default=datetime.now())
    whichStep = IntField()
    comment = StringField(null=True, required=False)
    desc = DictField()
