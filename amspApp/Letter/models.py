from datetime import datetime
from mongoengine import *
from amspApp.CompaniesManagment.Positions.models import Position
from amspApp.CompaniesManagment.models import Company
from django.utils import timezone

class InboxFolder(Document):
    positionID = IntField(required=False, null=True, )
    companyID = IntField(required=False, null=True)
    parentID = StringField(required=False, null=True)
    isPublic = IntField(default=0)
    title = StringField(required=True)
    count = IntField(default=0)


class InboxLabel(Document):
    positionID = IntField()
    companyID = IntField()
    title = StringField()
    color = StringField()
    bgcolor = StringField()
    count = IntField(default=0)


class InboxGroup(Document):
    positionID = IntField()
    companyID = IntField()
    title = StringField()
    members = ListField(null=True, required=False)
    count = IntField(default=0)
    meta = {'indexes': [
        {'fields': ['$title'],
         'default_language': 'english',
         'weights': {'title': 1}
        },
    ],
    }


class Letter(Document):
    subject = StringField(max_length=150, required=False)
    body = StringField(default=" ", max_length=60000, required=False, null=True,)
    dateOfPost = DateTimeField(default=timezone.now())
    """
    1=Dakheli
    2=Sadereh
    3=Varedeh
    4=Document
    5=Message
    6=report
    7=draft dekheli
    8=draft sadere
    9=draft dakheli
    10=template sadere
    11=template varedeh
    """
    letterType = IntField(required=True)
    creatorPositionID = IntField(required=True)
    creatorPosition = DictField(required=True)
    """
    recievers in Secratriat is for Roonevesht Recievers
    """
    recievers = ListField()
    secretariatID = IntField(required=True)
    secretariat = DictField(required=True)
    secretariatPermissionID = IntField()
    secretariatPermission = DictField()
    attachments = ListField()
    security = IntField(default=1)  # 1=addi 2=mahramaneh 3=serri
    periority = IntField(default=1)  # 1=addi 2=forri 3=kheili forri
    related = ListField()
    sign = DictField()
    parent = DictField()
    exp = DictField()




class Letter_Template(Document):
    dateOfPost = DateTimeField(default=timezone.now())
    CompanyID = IntField()
    SecretariatID = IntField()
    name = StringField()
    letter = DictField()
    extra = DictField()
    """
    whereToStore:
    1= sadereh
    2= varedeh
    3=
    """
    whereToStore = IntField()




class Inbox(Document):
    currentPositionID = IntField()
    dateOfObservable = DateTimeField()
    dateOfCreate = DateTimeField(default=timezone.now())
    sender = DictField()
    star = BooleanField(default=False)
    reciever = DictField()
    """
    these fields are in reciever
    security = IntField()
    #
        1=addi
        2=mahramaneh
        3=serri
    periority = IntField()  #
        1=addi
        2=forri
        3=kheili forri

    """
    letter = DictField()
    letterSummery = StringField(default="Autosave", required=False, null=True)
    labels = ListField()
    folders = ListField()
    readTimes = ListField()
    seen = BooleanField(default=False)
    """
    itemType:
        1 = this inbox item received and sent by some one else as usual inside letter
        2 = this inbox item is sent to a user and an inbox item listed in send letters
        3 = this inbox item forwarded
        4 = this inbox item is replied one, i mean this letter is a replay letter
        5 = this inbox item is auto send inbox as rooneveshte khodkar
        6 = this is first and beginner of a letter
        7 = no Type // this is for storing draft
        8 = this inbox item is sent as exported letter
        9 = this inbox item is in forwarded public folder
        10 = this inbox item is sent as imported letter

    """
    itemType = IntField(default=1)
    replyedInbox = DictField()  # when a sent=4 this field store old inbox body
    previousInboxId = ObjectIdField(null=True, required=False)  # when a sent=3 this field store old inbox body
    """
    itemMode :
        1= dakheli
        2= rooneveshte sadereh
        3= rooneveshte varedeh
        4= draft
        5= draft sadere
        6= draft varedeh
        7= dakheli first send
        8= forward dakheli
        9= sadere
        10= import
        11= template sadere
        12= template import

    """
    itemMode = IntField(default=1)
    """
    itemPlace :
        1= item in inboxes public folders
        2= item in archive
        3= item in trash
        4= item in trash and hide !
        5= item forwarded and then sender deleted by unseen history
    """
    itemPlace = IntField(default=1)
    extra = DictField()



