import copy

from asq.initiators import query
from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import serializers
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets
from amspApp.CompaniesManagment.Positions.models import Position, PositionsDocument, PositionSentHistory
from amspApp.CompaniesManagment.Positions.serializers.PositionSerializer import PositionSentHistorySerializer
from amspApp.CompaniesManagment.Processes.models import Bpmn
from amspApp.CompaniesManagment.members.serializers.MemberSerializer import MembersDocumentSerializer
from amspApp.Letter.models import Inbox
from amspApp.Letter.serializers.InboxSerializer import InboxSerializer
from amspApp.Letter.views.InboxListView import InboxListViewSet

from amspApp.Letter.views.LetterView import LetterViewSet

__author__ = 'mohammad'


class SelectMembersViewSet(viewsets.ModelViewSet):
    serializer_class = PositionSentHistorySerializer
    lookup_field = "id"
    queryset = PositionSentHistory.objects.all()

    def template_view(self, request, *args, **kwargs):
        return render_to_response(
            "share/select-recievers/SelectRecievers.html",
            {}, context_instance=RequestContext(request))

    def RemoveDuplicateRecievers(self, list):
        result = []
        for l in list:
            found = False
            for r in result:
                if r["positionID"] == l["positionID"]:
                    found = True
            if not found:
                result.append(l)
        return result

    defaultDesc = {"option": {
        "CurrentTime": "",
        "cc": "",
        "hamesh": "",
        "priority": "",
        "security": "",
    }}

    def ConvertToSimpleList(self, request):
        # selecting all positions into memory
        MembersDoc = PositionsDocument.objects.filter(companyID=self.request.user.current_company.id)
        MembersDoc = MembersDocumentSerializer(instance=MembersDoc, many=True).data
        MembersDoc = query(MembersDoc)
        result = []
        for item in request.data['items']:
            if item["type"] == 2:  # means this is memeber
                # document position id store here :(
                foundItem = MembersDoc.where(lambda x: x["positionID"] == int(item["id"]))[0]
                if not "desc" in item:
                    item["desc"] = self.defaultDesc
                foundItem["option"] = item["desc"]["option"]
                result.append(foundItem)
            else:
                foundItem = MembersDoc.where(
                    lambda x: x["positionID"] in [z["positionID"] for z in item["members"]]).to_list()
                for f in foundItem:
                    if not "desc" in item:
                        item["desc"] = self.defaultDesc
                    f["option"] = item["desc"]["option"]



                result += foundItem
        res = self.RemoveDuplicateRecievers(result)
        for r in res:
            if "desc" in r:
                r.pop("desc")
        return res

    def create(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        request.data["positionID"] = pos.id
        finalList = self.ConvertToSimpleList(request)

        request.data["afterProcess"] = finalList
        result1 = super(SelectMembersViewSet, self).create(request, *args, **kwargs)
        result = result1

        # forwarding group of letter
        if result.data["thisListIsFor"] == 2:
            self.SendAsForward(result.data["afterProcess"], result.data['desc']['selectedInbox'], pos)

        # forwarding a letter
        if result.data["thisListIsFor"] == 3:
            self.SendAsForward(result.data["afterProcess"], [result.data['desc']['selectedInboxID']], pos)

        # forwarding a letter then archive
        if result.data["thisListIsFor"] == 5:
            self.SendAsForward(result.data["afterProcess"], [result.data['desc']['selectedInboxID']], pos)
            InboxListViewSet().archiveIt(request, result.data['desc']['selectedInboxID'])

        # forwarding group of letters then archive
        if result.data["thisListIsFor"] == 6:
            self.SendAsForward(result.data["afterProcess"], result.data['desc']['selectedInbox'], pos)
            class req:
                def __init__(self):
                    pass

            req = req()
            req.user = request.user
            req.data = result.data['desc']['selectedInbox']
            InboxListViewSet().MoveSelectedToArchive(req,*args, **kwargs )

        # send to reciever of a letter and add it to the draft
        if result.data["thisListIsFor"] == 1:
            self.AddRecieversToDraf(result.data, pos)

        # publish bpmn to list
        if result.data["thisListIsFor"] == 4:
            self.PublishBpmn(result.data, request)

        for r in result.data["afterProcess"]:
            if "inboxID" in r:
                r["inboxID"] = str(r["inboxID"])
        return Response(result.data)

    def PublishBpmn(self, data, request):
        idList = []
        for itm in data['afterProcess']:
            idList.append(itm['id'])

        instance = Bpmn.objects.get(id=data['desc']["letterID"])
        publishedUsers = idList
        publishedUsersDetail = data['afterProcess']
        instance.publishedUsers = publishedUsers
        instance.publishedUsersDetail = publishedUsersDetail
        xtra = {}
        xtra["receiverListId"] = data['id']
        instance.extra = xtra
        instance.save()
        return Response({})

    def AddRecieversToDraf(self, details, pos):
        LetterViewSet().UpdateDraftRecievers(details, pos)

    """
    this is for forwards
    """

    @detail_route(methods=["post"])
    def send(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        inboxInstance = Inbox.objects.get(
            id=kwargs["id"],
            currentPositionID=pos.id)
        InboxSerializer().Forward(pos, request.data, inboxInstance)
        return Response({})

    def SendAsForward(self, positionDocDictList, inboxIDs, senderPosInstance):
        for i in inboxIDs:
            inboxInstance = Inbox.objects.get(id=i)
            InboxSerializer().Forward(senderPosInstance, positionDocDictList, inboxInstance)
        return True
