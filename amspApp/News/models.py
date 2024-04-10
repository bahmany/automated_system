from datetime import datetime

from mongoengine import Document, IntField, StringField, DateTimeField, DictField


class News(Document):
    companyID = IntField()
    title = StringField()
    body = StringField()
    postDate = DateTimeField(default=datetime.now())
    positionID = IntField()
    pic1 = StringField()
    readCount = IntField(default=0)
    """
    type
    1 = news
    2 = static box
    """

    type = IntField(default=1)  # 1= news
    details = DictField()
