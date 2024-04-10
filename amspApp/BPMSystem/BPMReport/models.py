

from datetime import datetime
from mongoengine import *


class ReportTemplate(Document):
    position_id = ObjectIdField()
    companyId = IntField(null=False, required=True)
    name = StringField(null=False, required=True)
    desc = StringField(null=True, required=False)
    structure = DictField(null=True,required=False)
    postDate = DateTimeField(default=datetime.now(), required=False)
