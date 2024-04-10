from django.utils import timezone
from mongoengine import Document, IntField, DateTimeField, DictField, StringField, ReferenceField, ListField


class Finding(Document):
    positionID = IntField(required=True, )
    companyID = IntField(required=True, )
    dateOfPost = DateTimeField(default=timezone.now())
    """
    type :
       1 = Draft
       2 = Root Cause and Cap Analysis
       3 = Follow Up
       4 = Finish
    """
    type = IntField(default=1)
    currentPerformerPositionID = IntField()
    performers = DictField()
    dueDateStart = DateTimeField()
    dueDateEnd = DateTimeField()
    desc = DictField()
    Files = DictField()
    rootCause = DictField()
    followUpPosID = StringField()
    followUp = DictField()


class QCDocuments(Document):
    positionID = IntField(required=True, )
    companyID = IntField(required=True, )
    dateOfPost = DateTimeField(default=timezone.now())
    """
    type :
       1 = Manual
    """
    type = IntField(default=1)
    title = StringField()
    exp = StringField()
    fileAddr = StringField()


class QCDocumentsDetails(Document):
    positionID = IntField(required=True, )
    companyID = IntField(required=True, )
    QCDocumentLink = ReferenceField(QCDocuments)
    dateOfPost = DateTimeField(default=timezone.now())
    pageIndex = IntField()
    pageID = IntField()
    width = IntField()
    height = IntField()
    word_margin = IntField()
    x0 = IntField()
    y0 = IntField()
    x1 = IntField()
    y1 = IntField()
    pageNum = IntField()
    word = StringField()
    fileAddr = StringField()

    meta = {'indexes': [
        {'fields': ["$word"],
         'default_language': 'none',
         'weights': {'word': 1}
         }
    ]}

class QCDocumentsOulines(Document):
    positionID = IntField(required=True, )
    companyID = IntField(required=True, )
    QCDocumentLink = ReferenceField(QCDocuments)
    dateOfPost = DateTimeField(default=timezone.now())
    title = StringField()
    desc = StringField()
    left = IntField()
    page = IntField()
    pageid = IntField()
    top = IntField()

class QCAuditingSchedule(Document):
    positionID = IntField(required=True, )
    companyID = IntField(required=True, )
    QCDocumentLink = ReferenceField(QCDocuments)
    dateOfPost = DateTimeField(default=timezone.now())
    auditNo = StringField()
    issueDate = DateTimeField(default=timezone.now())
    auditScope = ListField()
    objectives = ListField()
    auditDate = DateTimeField(default=timezone.now())
    audotLocation = ListField()
    leadAuditor = DictField()
    auditors = ListField()
    AuditDetails = ListField()

