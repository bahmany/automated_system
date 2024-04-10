from datetime import datetime
from mongoengine import Document, IntField, StringField, DateTimeField, ListField, DictField
from amspApp.CompaniesManagment.Charts.models import Chart
from amspApp.CompaniesManagment.models import Company
from amspApp.amspUser.models import MyUser
from django.db import models


class Position(models.Model):
    chart = models.ForeignKey(
        to=Chart,
        null=True,
        blank=True,
        related_name="set_position",
    )
    post_date = models.DateTimeField(
        default=datetime.now,
        blank=True,
        null=True
    )

    # here we have a lots of gaps ...
    # all inboxes links to here
    # when company owner eject an employer,
    # developer empty user field and this position going to wait for another user
    # in this way we can keep its positional inbox
    # and we can transfer inbox item to new user,,,
    # but we have to work one more and stimulate more states

    user = models.ForeignKey(
        to=MyUser,
        related_name="set_positions",
        blank=True,
        null=True
    )

    company = models.ForeignKey(
        to=Company,
        related_name="set_positions",
        blank=True,
        null=True
    )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.user != None and self.id == None:
            posi = Position.objects.filter(user=self.user_id, company=self.company_id).count()
            if posi > 0:
                raise Exception("This person has an active position (model exception) ""یک فرد در دو سمت نگنجد")
        return super(Position, self).save(force_insert, force_update, using,
                                          update_fields)


class PositionsDocument(Document):
    chartID = IntField(null=True, )
    userID = IntField(null=True, )
    companyID = IntField(null=True, )
    chartName = StringField(null=True, )
    profileName = StringField(null=True, )
    companyName = StringField(null=True, )
    profileID = StringField(null=True, )
    avatar = StringField(null=True, )
    postDate = DateTimeField()
    defaultSec = IntField()
    last = ListField(null=True, required=False)
    positionID = IntField(required=False, null=True)
    """
    hasBulkSentPermission :
    0 = has not permission
    1 = has permission
    """
    hasBulkSentPermission = IntField(required=False, null=True, default=1)

    """
    isPositionAllowedToSendDirectly
    0 = No
    1 = Yes
    This is for auto send letters through chart hierarchy
    """
    isPositionAllowedToSendDirectly = IntField(required=False, null=True, default=1)

    """
    isPositionIgonreAssistantHardSent
    0 = No
    1 = Yes
    """
    isPositionIgonreAssistantHardSent = IntField(required=False, null=True, default=1)
    desc = DictField()

    meta = {'indexes': [
        {'fields': ['$profileName', "$chartName"],
         'default_language': 'english',
         'weights': {'profileName': 1, 'chartName': 1}
         },
    ],
    }



    def save(self, force_insert=False, validate=True, clean=True,
             write_concern=None, cascade=None, cascade_kwargs=None,
             _refs=None, save_condition=None, **kwargs):

        if self.userID != None and self.id == None:
            posi = PositionsDocument.objects.filter(userID=self.userID, companyID=self.companyID).count()
            if posi > 0:
                raise Exception("This person has an active position (model exception) ")

        return super(PositionsDocument, self).save(force_insert, validate, clean,
                                                   write_concern, cascade, cascade_kwargs,
                                                   _refs, save_condition, **kwargs)


class PositionSentHistory(Document):
    positionID = IntField(required=True)
    postDate = DateTimeField(default=datetime.now())
    """
    1=compose
    2=forward letter selected
    3=forward one letter
    4=publish bmpn
    """
    thisListIsFor = IntField()
    afterProcess = ListField()
    items = ListField()
    desc = DictField()
