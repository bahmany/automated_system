from datetime import datetime

from mongoengine import Document, ObjectIdField, IntField, StringField, DictField, DateTimeField, ListField


class DataTable(Document):
    position_id = IntField(null=False, required=True)
    companyId = IntField(null=False, required=True)
    name = StringField(null=False, required=True)
    desc = StringField(null=True, required=False)
    publishedUsers = DictField(null=True, required=False)
    postDate = DateTimeField(default=datetime.now(), required=False)
    exp = DictField(null=True, required=False)
    """
    schedule :
    running strategy like 2 hours, one a week and ...
    """
    schedule = DictField(required=False, null=True)
    """
    field must contains permission about who access to which column
    """
    fields = DictField(null=True, required=False)


class DataTableValues(Document):
    position_id = IntField(null=False, required=True)  # first creator pos id
    companyId = IntField(null=False, required=True)  # first creator company id
    postDate = DateTimeField(default=datetime.now(), required=False)
    desc = StringField(null=True, required=False)
    exp = DictField(null=True, required=False)
    values = ListField(null=True, required=False)
    dataTableLink = ObjectIdField(null=False, required=True)


class TemporaryDataTableValuesForProcess(Document):
    position_id = IntField(null=False, required=True)  # first creator pos id
    companyId = IntField(null=False, required=True)  # first creator company id
    postDate = DateTimeField(default=datetime.now(), required=False)
    desc = StringField(null=True, required=False)
    exp = DictField(null=True, required=False)
    values = ListField(null=True, required=False)
    dataTableLink = ObjectIdField(null=False, required=True)
    bpmnID = ObjectIdField(null=False, required=True)
    launchedProcessID = ObjectIdField(null=False, required=True)
    elementID = StringField(null=True, required=False)
    taskID = StringField(null=True, required=False)
