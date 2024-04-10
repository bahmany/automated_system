from collections import Counter
from datetime import datetime
import json

from bson import json_util
from django.db.models import ManyToManyField
from django.shortcuts import render_to_response
from django.template import RequestContext
from mongoengine import QuerySet
from rest_framework.decorators import list_route
from rest_framework_mongoengine import viewsets
from rest_framework.response import Response
from amspApp.CompaniesManagment import Positions
from amspApp.CompaniesManagment.Positions.models import Position, PositionsDocument
from amspApp.CompaniesManagment.Positions.serializers.PositionSerializer import PositionDocumentSerializer
from amspApp.CompaniesManagment.Secretariat.models import Secretariat
from amspApp.CompaniesManagment.Secretariat.serializers.SecretariatsSerializers import SecretariatSerializer, \
    SecretariatSerializerPermission
from amspApp.CompaniesManagment.Secretariat.viewes.SecretariatsViews import SecretariatsViewSet
from amspApp.Letter.models import InboxFolder, Letter
from rest_framework import status
from amspApp.Letter.serializers.InboxFolderSerializer import InboxFolderSerializer
from amspApp.Letter.serializers.LetterSerializer import LetterSerializer
from amspApp._Share.ListPagination import ListPagination


class LetterViewSet(viewsets.ModelViewSet):
    pagination_class = ListPagination
    lookup_field = "id"
    serializer_class = LetterSerializer
    queryset = Letter.objects.all()

    # def retrieve(self, request, *args, **kwargs):
    #     self = self


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.sign["letter"] = None  # this object sometimes creates unlimited loops
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def removeBulkPersonKeys(self, item):
        if "companyID" in item: item.pop("companyID")
        if "companyName" in item: item.pop("companyName")
        if "defaultSec" in item: item.pop("defaultSec")
        if "hasBulkSentPermission" in item: item.pop("hasBulkSentPermission")
        if "isPositionAllowedToSendDirectly" in item: item.pop("isPositionAllowedToSendDirectly")
        if "isPositionIgonreAssistantHardSent" in item: item.pop("isPositionIgonreAssistantHardSent")
        if "desc" in item: item.pop("desc")
        return item

    """
    the first part of creating a letter
    """

    def mapLetterObject(self, data, userInstance, CompanyInstance, request=None):
        positionInstance = Position.objects.get(user=userInstance, company=CompanyInstance)
        postionDocInstance = PositionsDocument.objects.get(positionID=positionInstance.id)
        postionDocInstanceSerial = PositionDocumentSerializer(instance=postionDocInstance)
        secretariatID = SecretariatSerializer().getDefaultSec(self.request.user.id,
                                                              self.request.user.current_company.id,
                                                              postionDocInstanceSerial.data)

        secretariatInstance = SecretariatsViewSet().GetDefaultSecretariatInstance(request)

        data['dateOfPost'] = datetime.now()
        data['creatorPositionID'] = positionInstance.id
        data['creatorPosition'] = self.removeBulkPersonKeys(postionDocInstanceSerial.data)
        # data['recievers'] = data["recievers"]
        data['secretariatID'] = secretariatInstance.secretariat_id
        data['secretariat'] = SecretariatSerializer(instance=secretariatInstance.secretariat).data
        data['secretariatPermissionID'] = secretariatInstance.id
        data['secretariatPermission'] = SecretariatSerializerPermission(instance=secretariatInstance).data
        if "body" in data:
            if data["body"] == None:
                data["body"] = " "
            if data["body"] == "":
                data["body"] = " "

        data['letterType'] = data["itemType"]
        if 'replyedInbox' in data:
            if data['replyedInbox'] != {}:
                data['letterType'] = 4
        return data

    """

    Senario in sending letter !! :

    """

    def create(self, request, *args, **kwargs):
        #pring("------------------------------------------------------------- letter.py line 94")
        newData = self.mapLetterObject(
            request.data,
            request.user,
            request.user.current_company,
            request)
        # this is for handling editing in a very fast way
        # if "id" in newData:
        #     return self.update(request, *args, **kwargs)
        #pring("------------------------------------------------------------- letter.py line 103")
        for nd in newData.keys():
            request.data[nd] = newData[nd]
        return super(LetterViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if (not request.data["body"]):
            request.data["body"] = " "
        return super(LetterViewSet, self).update(request, *args, **kwargs)

    def UpdateDraftRecievers(self, details, pos):
        letterInstace = Letter.objects.get(
            id=details["desc"]["letterID"]
        )
        exp = letterInstace.exp
        exp["recievers_raw"] = json.dumps(details, default=json_util.default)
        update = {
            "recievers_id": details["id"],
            "recievers": details["afterProcess"],
            "exp": exp
        }
        ser = LetterSerializer(instance=letterInstace, data=update, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({})
