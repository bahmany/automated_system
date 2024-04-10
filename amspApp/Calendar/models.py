from datetime import datetime

from mongoengine import Document, IntField, DateTimeField, StringField, BooleanField, DictField


# this model is user related not position related !!
class CalendarItems(Document):
    userID = IntField()
    postDate = DateTimeField(default=datetime.now, required=False, null=True)
    startDate = DateTimeField()
    endDate = DateTimeField(required=False, null=True)
    title = StringField(max_length=255)
    detail = StringField()
    finished = BooleanField(default=False)
    priority = IntField(default=1) # 1= usual    2= forced
    progress = IntField(default=0)
    exp = DictField(null=True, required=False)