"""
سناریوهای تاریخچه
اول : اولین نفری که نامه ی داخلی را ثبت می کند
دوم : اولین نفری که نامه وارده را پیش نویس ثبت می کند



"""


"""
here we have so many scenarios
    1st: first sender must be specified
    2st: second sender with/without footnotes must be specified
    3st: automated receivers must be specified
    4st: draft send must be specified
    5st: priorities must be observable
    6st: secure items must not be shown
    7st: replay mode must be shown
    8st: forward mode must be shown
"""
class InboxHistory(Document):
    letterID = ObjectIdField()
    """
    senderDetail :
        contains sender avatar
        contains sender name and position
        contains sender inbox id

    """
    senderDetail = DictField()
    recieverDetail = DictField()
    """
    itemType
    1 = usual sent
    2 = first sender
    """
    itemType = IntField()
    """
    itemMode
    1 = usual
    2 = automated
    """
    itemMode = IntField()
    """
    itemActivityMode
    1 = usual
    2 = as replay
    3 = as forward
    """
    itemActivityMode = IntField()
    """
    docType
    1 = usual
    2 = draft
    3 = trash !! :))
    """
    docType = IntField()
    previousInboxId = ObjectIdField(null=True, required=False)
    currentInboxId = ObjectIdField(null=True, required=False)


class CompanyRecieverGroup(Document):
    name = StringField(null=False, required=True)
    companyID = IntField()
    postPositionID = IntField()
    postDate = DateTimeField(default=timezone.now())

    meta = {'indexes': [
        {'fields': ['$name'],
         'default_language': 'english',
         'weights': {'name': 1}
        },
    ],
    }


"""
here we have so many issue
"""
class CompanyReciever(Document):
    name = StringField(null=False, required=True)
    companyID = IntField()
    group = ReferenceField(CompanyRecieverGroup)
    groupname = StringField(default="")
    postPositionID = IntField()
    postDate = DateTimeField(default=timezone.now())
    details = DictField(required=False)
    meta = {'indexes': [
        {'fields': ['$name', "$details", "$groupname"],
         'default_language': 'english',
         'weights': {'name': 1, 'details':1, "groupname":1}
        },
    ],
    }

# personel names of company recievers
class CompanyRecieversSubName(Document):
    name = StringField(null=False, required=True)
    details = DictField(required=False)
    companyReciever = ReferenceField(CompanyReciever)
    postDate = DateTimeField(default=timezone.now())
    postPositionID = IntField()



class Recieved(Document):
    postDate = DateTimeField(default=timezone.now())
    timeOf = StringField( required=True)
    reciever = StringField(required=True)
    desc = StringField()
    how = StringField()
    sender = StringField()
    whenSender = StringField()
    inboxID = StringField()
    positionID = IntField(null=False, required=True)


class ExportScannedAfterSend(Document):
    postDate = DateTimeField(default=timezone.now())
    inboxID = StringField()
    positionID = IntField(null=False, required=True)
    fileAddr = ListField(required=True)
    desc = StringField()

class ExportTemplates(Document):
    postDate = DateTimeField(default=timezone.now())
    secID = IntField(required=True)
    fileAddr = StringField(required=True)
    name = StringField(required=True)
    positionID = IntField(null=False, required=True)
    desc = DictField()

class SecTag(Document):
    companyID = IntField()
    name = StringField()
    postDate = DateTimeField(default=timezone.now())
    secretariatID = IntField()
    PositionID = IntField()
    letterType = IntField()  # 1: sadereh 2: varedeh


class SecTagItems(Document):
    tag = ReferenceField(SecTag)
    letterID = ObjectIdField()
    positionID = IntField()
    postDate = DateTimeField(default=timezone.now())





