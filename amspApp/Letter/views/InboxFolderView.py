from django.shortcuts import render_to_response
from django.template import RequestContext
from mongoengine import QuerySet
from rest_framework.decorators import list_route
from rest_framework_mongoengine import viewsets
from rest_framework.response import Response
from amspApp.CompaniesManagment import Positions
from amspApp.CompaniesManagment.Positions.models import Position
from amspApp.Letter.models import InboxFolder, Inbox
from rest_framework import status
from amspApp.Letter.serializers.InboxFolderSerializer import InboxFolderSerializer
from amspApp.Letter.serializers.InboxSerializer import InboxSerializer
from amspApp._Share.ListPagination import ListPagination
from amspApp.amspUser.views.StatisticsView import GetStaticsViewSet


class InboxFolderViewset(viewsets.ModelViewSet):
    # pagination_class = ListPagination
    lookup_field = "id"
    serializer_class = InboxFolderSerializer


    def template_view(self, request, *args, **kwargs):
        return render_to_response(
            "letter/InboxSidebar.html",
            {},
            context_instance=RequestContext(self.request)
        )

    def get_queryset(self):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        self.queryset = InboxFolder.objects.filter(positionID=pos.id)
        return super(InboxFolderViewset, self).get_queryset()

    def get_object(self):
        return super(InboxFolderViewset, self).get_object()


    def create(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        request.data["positionID"] = pos.id
        request.data["companyID"] = pos.company_id

        return super(InboxFolderViewset, self).create(request, *args, **kwargs)

    @list_route(methods=['get'])
    def listFolderTreeView(self, request, *args, **kwargs):
        pos = Position.objects.get(user=self.request.user, company=self.request.user.current_company)
        foldersList = InboxFolder.objects.filter(positionID=pos.id)

        return Response(self.serializer_class().startTreeView(foldersList))

    @list_route(methods=["post"])
    def AddLetterTo(self, request, *args, **kwargs):
        pos = Position.objects.get(user=self.request.user, company=self.request.user.current_company)
        inboxInstance = Inbox.objects.get(
            id=request.data["inboxID"],
            currentPositionID=pos.id
        )
        self.get_queryset()
        folderInstance = self.queryset.get(
            positionID=pos.id,
            id=request.data["folderID"]
        )
        folders = inboxInstance.folders
        addedFolder = folderInstance._data
        addedFolder["id"] = str(addedFolder["id"])
        folders.append(addedFolder)
        inboxSerial = InboxSerializer(instance=inboxInstance, data={
            "folders": folders
        }, partial=True)
        inboxSerial.is_valid(raise_exception=True)
        # result = inboxSerial.update(instance=inboxInstance, validated_data=inboxSerial.validated_data)
        result = inboxSerial.save()
        GetStaticsViewSet().getInboxFoldersStatisticsRenewCache(positionInstance=pos)
        return Response({})

    @list_route(methods=["post"])
    def RemoveFromLetter(self, request, *args, **kwargs):
        pos = Position.objects.get(user=self.request.user, company=self.request.user.current_company)
        inboxInstance = Inbox.objects.get(
            id=request.data["inboxID"],
            currentPositionID=pos.id
        )
        self.get_queryset()
        folderInstance = self.queryset.get(
            positionID=pos.id,
            id=request.data["folderID"]
        )
        folders = inboxInstance.folders
        removingFolder = folderInstance._data
        finalFolders = []
        for f in folders:
            if (f["id"] != str(folderInstance.id)):
                finalFolders.append(f)
        inboxSerial = InboxSerializer(instance=inboxInstance, data={
            "folders": finalFolders
        }, partial=True)
        inboxSerial.is_valid(raise_exception=True)
        result = inboxSerial.save()
        GetStaticsViewSet().getInboxFoldersStatisticsRenewCache(positionInstance=pos)
        return Response({})
