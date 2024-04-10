

from datetime import datetime
from mongoengine import *


class MSTemplate(Document):
    position_id = ObjectIdField()
    companyId = IntField(null=False, required=True)
    name = StringField(null=False, required=True)
    icon = StringField(null=True, required=False)
    desc = StringField(null=True, required=False)
    publishedUsers = ListField(null=True, required=False,default=[])
    publishedUsersDetail = ListField(null=True, required=False,default=[])
    dataType = StringField(null=False, required=True)
    postDate = DateTimeField(default=datetime.now(), required=False)
    exp = DictField(null=True, required=False)


class MSData(Document):
    position_id = ObjectIdField()
    template_id = ObjectIdField()
    value = IntField(null=False, required=True)
    desc = StringField(null=True, required=False)
    postDate = DateTimeField(default=datetime.now(), required=False)
    entryDate = DateTimeField(default=datetime.now(), required=False)