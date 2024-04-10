from datetime import datetime
from mongoengine import *


class Bpmn(Document):
    user_id = IntField()
    company_id = IntField(default=1)
    name = StringField(max_length=50, required=True)
    description = StringField(max_length=255, null=True, required=False)
    xml = StringField(null=True, required=False)
    form = ListField(null=True, required=False)
    processObjs = ListField(null=True, required=False)
    userTasks = ListField(null=True, required=False,default=[])
    otherTasks = ListField(null=True, required=False,default=[])
    bindingMap = DictField(required=False, default={})
    storage = DictField(required=False, default={}) # storing user defined variables
    is_valid_form = BooleanField(default=False)
    publishedUsers = ListField(null=True, required=False, default=[])
    publishedUsersDetail = ListField(null=True, required=False, default=[])
    extra = DictField(null=True, required=False, default={})
    postDate = DateTimeField(null=True, required=False, default=datetime.now())

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        self.postDate = datetime.now()
        return super(Bpmn, self).save(*args, **kwargs)