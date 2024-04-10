from django.utils import timezone
from mongoengine import *


# this model is user related not position related !!
class Chat(Document):
    positionID = IntField(required=True,)
    companyID = IntField(required=True,)
    dateOfPost = DateTimeField(default=timezone.now())
    """
    chatType :
    1= single user
    2= group
    3= page
    """
    chatType = IntField(required=True,)
    dest_positionID = IntField()     # if chatType = 1
    dest_groupID = ObjectIdField()   # if chatType = 2
    dest_pageID = ObjectIdField()    # if chatType = 3
    is_deleted = BooleanField(default=False)
    seen = BooleanField(default=False)
    dateOfSeen = DateTimeField()

    body = StringField(min_length=4, max_length=400, required=True)
    desc = DictField()

class MutedPositions(Document):
    positionID = IntField(required=True,)
    companyID = IntField(required=True,)
    dateOfPost = DateTimeField(default=timezone.now())
    mutedPositionID = IntField(required=True)




