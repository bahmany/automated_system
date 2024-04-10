from datetime import datetime
from mongoengine import Document, StringField, ReferenceField, IntField, DateTimeField, BooleanField


class HRSanadType(Document):
    name = StringField()

class Vahed(Document):
    name = StringField()

class Format(Document):
    name = StringField()

class FarayandhayeMortabet(Document):
    name = StringField()

class NoeSanad(Document):
    name = StringField()
    

class HRForms(Document):
    typeOfSanad = ReferenceField(HRSanadType)
    shomarehSanad = StringField()
    name = StringField()
    Vahed = ReferenceField(Vahed)
    formatDoc = ReferenceField(Format)
    farayandhayeMortabet = ReferenceField(FarayandhayeMortabet)
    noeSanad = ReferenceField(NoeSanad)
    positionID = IntField()
    PostDate = DateTimeField(default=datetime.now())
    visible = BooleanField(default=True)

class HRFormItems(Document):
    formAddress = StringField()
    form = ReferenceField(HRForms, related_name="link_to_form")
    dateOfPost = DateTimeField(default=datetime.now())
    isItDefault = BooleanField()
