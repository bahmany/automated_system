import mimetypes
import os
from datetime import datetime

from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from elasticsearch import NotFoundError, RequestError
from elasticsearch_dsl import Search
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets
from tweepy.streaming import json

from amsp.settings import FILE_PATH
from amspApp.CompaniesManagment.Positions.models import Position
from amspApp.FileServer.views.FileUploadView import FileUploadViewSet
from amspApp.FileServer.views.fileManagerBridge import FileManager
from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh_with_time
from amspApp.Infrustructures.Classes.jsonDefault import defaultMorabaa
from amspApp.Letter.elasticConn import getElasticSearch
from amspApp.Letter.models import Inbox, InboxHistory, Letter
from amspApp.Letter.serializers.InboxSerializer import InboxSerializer
from amspApp.Letter.serializers.LetterHistorySerializer import LetterHistorySerializer
from amspApp.Notifications.models import Notifications
from amspApp.Notifications.views.NotificationView import NotificationViewSet
from amspApp._Share.ListPagination import ListPagination
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class InboxListViewSet(viewsets.ModelViewSet):
    pagination_class = ListPagination
    lookup_field = "id"
    serializer_class = InboxSerializer

    def template_view(self, request, *args, **kwargs):
        return render_to_response(
            "letter/Inbox/base.html",
            {},
            context_instance=RequestContext(request)
        )

    def template_view_list(self, request, *args, **kwargs):
        return render_to_response(
            "letter/Inbox/List.html",
            {},
            context_instance=RequestContext(request)
        )

    def template_view_sidebar(self, request, *args, **kwargs):
        return render_to_response(
            "letter/Sidebar/base.html",
            {},
            context_instance=RequestContext(request)
        )

    def get_queryset(self):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        self.queryset = Inbox.objects.filter(
            currentPositionID=pos.id,
            dateOfObservable__lte=datetime.now()
        ).order_by("-dateOfObservable")
        return super(InboxListViewSet, self).get_queryset()

    @list_route(methods=["get"])
    def StartConverting(self, request, *args, **kwargs):
        def clear_file(file_path):
            # Open the file in write mode ('w') and immediately close it
            with open(file_path, 'w') as file:
                pass

        def write_string_to_file(file_path, text):
            # Clear the file before writing to it
            clear_file(file_path)

            # Open the file in write mode ('w')
            with open(file_path, 'w') as file:
                # Write the string to the file
                file.write(text)

        def read_file_contents(file_path):
            # Open the file in read mode ('r')
            with open(file_path, 'r') as file:
                # Read and return the contents of the file
                return file.read()

        file_path = FILE_PATH + 'fetcher.txt'

        first_id = None

        if not os.path.exists(file_path):
            first_id = str(Inbox.objects.all().order_by("id").first().id)
        else:
            first_id = read_file_contents(file_path)

        # a = 1
        # return
        #
        # i = 263086-1
        # result = Inbox.objects.all().order_by("id")[263086:350000]
        # result = Inbox.objects.filter(currentPositionID=710).order_by("-id")
        last_id = str(Inbox.objects.all().order_by("-id").first().id)
        els = InboxSerializer()

        while last_id != first_id:
            inbox_instance = Inbox.objects.get(id=first_id)
            inbox_instance_serial = InboxSerializer(instance=inbox_instance)
            try:
                els.addToElastic(
                    inbox_instance,
                    inbox_instance_serial,
                    inbox_instance_serial.data["reciever"])
                print("Captured %s" % (inbox_instance_serial['id'],))
            except Exception as e:
                print("Error In  '%s'" % (e,))
            write_string_to_file(file_path, str(inbox_instance.id))
            first_id = str(Inbox.objects(id__gt=first_id).order_by("id").limit(1).first().id)

        # els = InboxSerializer()

        # i = 0
        # for r in ccc:
        #     i += 1
        #     # if i > :
        #     _r = InboxSerializer(instance=r)
        #     try:
        #         els.addToElastic(
        #             r,
        #             _r,
        #             _r.data["reciever"])
        #         print("Captured %d" % (i,))
        #     except Exception as e:
        #         print("Error In  %d , '%s'" % (i, e))
        #     # else:
        #     #     print("Captured %d BEFORE ! " % (i,))

        pass

    @list_route(methods=["get"])
    def readLetter(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        inboxInstance = Inbox.objects.get(
            id=request.query_params["id"],
            currentPositionID=pos.id
        )
        inboxSerial = self.serializer_class(
            data={"seen": True, },
            instance=inboxInstance,
            partial=True)
        inboxSerial.is_valid(raise_exception=True)
        inboxSerial.update(instance=inboxInstance, validated_data=inboxSerial.validated_data)
        return Response({})

    @list_route(methods=["get"])
    def unreadLetter(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        inboxInstance = Inbox.objects.get(
            id=request.query_params["id"],
            currentPositionID=pos.id
        )
        inboxSerial = self.serializer_class(
            data={"seen": False, },
            instance=inboxInstance,
            partial=True)
        inboxSerial.is_valid(raise_exception=True)
        inboxSerial.update(instance=inboxInstance, validated_data=inboxSerial.validated_data)
        return Response({})

    @detail_route(methods=['get'])
    def downloadAttachment(self, request, *args, **kwargs):
        # getting inbox instances
        self.queryset = self.get_queryset()
        inboxInstance = self.queryset.get(id=kwargs['id'])
        # getting attachment
        atts = inboxInstance.letter['exp'].get('extraAttachments', None)
        if atts == None:
            letterIns = Letter.objects.get(id=inboxInstance.letter['id'])
            atts = letterIns.attachments
            pass

        # getting created user id
        userID = inboxInstance.letter["creatorPosition"]["userID"]
        # getting files list to compress
        fileClass = FileManager(userID)
        fileView = FileUploadViewSet()
        for a in atts:
            a["path"] = fileView.getPath(
                a["imgLink"].split("_")[1] if len(a["imgLink"].split("_")) > 1 else a["imgLink"])
            a["name"] = a["imgInf"]["name"]
            a["type"] = "file"
        filename = fileClass.MakeFilesCompress(atts)
        chunk_size = 8192
        response = StreamingHttpResponse(FileWrapper(open(filename, 'rb'), chunk_size),
                                         content_type=mimetypes.guess_type(filename)[0])
        response['Content-Length'] = os.path.getsize(filename)
        response['Content-Disposition'] = "attachment; filename=%s" % "download.zip"
        # os.remove(filename)
        return response

    @list_route(methods=["get"])
    def getLetterPrev(self, request, *args, **kwargs):
        # self.checkInboxMatch_MongoAndElasticAndHistroyAndNotification(request)
        pos = Position.objects.get(
            user=request.user,
            company=request.user.current_company)
        inboxInstance = Inbox.objects.get(
            id=request.query_params["id"],
            currentPositionID=pos.id)
        result = self.serializer_class(instance=inboxInstance)
        result = result.data
        if 'sign' in result['letter']:
            if 'generatedFileAddr' in result['letter']['sign']:
                result['letter']['sign']['generatedFileAddr'] = \
                    result['letter']['sign']['generatedFileAddr'].split("/")[
                        len(result['letter']['sign']['generatedFileAddr'].split("/")) - 1]
                result['letter']['sign']['generatedFileAddr'] = "/api/v1/file/upload?q=" + result['letter']['sign'][
                    'generatedFileAddr']

        if result["dateOfCreate"]:
            result["dateOfCreate"] = mil_to_sh_with_time(result["dateOfCreate"])
        if result["dateOfObservable"]:
            result["dateOfObservable"] = mil_to_sh_with_time(result["dateOfObservable"])
        result['sender']['avatar'] = result['sender']['avatar'].replace("50CC", "100")
        result['reciever']['avatar'] = result['reciever']['avatar'].replace("50CC", "100")
        result['letter']['body'] = result['letter']['body'].replace("&nbsp;", " ")
        # getting all hamesh
        hamesh = Inbox.objects.filter(letter__id=Letter.objects.get(id=result['letter']['id']).id)
        result['hameshHistory'] = []

        for h in hamesh:
            if h.reciever.get('option', {}).get('hamesh', '') != '':
                if h.reciever.get('option', {}).get('security', 0) in [0, 1]:
                    result['hameshHistory'].append(
                        {
                            'sender': h.sender.get('profileName', '') + ' ' + h.sender.get('chartName', ''),
                            'dateOf': mil_to_sh_with_time(h.dateOfObservable, ''),
                            'message': h.reciever.get('option', {}).get('hamesh', ''),
                            'rec': h.reciever.get('profileName', '') + ' ' + h.reciever.get('chartName', '')
                        }
                    )

        return Response(result)

    @detail_route(methods=["get"])
    def moveToArchive(self, request, *args, **kwargs):
        self.archiveIt(request, kwargs["id"])
        return Response({})

    @list_route(methods=["get"])
    def getHameshHistory(self, request, *args, **kwargs):
        currentPosDoc = GetPositionViewset().GetCurrentPositionDocumentInstance(request).positionID

        hameshs = list(
            InboxHistory.objects.aggregate(
                {
                    '$match': {
                        '$and': [
                            {'recieverDetail.hamesh': {'$ne': ''}},
                            {'recieverDetail.hamesh': {'$ne': None}},
                            {'recieverDetail.hamesh': {'$ne': 'null'}},
                            {'senderDetail.positionID': currentPosDoc}
                        ]
                    }

                },
                {
                    '$project':
                        {
                            'ss': '$recieverDetail.hamesh'}
                },
                {'$sort': {'_id': -1}},
                {'$group': {'_id': '$ss'}},
                {'$limit': 30}
            )

        )
        hameshs = [x['_id'] for x in hameshs]

        return Response(hameshs)

    def archiveIt(self, request, inboxID):
        pos = Position.objects.get(
            user=request.user,
            company=request.user.current_company)
        # getting inbox instance
        inboxInstance = Inbox.objects.get(
            id=inboxID,
            currentPositionID=pos.id)
        inboxUpdateSerial = InboxSerializer(instance=inboxInstance,
                                            data={"itemPlace": 2},
                                            partial=True)
        inboxUpdateSerial.is_valid(raise_exception=True)
        inboxUpdateSerial.update(inboxInstance, inboxUpdateSerial.validated_data)

    @detail_route(methods=["get"])
    def moveFromArchive(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        # getting inbox instance
        inboxInstance = Inbox.objects.get(
            id=kwargs["id"],
            currentPositionID=pos.id)
        inboxUpdateSerial = InboxSerializer(instance=inboxInstance,
                                            data={"itemPlace": 1},
                                            partial=True)
        inboxUpdateSerial.is_valid(raise_exception=True)
        inboxUpdateSerial.update(inboxInstance, inboxUpdateSerial.validated_data)
        return Response({})

    @detail_route(methods=["get"])
    def moveToTrash(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        # getting inbox instance
        inboxInstance = Inbox.objects.get(
            id=kwargs["id"],
            currentPositionID=pos.id)

        inboxUpdateSerial = InboxSerializer(instance=inboxInstance,
                                            data={"itemPlace": 3},
                                            partial=True)
        inboxUpdateSerial.is_valid(raise_exception=True)
        inboxUpdateSerial.update(inboxInstance, inboxUpdateSerial.validated_data)

        return Response({})

    @list_route(methods=["post"])
    def MoveSelectedToTrash(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        for i in request.data:
            inboxInstance = Inbox.objects.get(
                id=i,
                currentPositionID=pos.id)

            inboxUpdateSerial = InboxSerializer(instance=inboxInstance,
                                                data={"itemPlace": 3},
                                                partial=True)
            inboxUpdateSerial.is_valid(raise_exception=True)
            inboxUpdateSerial.update(inboxInstance, inboxUpdateSerial.validated_data)
        return Response({})

    @list_route(methods=["get"])
    def GetLastInboxID(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)

        res = Inbox.objects.filter(currentPositionID=pos.id).order_by("-id").limit(1)
        result = {}
        if res.count() == 0:
            result["r"] = 0
        else:
            result["r"] = str(res[0].id)

        return Response(result)

    @list_route(methods=["post"])
    def MoveSelectedToArchive(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=request.user,
            company=request.user.current_company)
        for i in request.data:
            inboxInstance = Inbox.objects.get(id=i, currentPositionID=pos.id)
            inboxUpdateSerial = InboxSerializer(instance=inboxInstance,
                                                data={"itemPlace": 2},
                                                partial=True)
            inboxUpdateSerial.is_valid(raise_exception=True)
            inboxUpdateSerial.update(inboxInstance, inboxUpdateSerial.validated_data)
        return Response({})

    @list_route(methods=["post"])
    def ChangeStar(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        # getting inbox instance
        inboxInstance = Inbox.objects.get(
            id=request.data["inboxId"],
            currentPositionID=pos.id)

        inboxUpdateSerial = InboxSerializer(instance=inboxInstance,
                                            data={"star": not inboxInstance.star},
                                            partial=True)
        inboxUpdateSerial.is_valid(raise_exception=True)
        inboxUpdateSerial.update(inboxInstance, inboxUpdateSerial.validated_data)

        return Response({})

        # getting inbox instance

    """
    here is security problem
    we have to set a permission
    not to allow people query from itemPlace=4
    another problem is denying all action from forwarding, replaying and etc..
    when itemPlace == 4

    tnx
    """

    @detail_route(methods=["get"])
    def deleteForEver(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=request.user,
            company=request.user.current_company)
        # getting inbox instance
        inboxInstance = Inbox.objects.get(
            id=kwargs["id"],
            currentPositionID=pos.id)

        inboxUpdateSerial = InboxSerializer(instance=inboxInstance,
                                            data={"itemPlace": 4},
                                            partial=True)
        inboxUpdateSerial.is_valid(raise_exception=True)
        inboxUpdateSerial.update(inboxInstance, inboxUpdateSerial.validated_data)

        return Response({})

    """
    while we are testing sometimes maybe we delete something independently
     this method bind these four items
     MongoDB Inbox
     Elastic
     Notofications
     InboxHistory
    """

    @list_route(methods=["get"])
    def checkInboxMatch_MongoAndElasticAndHistroyAndNotification(self, request):
        # starting with mongo
        # getting all user positionIDs
        pos = Position.objects.filter(user=request.user)
        pos = [x["id"] for x in list(pos.values("id"))]

        mongoInboxItems = Inbox.objects.filter(currentPositionID__in=pos)
        mongoInboxIDs = [str(x.id) for x in mongoInboxItems.only("id")]
        for inbox in mongoInboxItems:
            es = getElasticSearch()
            for p in pos:
                indexName = "inbox_%s" % (p,)
                try:
                    s = Search(using=es, index=indexName, ).query(id__in=mongoInboxIDs[1:3]).execute()
                    s = s
                except NotFoundError:
                    continue
                except RequestError:
                    continue

    @detail_route(methods=["post"])
    def removeHistoryUnseen(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        inboxInstance = Inbox.objects.get(
            id=kwargs["id"],
            currentPositionID=pos.id)

        # just allowded to remove 3 of item for hacking purpose
        recieverInboxInstance = Inbox.objects.filter(
            id=request.data['recieverDetail']['inboxID'],
            sender__positionID=pos.id,
            seen=False).limit(3)

        # deleting from elastic
        # deleting from history
        # deleting from notifications

        if (recieverInboxInstance[0].itemType == 5):
            return Response({"msg": "رونوشت اتوماتیک را نمی توانید حذف کنید"})

        InboxHistory.objects.get(id=request.data['id']).delete()

        InboxSerializer().removeFromElastic(
            recieverInboxInstance[0].currentPositionID, str(recieverInboxInstance[0].id))

        recieverInboxInstance.delete()

        Notifications.objects.filter(extra__inboxID=request.data['recieverDetail']['inboxID']).delete()
        NotificationViewSet().changesHappened(request.user.id)

        return Response({})

    """
    docType
    1 = usual
    2 = draft
    3 = trash !! :))
    itemActivityMode
    1 = usual
    2 = as replay
    3 = as forward
    itemMode
    1 = usual
    2 = automated
    itemType
    1 = usual sent
    2 = first sender


    """

    def handleHistoryExplanation(self, historyItemDict):
        docType = historyItemDict["docType"]
        itemActivityMode = historyItemDict["itemActivityMode"]
        itemMode = historyItemDict["itemMode"]
        itemType = historyItemDict["itemType"]
        currentInboxInstance = Inbox.objects.get(id=historyItemDict["currentInboxId"])
        message = ""

        def mapLetterType(letterType):
            if letterType == 1:
                return "نامه داخلی"
            if letterType == 2:
                return "نامه صادره"
            if letterType == 3:
                return "نامه وارده"
            if letterType == 7:
                return "پیش نویس داخلی"
            if letterType == 8:
                return "پیش نویس صادره"
            if letterType == 9:
                return "پیش نویس وارده"

        if (docType == 1 and itemActivityMode == 1 and itemMode == 1 and itemType == 2):
            message = "این <strong style='text-decoration: underline;'>%s</strong>  توسط <strong style='color:blue'>%s</strong> مورخه %s برای اولین بار ثبت شده است" % (
                mapLetterType(currentInboxInstance.letter["letterType"]),
                historyItemDict["senderDetail"]["name"] + " - " + historyItemDict["senderDetail"]["chart"],
                mil_to_sh_with_time(historyItemDict["senderDetail"]["date"], splitter="-"),
            )

        if (docType == 1 and itemActivityMode == 1 and itemMode == 1 and itemType == 1):
            message = "این <strong style='text-decoration: underline;'>%s</strong> توسط <strong style='color:blue'>%s</strong> مورخه %s به <strong style='color:blue'>%s</strong> ارسال شده است" % (
                mapLetterType(currentInboxInstance.letter["letterType"]),
                historyItemDict["senderDetail"]["name"] + " - " + historyItemDict["senderDetail"]["chart"],
                mil_to_sh_with_time(historyItemDict["senderDetail"]["date"], splitter="-"),
                historyItemDict["recieverDetail"]["name"] + " - " + historyItemDict["recieverDetail"]["chart"],
            )

        if (docType == 1 and itemActivityMode == 3 and itemMode == 1 and itemType == 1):
            message = "این <strong style='text-decoration: underline;'>%s</strong> توسط <strong style='color:blue'>%s</strong> مورخه %s به <strong style='color:blue'>%s</strong> ارجاع شده است" % (
                mapLetterType(currentInboxInstance.letter["letterType"]),
                historyItemDict["senderDetail"]["name"] + " - " + historyItemDict["senderDetail"]["chart"],
                mil_to_sh_with_time(historyItemDict["senderDetail"]["date"], splitter="-"),
                historyItemDict["recieverDetail"]["name"] + " - " + historyItemDict["recieverDetail"]["chart"],
            )

        if (docType == 1 and itemActivityMode == 1 and itemMode == 2 and itemType == 1):
            mainReciever = {
                "chartName": "",
                "inboxID": "",
                "positionID": "",
                "profileName": "",
            }
            if 'thisAutoSupposeToRecievedBy' in currentInboxInstance.reciever:
                mainReciever = currentInboxInstance.reciever["thisAutoSupposeToRecievedBy"]
            message = "این <strong style='text-decoration: underline;'>%s</strong> توسط <strong style='color:blue'>%s</strong> مورخه %s به <strong style='color:blue'>%s</strong> ارجاع یا ارسال و <strong style='text-decoration: underline;color:green;'>رونوشت خودکار</strong> آن به <strong style='color:red'>%s</strong> ارجاع شده است" % (
                mapLetterType(currentInboxInstance.letter["letterType"]),
                historyItemDict["senderDetail"]["name"] + " - " + historyItemDict["senderDetail"]["chart"],
                mil_to_sh_with_time(historyItemDict["senderDetail"]["date"], splitter="-"),
                mainReciever["profileName"] + ' - ' + mainReciever["chartName"],
                str(historyItemDict["recieverDetail"]["name"]) + " - " + str(
                    historyItemDict["recieverDetail"]["chart"]) if mainReciever["chartName"] else "",
            )
        if (docType == 1 and itemActivityMode == 1 and itemMode == 1 and itemType == 1):
            pass

        if (docType == 1 and itemActivityMode == 1 and itemMode == 1 and itemType == 1):
            pass

        if (docType == 1 and itemActivityMode == 1 and itemMode == 1 and itemType == 1):
            pass

        historyItemDict["message"] = message

        return historyItemDict

    """
    Recursive method for generating history tree for json
    """

    @detail_route(methods=["get"])
    def history(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        inboxInstance = Inbox.objects.get(
            id=kwargs["id"],
            currentPositionID=pos.id)

        historyList = \
            InboxHistory.objects.filter(
                letterID=inboxInstance.letter["id"],
                recieverDetail__security__in=[None, 0, 1, 2],
                recieverDetail__cc__in=[None, False, ""],
            ).order_by("id")
        # if inboxInstance.letter['letterType'] ==
        starterInstace = InboxHistory.objects.filter(letterID=inboxInstance.letter["id"], itemType=2)
        if starterInstace.count() < 1:
            starterInstace = InboxHistory.objects.filter(letterID=inboxInstance.letter["id"]).order_by("-id")
        starter = starterInstace[0]  # raise error s
        starter = LetterHistorySerializer(instance=starterInstace[0]).data
        starter = self.handleHistoryExplanation(starter)
        historyList = LetterHistorySerializer(instance=historyList, many=True).data
        # cleaning history list
        tempList = []
        for hl in historyList:
            addIt = True
            if hl["docType"] == 1 and hl["itemType"] == 1 and hl["itemMode"] == 1 and hl["itemActivityMode"] == 1:
                if "recieverDetail" in hl:
                    if "positionID" in hl["recieverDetail"]:
                        if "senderDetail" in hl:
                            if "positionID" in hl["senderDetail"]:
                                if hl["senderDetail"]["positionID"] == hl["recieverDetail"]["positionID"]:
                                    addIt = False
            if addIt:
                tempList.append(hl)
        historyList = tempList
        del hl
        del tempList

        for h in historyList:
            h = self.handleHistoryExplanation(h)

        historyListRAW = InboxHistory.objects.filter(
            letterID=inboxInstance.letter["id"],
            recieverDetail__security__in=[None, 0, 1, 2],
            recieverDetail__cc__in=[None, False, ""],
        ).order_by("-itemType", "id")
        historyListRAW = historyList

        def getChildren(starter, posID):
            re = []
            for h in historyList:
                # if h["itemType"] != 2:
                if True:
                    if starter['currentInboxId'] == h['previousInboxId']:
                        res = h
                        if h['recieverDetail']['security'] == 2:
                            h['recieverDetail']['hamesh'] = "************"
                        res['children'] = getChildren(h, posID)
                        res['can_remove'] = (res['senderDetail']['positionID'] == posID) and (
                            not res["recieverDetail"]["seen"])
                        re.append(res)
            if len(re) > 0: return re

        starter["children"] = getChildren(starter, pos.id)

        def getJustInboxIDs(top):
            ss = []
            ss.append(top["currentInboxId"])
            if "children" in top:
                if top["children"] != None:
                    if len(top["children"]) > 0:
                        for c in top["children"]:
                            ss = ss + getJustInboxIDs(c)
            return ss

        ss = getJustInboxIDs(starter)
        cc = []
        for s in ss:
            for h in historyListRAW:
                h["avatar"] = None
                if h["currentInboxId"] == s:
                    if h["itemType"] == 2:
                        if "avatar" in h:
                            if h["avatar"]:
                                h["avatar"] = h["senderDetail"]["avatar"].replace("50CC", "50")
                    else:
                        if "recieverDetail" in h:
                            if "avatar" in h["recieverDetail"]:
                                if h["recieverDetail"]["avatar"]:
                                    h["avatar"] = h["recieverDetail"]["avatar"].replace("50CC", "50")

                    cc.append(h)

        starter["RAW"] = cc

        bodyStr = json.dumps(starter, default=defaultMorabaa)
        return HttpResponse(bodyStr, content_type="application/json")
