from django.shortcuts import render_to_response
from django.template import RequestContext
from mongoengine import QuerySet
from rest_framework.decorators import list_route
from rest_framework_mongoengine import viewsets
from rest_framework.response import Response
from amspApp.CompaniesManagment import Positions
from amspApp.CompaniesManagment.Positions.models import Position
from amspApp.Letter.models import InboxFolder, InboxLabel, Inbox
from rest_framework import status
from amspApp.Letter.serializers.InboxFolderSerializer import InboxFolderSerializer
from amspApp.Letter.serializers.InboxLabelSerializer import InboxLabelSerializer
from amspApp.Letter.serializers.InboxSerializer import InboxSerializer
from amspApp._Share.ListPagination import ListPagination
from amspApp.amspUser.views.StatisticsView import GetStaticsViewSet


class InboxLabelViewset(viewsets.ModelViewSet):
    pagination_class = ListPagination
    lookup_field = "id"
    serializer_class = InboxLabelSerializer


    def get_queryset(self):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)

        self.queryset = InboxLabel.objects.filter(positionID=pos.id)
        return super(InboxLabelViewset, self).get_queryset()

    def create(self, request, *args, **kwargs):
        request.data["companyID"] = self.request.user.current_company.id
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        request.data["positionID"] = pos.id
        return super(InboxLabelViewset, self).create(request, *args, **kwargs)
    def update(self, request, *args, **kwargs):
        request.data["companyID"] = self.request.user.current_company.id
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        request.data["positionID"] = pos.id
        return super(InboxLabelViewset, self).update(request, *args, **kwargs)


    @list_route(methods=["post"])
    def AddLetterTo(self, request, *args, **kwargs):
        pos = Position.objects.get(user=self.request.user, company=self.request.user.current_company)
        inboxInstance = Inbox.objects.get(
            id=request.data["inboxID"],
            currentPositionID=pos.id
        )
        self.get_queryset()
        labelInstance = self.queryset.get(
            positionID=pos.id,
            id=request.data["labelID"]
        )
        labels = inboxInstance.labels
        addedLabel = labelInstance._data
        addedLabel["id"] = str(addedLabel["id"])
        labels.append(addedLabel)
        inboxSerial = InboxSerializer(instance=inboxInstance, data={
            "labels": labels
        }, partial=True)
        inboxSerial.is_valid(raise_exception=True)
        # result = inboxSerial.update(instance=inboxInstance, validated_data=inboxSerial.validated_data)
        result = inboxSerial.save()
        # GetStaticsViewSet().getInboxLabelsStatisticsRenewCache(positionInstance=pos)
        return Response({})

    @list_route(methods=["post"])
    def RemoveFromLetter(self, request, *args, **kwargs):
        pos = Position.objects.get(user=self.request.user, company=self.request.user.current_company)
        inboxInstance = Inbox.objects.get(
            id=request.data["inboxID"],
            currentPositionID=pos.id
        )
        self.get_queryset()
        labelInstance = self.queryset.get(
            positionID=pos.id,
            id=request.data["labelID"]
        )
        labels = inboxInstance.labels
        removingFolder = labelInstance._data
        finalLabels = []
        for f in labels:
            if (f["id"] != str(labelInstance.id)):
                finalLabels.append(f)
        inboxSerial = InboxSerializer(instance=inboxInstance, data={
            "labels": finalLabels
        }, partial=True)
        inboxSerial.is_valid(raise_exception=True)
        result = inboxSerial.save()
        GetStaticsViewSet().getInboxLabelsStatisticsRenewCache(positionInstance=pos)
        return Response({})
