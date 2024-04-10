from datetime import datetime, timezone
from mongoengine import *

class docModel(Document):
    companyId=IntField(null=True,required=False)
    position_id=ObjectIdField(null=True,required=True)
    name = StringField()

class docZone(Document):
    companyId=IntField(null=True,required=False)
    position_id=ObjectIdField(null=True,required=True)
    name = StringField()

class docFormat(Document):
    companyId=IntField(null=True,required=False)
    position_id=ObjectIdField(null=True,required=True)
    name = StringField()

class docRelated(Document):
    companyId=IntField(null=True,required=False)
    position_id=ObjectIdField(null=True,required=True)
    name = StringField()

class docType(Document):
    companyId=IntField(null=True,required=False)
    position_id=ObjectIdField(null=True,required=True)
    name = StringField()



class DMSTree(Document):
    positionID = IntField(required=False, null=True, )
    companyID = IntField(required=False, null=True)
    parentID = StringField(required=False, null=True)
    isPublic = IntField(default=0)
    title = StringField(required=True)
    count = IntField(default=0)








class DMS(Document):
    """
    allFiles:[
    {'dir':'DIR',
    'size':'SIZE',
    'name':'NAME',
    'date':'DATE',
    'isCurr':'0,1',}
    ]
    """
    position_id = ObjectIdField(null=True, required=False)
    companyId = IntField(null=True, required=False)
    name = StringField(null=False, required=True)
    docCode = StringField(null=True, required=False)
    docType = ReferenceField(docType,null=False,required=True)
    docZone = ReferenceField(docZone,null=False,required=True)
    docFormat = ReferenceField(docFormat,null=False,required=True)
    docRelated = ReferenceField(docRelated,null=False,required=True)
    docModel = ReferenceField(docModel,null=False,required=True)
    allFiles = ListField(null=True, required=False, default=[])
    currentFile = StringField(null=True, required=False)
    postDate = DateTimeField(default=datetime.now())
    latestPostDate = DateTimeField(default=datetime.now())
    visible = BooleanField(default=True)
    extra=DictField(null=True,required=False,default={})



