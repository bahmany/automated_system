from datetime import datetime
from mongoengine import *

__author__ = 'mohammad'


class File(DynamicDocument):
    userID = IntField(required=True)
    originalFileName = StringField(max_length=500, required=True)
    decodedFileName = StringField(max_length=250, required=True)
    dateOfPost = DateTimeField(default=datetime.now(), required=False)
    downloadTimes = DictField(required=False)
    uploaderIP = DictField(required=False)
    extra = DictField(required=False)


"""
uploaded files in compose saves here for history
this history help up to save uploaded file group
"""


class FileAtts(Document):
    files = ListField()
    userID = IntField(required=True)
    positionID = IntField(required=True)
    dateOfPost = DateTimeField(default=datetime.now(), required=False)
    exp = DictField()


class FileFolders(Document):
    userID = IntField(required=True)
    name = StringField(max_length=90, required=True)
    parentFolder = StringField(null=True, required=False)
    """
    privacy
    1 = Private
    2 = Public for globe
    3 = Public for selected companies
    """
    privacy = IntField(default=1)
    count = IntField(default=0)
    companies = ListField()
    dateOfCreate = DateTimeField(default=datetime.now())


class FileFolderItems(Document):
    fileID = ObjectIdField(required=True)
    folder = ReferenceField(FileFolders)
    """
    privacy
    1 = Private
    2 = Public for globe
    3 = Public for selected companies
    """
    privacy = IntField(default=1)
    """
    when we use companies
    we want to restrict share item to specific companies

    """
    companies = ListField()
    file = DictField(default={})
    dateOfCreate = DateTimeField(default=datetime.now())


class FileManagerItem(Document):
    address = StringField(max_length=600, required=True)
    itemType = IntField()  # 1= folder 2= file
    userID = IntField()
    """
    userAllowToRemove :
    in some cases user does not allow to delete files

    """
    userAllowToRemove = BooleanField(default=True)
    userAllowToRename = BooleanField(default=True)
    """
    share :
    userID # file sharing is for entire morabaa !!
    startShare
    endShare # if null unlimited
    shareType # 1= by automation 2=by bpms  3= etc...
    """
    share = DictField()

class FileInAutomations(Document):
    FileManagerItemID = ObjectIdField()
    LetterID = ObjectIdField()

