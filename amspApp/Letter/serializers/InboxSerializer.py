import copy
import json
from datetime import datetime

import bson
from asq.initiators import query
from dateutil import parser
from django.core.cache import cache

from amsp import settings
from amspApp.CompaniesManagment.Charts.models import Chart
from amspApp.CompaniesManagment.Positions.models import Position, PositionsDocument
from amspApp.CompaniesManagment.Positions.serializers.PositionSerializer import PositionDocumentSerializer
from amspApp.CompaniesManagment.Secretariat.viewes.SecretariatsViews import SecretariatsViewSet
from amspApp.Infrustructures.Classes import DateConvertors
from amspApp.Infrustructures.Classes.DateConvertors import convertJerkStrDateTime, sh_to_mil
from amspApp.Infrustructures.Classes.RemoveHtml import strip_tags
from amspApp.Letter.elasticConn import getElasticSearch
from amspApp.Letter.models import Inbox, Letter, InboxHistory
from amspApp.Letter.serializers.LetterHistorySerializer import LetterHistorySerializer
from amspApp.Notifications.models import Notifications
from amspApp.Notifications.serializers.NotificationSerializer import NotificationsSerializer
from amspApp.Notifications.views.NotificationView import NotificationViewSet
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer
from amspApp.tasks import saveToElastic, updateToElastic


class InboxSerializer(DynamicFieldsDocumentSerializer):
    autoHameshList = []

    class Meta:
        model = Inbox

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    def getElastic(self, inboxInstance, positionID):
        es = getElasticSearch()
        dabirkhaneh_itemModes = [5, 6, 9, 10, 11, 12]
        indexName = settings.ELASTIC_INBOX_INDEXING_NAME + str(positionID)
        if inboxInstance.itemMode in dabirkhaneh_itemModes:
            indexName = settings.ELASTIC_SEC_INDEXING_NAME + str(inboxInstance.letter['secretariatID'])
        es.indices.create(index=indexName, ignore=400)

        return {"elastic": es, "indexName": indexName}

    def removeExtraPersonDetails(self, person):
        if "chartID" in person: del person["chartID"]
        if "id" in person: del person["id"]
        if "last" in person: del person["last"]
        if "positionID" in person: del person["positionID"]
        if "postDate" in person: del person["postDate"]
        if "profileID" in person: del person["profileID"]
        if "userID" in person: del person["userID"]
        if "companyID" in person: del person["companyID"]
        if "defaultSec" in person: del person["defaultSec"]
        if "desc" in person: del person["desc"]
        if "hasBulkSentPermission" in person: del person["hasBulkSentPermission"]
        if "isPositionAllowedToSendDirectly" in person: del person["isPositionAllowedToSendDirectly"]
        if "isPositionIgonreAssistantHardSent" in person: del person["isPositionIgonreAssistantHardSent"]
        return person

    def removeExraSecretrait(self, secretrait):
        if "company" in secretrait: del secretrait["company"]
        if "dakheli_last_id" in secretrait: del secretrait["dakheli_last_id"]
        if "dakheli_letters_format" in secretrait: del secretrait["dakheli_letters_format"]
        if "id" in secretrait: del secretrait["id"]
        if "post_date" in secretrait: del secretrait["post_date"]
        if "sadere_last_id" in secretrait: del secretrait["sadere_last_id"]
        if "sadereh_letters_format" in secretrait: del secretrait["sadereh_letters_format"]
        if "varede_last_id" in secretrait: del secretrait["varede_last_id"]
        if "varede_letters_format" in secretrait: del secretrait["varede_letters_format"]
        return secretrait

    def removeExraSign(self, sign):
        if "id" in sign: del sign["id"]
        if "postDate" in sign: del sign["postDate"]
        if "position" in sign: self.removeExtraPersonDetails(sign["position"])
        return sign

    def removeLetterExpExtra(self, extra):
        if "recievers_id" in extra: del extra["recievers_id"]
        if "recievers_raw" in extra: del extra["recievers_raw"]
        if "extraAttachments" in extra:
            for e in extra["extraAttachments"]:
                if "imgInf" in e:
                    if "lastModified" in e["imgInf"]:
                        del e["imgInf"]["lastModified"]
                    if "type" in e["imgInf"]:
                        del e["imgInf"]["type"]
                    if "lastModified" in e["imgInf"]:
                        del e["imgInf"]["size"]
                    if "lastModified" in e["imgInf"]:
                        del e["imgInf"]["lastModifiedDate"]

        return extra

    def removeLettersExtra(self, letterBody):
        letterBody["hasAttachmant"] = False
        if "attachments" in letterBody:
            letterBody["hasAttachmant"] = bool(len(letterBody["attachments"]))
            del letterBody["attachments"]
        if "exp" in letterBody and not (letterBody["hasAttachmant"]):
            if "extraAttachments" in letterBody["exp"]:
                letterBody["hasAttachmant"] = bool(len(letterBody["exp"]["extraAttachments"]))
                del letterBody["exp"]["extraAttachments"]

        if "attachments" in letterBody:
            del letterBody["attachments"]
        if "creatorPosition" in letterBody:
            letterBody["creatorPosition"] = self.removeExtraPersonDetails(letterBody["creatorPosition"])
        if "secretariat" in letterBody:
            letterBody["secretariat"] = self.removeExraSecretrait(letterBody["secretariat"])
        if "secretariatPermission" in letterBody:
            del letterBody["secretariatPermission"]

        if "sign" in letterBody:
            letterBody["sign"] = self.removeExraSign(letterBody["sign"])

        if "exp" in letterBody:
            letterBody["exp"] = self.removeLetterExpExtra(letterBody["exp"])

        if "recievers" in letterBody:
            for r in letterBody["recievers"]:
                r = self.removeExtraPersonDetails(r)

        if "creatorPositionID" in letterBody: del letterBody["creatorPositionID"]
        if "id" in letterBody: del letterBody["id"]
        if "letterType" in letterBody: del letterBody["letterType"]
        if "others" in letterBody: del letterBody
        if "secretariatID" in letterBody: del letterBody["secretariatID"]
        if "secretariatPermissionID" in letterBody: del letterBody["secretariatPermissionID"]

        return letterBody

    def removeInboxExtra(self, body):
        if "other" in body: del body["other"]
        if "previousInboxId" in body: del body["previousInboxId"]
        if "readTimes" in body: del body["readTimes"]
        if "replyedInbox" in body: del body["replyedInbox"]

        return body

    def removeExtraCompany(self, companyReciever):
        if "companyID" in companyReciever: del companyReciever["companyID"]
        if "details" in companyReciever: del companyReciever["details"]
        if "group" in companyReciever: del companyReciever["group"]
        if "id" in companyReciever: del companyReciever["id"]
        if "postDate" in companyReciever: del companyReciever["postDate"]
        if "postPositionID" in companyReciever: del companyReciever["postPositionID"]
        return companyReciever

    def removeExtraHamesh(self, Hamesh):
        if "avatar" in Hamesh: del Hamesh["avatar"]
        if "chartID" in Hamesh: del Hamesh["chartID"]
        if "companyName" in Hamesh: del Hamesh["companyName"]
        if "hamesh" in Hamesh: del Hamesh["hamesh"]
        if "id" in Hamesh: del Hamesh["id"]
        if "positionID" in Hamesh: del Hamesh["positionID"]
        if "profileID" in Hamesh: del Hamesh["profileID"]
        if "userID" in Hamesh: del Hamesh["userID"]
        return Hamesh

    def removeAllExtra(self, body):
        if "recievers" in body:
            body["recievers"] = self.removeExtraPersonDetails(body["recievers"])
            if "others" in body["recievers"]:
                for r in body["recievers"]["others"]:
                    r = self.removeExtraPersonDetails(r)

        if "letter" in body:
            body["letter"] = self.removeLettersExtra(body["letter"])

        if "sender" in body:
            body["sender"] = self.removeExtraPersonDetails(body["sender"])
        body = self.removeInboxExtra(body)

        if "letter" in body:
            if "exp" in body["letter"]:
                if "export" in body["letter"]["exp"]:
                    if "companyRecievers" in body["letter"]["exp"]["export"]:
                        for r in body["letter"]["exp"]["export"]["companyRecievers"]:
                            r = self.removeExtraCompany(r)

                    if "hameshRecievers" in body["letter"]["exp"]["export"]:
                        for r in body["letter"]["exp"]["export"]["hameshRecievers"]:
                            r = self.removeExtraHamesh(r)
        return body

    def addToElastic(self, inboxInstance, inboxSerial, recieverPerson):
        # es = Elasticsearch()
        # dabirkhaneh_itemModes = [5, 6, 9, 10, 11, 12]
        # indexName = settings.ELASTIC_INBOX_INDEXING_NAME + str(recieverPerson["positionID"])
        # if inboxInstance.itemMode in dabirkhaneh_itemModes:
        #     indexName = settings.ELASTIC_SEC_INDEXING_NAME + str(inboxInstance.letter['secretariatID'])
        #
        # es.indices.create(index=indexName, ignore=400)

        """
        id
        itemMode
        itemPlace
        itemType
        seen
        sender.avatar
        sender.profileName
        sender.profileName
        sender.chartName

        letter.senderCompanyName
        letter.hasAttachmant
        letter.senderCompanyGroup
        letter.body

        reciever.others[0].chartName
        reciever.others[0].profileName

        dateOfObservable
        folders // folder.name & folder.id
        labels //  label.name & label.id & label.bgcolor & label.color

        """

        # elastic = self.getElastic(inboxInstance, recieverPerson["positionID"])
        #
        # es = elastic["elastic"]

        def defaultDecoder(obj):
            if type(obj) == bson.dbref.DBRef:
                return str(obj.id)

        # dt = {}
        # dt["id"] = str(inboxInstance.id)
        # dt["itemMode"] = inboxInstance.itemMode
        # dt["itemPlace"] = inboxInstance.itemPlace
        # dt["itemType"] = inboxInstance.itemType
        # dt["seen"] = False
        # dt["sender"] = {}
        # dt["sender"]['avatar'] = inboxInstance.sender.get('avatar')
        # dt["sender"]['profileName'] = inboxInstance.sender.get('profileName')
        # dt["sender"]['profileName'] = inboxInstance.sender.get('profileName')
        # dt["sender"]['chartName'] = inboxInstance.sender.get('chartName')
        #
        # dt["recievers"] = {}
        # dt["recievers"]['avatar'] = inboxInstance.reciever.get('avatar')
        # dt["recievers"]['profileName'] = inboxInstance.reciever.get('profileName')
        # dt["recievers"]['profileName'] = inboxInstance.reciever.get('profileName')
        # dt["recievers"]['chartName'] = inboxInstance.reciever.get('chartName')

        bodyStr = json.dumps(inboxSerial.data, default=defaultDecoder)
        body = json.loads(bodyStr)
        body["any"] = ', '.join("{%s}" % (val,) for val in body.items()).replace("{", " ").replace("}",
                                                                                                   " ").replace("(",
                                                                                                                " ").replace(
            ")", " ").replace("'", " ").replace(",", " ").replace(":", " ")
        body["inboxId"] = str(inboxInstance.id)
        if 'letter' in body['letter']['sign']:
            body['letter']['sign'].pop('letter')
        body["other"] = ""
        if "letter" in body:
            if "exp" in body["letter"]:
                if "recievers_raw" in body["letter"]["exp"]:
                    body['letter']['exp']['recievers_raw'] = json.dumps(body['letter']['exp']['recievers_raw'])

        # removing enoying items for reducing :

        self.removeAllExtra(body)

        # updating some datefield
        if "letter" in body:
            if "exp" in body["letter"]:
                if "dateOfSent" in body["letter"]["exp"]:
                    if body["letter"]["exp"]["dateOfSent"]:
                        body["letter"]["exp"]["dateOfSent"] = sh_to_mil(
                            body.get("letter", {}).get("exp", {}).get("dateOfSent", datetime.now()))

        for pp in body.get('reciever', {}).get('others', []):
            if pp.get('last', None) is not None:
                for cc in pp.get('last', []):
                    # cc['dateof'] = ''  # I don't know why , but elastic search make an error because of this
                    del cc['dateof']  # I don't know why , but elastic search make an error because of this

        # es.index(index=elastic["indexName"], doc_type="inbox", id=str(inboxInstance.id), body=body, request_timeout=150)

        saveToElastic(
            _positionID=recieverPerson["positionID"],
            _secretariatID=str(inboxInstance.letter['secretariatID']),
            _inboxInstance_itemMode=inboxInstance.itemMode,
            _doc_type="inbox",
            _inboxInstance_id=str(inboxInstance.id),
            _body=body
        )

    def SaveToSentFolder(self, letterInstance):
        return self.SendToInbox(
            person=letterInstance.creatorPosition,
            letterInstance=letterInstance,
            itemType=6,
            replyedInbox={},
            itemMode=7,
            previousInboxId=None
        )

    def SaveToForwardFolder(
            self,
            currentPositionInstance,
            currentInboxInstance,
            letterInstace,
            recievers):
        positionProfileInstance = PositionsDocument.objects.get(positionID=currentPositionInstance.id)
        person = PositionDocumentSerializer(instance=positionProfileInstance).data

        return self.SendToInbox(
            person=person,
            letterInstance=letterInstace,
            itemType=9,
            itemMode=8,
            replyedInbox={},
            previousInboxId=str(currentInboxInstance.id),
            forwardRecievers=recievers)

    def SaveToSentFolderAsExport(self, letterInstance):
        return self.SendToInbox(
            person=letterInstance.creatorPosition,
            letterInstance=letterInstance,
            itemType=8,
            replyedInbox={},
            itemMode=9,
            previousInboxId=None
        )

    def SaveToRecFolderAsImport(self, letterInstance):
        return self.SendToInbox(
            person=letterInstance.creatorPosition,
            letterInstance=letterInstance,
            itemType=10,
            replyedInbox={},
            itemMode=10,
            previousInboxId=None
        )

    def SaveToTemplateAsExport(self, letterInstance):
        return self.SendToInbox(
            person=letterInstance.creatorPosition,
            letterInstance=letterInstance,
            itemType=8,
            replyedInbox={},
            itemMode=11,
            previousInboxId=None
        )

    def SaveToDraftAsExport(self, letterInstance):
        return self.SendToInbox(
            person=letterInstance.creatorPosition,
            letterInstance=letterInstance,
            itemType=8,
            replyedInbox={},
            itemMode=5,
            previousInboxId=None
        )

    """
    letter.letterType :
        1= Dakheli
        2= Sadereh
        3= Varedeh
        4= Document
        5= Message
        6= report
        7= draft dekheli
        8= draft sadere
        9= draft varedeh


    letter.security :
        1= addi
        2= mahramaneh
        3= serri


    letter.periority :
        1= addi
        2= forri
        3= kheili forri

    inbox.reciever.security :
        1= addi
        2= mahramaneh
        3= serri


    inbox.reciever.periority :
        1= addi
        2= forri
        3= kheili forri


    inbox.itemType:
        1 = this inbox item received and sent by some one else as usual inside letter
        2 = this inbox item is sent to a user and an inbox item listed in send letters
        3 = this inbox item forwarded // even if draft or dakheli
        4 = this inbox item is replied one, i mean this letter is a replay letter
        5 = this inbox item is auto send inbox as rooneveshte khodkar
        6 = this is first and beginner of a letter
        7 = no Type // this is for storing draft
        8 = this inbox item is sent as exported letter

    inbox.itemMode :
        1= dakheli
        2= rooneveshte sadereh
        3= rooneveshte varedeh
        4= draft
        5= draft sadere
        6= draft varedeh
        7= dakheli first send

    inbox.itemPlace :
        1= item in inboxes public folders
        2= item in archive
        3= item in trash
        4= item in trash and hide !

        """

    def Forward(self, SenderPisitionInstance, Recievers, InboxInstance):
        letterInstance = Letter.objects.get(id=InboxInstance["letter"]["id"])

        self.SaveToForwardFolder(SenderPisitionInstance, InboxInstance, letterInstance, Recievers)
        for p in Recievers:
            p["inboxID"] = str(InboxInstance.id)  # refers to previous inbox

        for person in Recievers:
            # person["inboxID"] = str(InboxInstance.id)  # refers to previous inbox
            itemMode = 1  # default item mode is dakheli
            # to handle forwarding drafts
            if letterInstance.letterType == 7:
                itemMode = 4
            # ----------------------------
            ff = self.SendToInbox(
                person=person,
                letterInstance=letterInstance,
                itemType=3,
                replyedInbox={},
                itemMode=itemMode,
                sender=InboxInstance.reciever,
                previousInboxId=InboxInstance.id,
                forwardRecievers=Recievers
            )
            self.AutoHameshList(ff, letterInstance)

    """
    this def adds statics to the counter cache
    if cache found , it will be updated the specific field
    else create statics from inbox // heavy process

    """

    def GenerateCounterCatch(self, positionId, cacheName):

        positionInstance = Position.objects.filter(id=positionId)
        if positionInstance.count() == 0:
            return None
        positionInstance = positionInstance[0]
        defaultSecratriat = SecretariatsViewSet().GetDefaultSecretariatInstanceByPositionInstance(positionInstance)

        # Inbox count
        AllInboxCount = Inbox.objects.filter(
            itemType__in=[1, 2, 3, 4, ],
            itemMode__in=[1, 2, 3],
            itemPlace__in=[1],
            currentPositionID=positionId,
            letter__secretariat__id=defaultSecratriat.secretariat.id
        ).count()
        AllInboxCountUnSeen = Inbox.objects.filter(
            itemType__in=[1, 2, 3, 4, ],
            itemMode__in=[1, 2, 3],
            itemPlace__in=[1],
            currentPositionID=positionId,
            seen=False,
            letter__secretariat__id=defaultSecratriat.secretariat.id

        ).count()
        # -------------

        # Sent count
        AllSentCount = Inbox.objects.filter(
            itemType__in=[6],
            itemMode__in=[7],
            itemPlace__in=[1],
            currentPositionID=positionId,
            letter__secretariat__id=defaultSecratriat.secretariat.id

        ).count()
        # -------------

        # Draft count
        AllDraftCount = Inbox.objects.filter(
            itemType__in=[7],
            itemMode__in=[4, 5, 6],
            itemPlace__in=[1],
            currentPositionID=positionId,
            letter__secretariat__id=defaultSecratriat.secretariat.id

        ).count()
        AllDraftCountUnSeen = Inbox.objects.filter(
            itemType__in=[7],
            itemMode__in=[4, 5, 6],
            itemPlace__in=[1],
            currentPositionID=positionId,
            seen=False,
            letter__secretariat__id=defaultSecratriat.secretariat.id

        ).count()
        # -------------

        # Archive count
        AllArchiveCount = Inbox.objects.filter(
            itemPlace__in=[2],
            currentPositionID=positionId,
            letter__secretariat__id=defaultSecratriat.secretariat.id

        ).count()
        AllArchiveCountUnSeen = Inbox.objects.filter(
            itemPlace__in=[2],
            currentPositionID=positionId,
            seen=False,
            letter__secretariat__id=defaultSecratriat.secretariat.id

        ).count()
        # ----------------

        # Trash count
        AllTrashCount = Inbox.objects.filter(
            itemPlace__in=[3],
            currentPositionID=positionId,
            letter__secretariat__id=defaultSecratriat.secretariat.id

        ).count()
        AllTrashCountUnSeen = Inbox.objects.filter(
            itemPlace__in=[3],
            currentPositionID=positionId,
            seen=False,
            letter__secretariat__id=defaultSecratriat.secretariat.id

        ).count()
        # ----------------

        # Automated count
        AllAutomatedCount = Inbox.objects.filter(
            itemType__in=[5],
            itemMode__in=[1, 2, 3, 4, 5, 6],
            itemPlace__in=[1],
            currentPositionID=positionId,
            letter__secretariat__id=defaultSecratriat.secretariat.id

        ).count()
        AllAutomatedCountUnSeen = Inbox.objects.filter(
            itemType__in=[5],
            itemMode__in=[1, 2, 3, 4, 5, 6],
            itemPlace__in=[1],
            currentPositionID=positionId,
            seen=False,
            letter__secretariat__id=defaultSecratriat.secretariat.id

        ).count()
        # ----------------
        res = {
            'ic': AllInboxCount,
            'icu': AllInboxCountUnSeen,
            'sc': AllSentCount,
            'dc': AllDraftCount,
            'dcu': AllDraftCountUnSeen,
            'ac': AllArchiveCount,
            'acu': AllArchiveCountUnSeen,
            'tc': AllTrashCount,
            'tcu': AllTrashCountUnSeen,
            'aac': AllAutomatedCount,
            'aacu': AllAutomatedCountUnSeen, }
        cache.set(cacheName, res, 9500)
        return res

    def UpdateCounterCatch(self, inboxInstance, cacheName):
        cacheInstance = cache.get(cacheName)
        if cacheInstance == None:
            cacheInstance = self.GenerateCounterCatch(inboxInstance.reciever['positionID'], cacheName)
        if ((inboxInstance.itemType in [1, 2, 3, 4]) and
                (inboxInstance.itemMode in [1, 2, 3]) and
                (inboxInstance.itemPlace in [1])):
            cacheInstance["ic"] += 1
        if ((inboxInstance.itemType in [1, 2, 3, 4]) and
                (inboxInstance.itemMode in [1, 2, 3]) and
                (inboxInstance.itemPlace in [1]) and
                (inboxInstance.seen == False)):
            cacheInstance["icu"] += 1
        # -------------------------
        # updatig send items count ...
        if ((inboxInstance.itemType in [6]) and
                (inboxInstance.itemMode in [7]) and
                (inboxInstance.itemPlace in [1])):
            cacheInstance["sc"] += 1
        # -------------------------
        # updatig draft count ...
        if ((inboxInstance.itemType in [7]) and
                (inboxInstance.itemMode in [4, 5, 6]) and
                (inboxInstance.itemPlace in [1])):
            cacheInstance["dc"] += 1
        if ((inboxInstance.itemType in [7]) and
                (inboxInstance.itemMode in [4, 5, 6]) and
                (inboxInstance.itemPlace in [1]) and
                (inboxInstance.seen == False)):
            cacheInstance["dcu"] += 1
        # -------------------------
        # updatig archiving count ...
        if (inboxInstance.itemPlace in [2]):
            cacheInstance["ac"] += 1
        if ((inboxInstance.itemPlace in [2]) and
                (inboxInstance.seen == False)):
            cacheInstance["acu"] += 1
        # -------------------------
        # updatig trash count ...
        if (inboxInstance.itemPlace in [3]):
            cacheInstance["tc"] += 1
        if ((inboxInstance.itemPlace in [3]) and
                (inboxInstance.seen == False)):
            cacheInstance["tcu"] += 1
        # -------------------------
        # updatig draft count ...
        if ((inboxInstance.itemType in [5]) and
                (inboxInstance.itemMode in [1, 2, 3, 4, 5, 6]) and
                (inboxInstance.itemPlace in [1])):
            cacheInstance["aac"] += 1
        if ((inboxInstance.itemType in [5]) and
                (inboxInstance.itemMode in [1, 2, 3, 4, 5, 6]) and
                (inboxInstance.itemPlace in [1]) and
                (inboxInstance.seen == False)):
            cacheInstance["aacu"] += 1
        # -------------------------
        cache.set(cacheName, cacheInstance, 9500)
        return cacheInstance

    def AddToCounters(self, inboxInstance):
        positionId = inboxInstance.currentPositionID
        cacheName = "inbox_static_" + str(positionId)
        cacheInstance = cache.get(cacheName)
        if cacheInstance:
            # updatig inbox count ...
            cacheInstance = self.UpdateCounterCatch(inboxInstance, cacheName)
            return cacheInstance

        res = self.GenerateCounterCatch(positionId, cacheName)

        return res

    def GetInboxCounter(self, positionInstance, oldStatic=None):
        cacheName = "inbox_static_" + str(positionInstance.id)
        cacheInstance = cache.get(cacheName)
        if cacheInstance == None:
            cacheInstance = self.GenerateCounterCatch(positionInstance.id, cacheName)
        return cacheInstance

    """
    we have so many actions here
    1: seen or not count
    2: archive count seen or not
    3: trash count seen or not
    """

    def UpdateCounterCatchMakeSeen(self, oldInstance, newInstance):
        positionId = newInstance.currentPositionID
        cacheName = "inbox_static_" + str(positionId)
        return self.GenerateCounterCatch(positionId, cacheName)

    def SaveToDraftFolder(self, letterInstance):
        return self.SendToInbox(
            person=letterInstance.creatorPosition,
            letterInstance=letterInstance,
            itemType=7,
            replyedInbox={},
            itemMode=4,
            previousInboxId=None
        )

    def removeBulkPersonKeys(self, item):
        if "companyID" in item: item.pop("companyID")
        if "companyName" in item: item.pop("companyName")
        if "defaultSec" in item: item.pop("defaultSec")
        if "hasBulkSentPermission" in item: item.pop("hasBulkSentPermission")
        if "isPositionAllowedToSendDirectly" in item: item.pop("isPositionAllowedToSendDirectly")
        if "isPositionIgonreAssistantHardSent" in item: item.pop("isPositionIgonreAssistantHardSent")
        if "others" in item: item.pop("others")
        if "others_count" in item: item.pop("others_count")
        if "desc" in item: item.pop("desc")
        return item

    def SendToInbox(self,
                    person,
                    letterInstance,
                    itemType,
                    replyedInbox,
                    itemMode,
                    sender=None,
                    previousInboxId=None,
                    forwardRecievers=None):

        """
        this line is very important in time of visibility
        if user set an invalid date it raise exception or replace it with current date
        """
        # pring("------------------------------------------------------------- inboxSerializer.py line 699")

        dateOfObservable = datetime.now()
        if "desc" in person:
            person.pop("desc")

        if "CurrentTime" in person:
            if len(person["CurrentTime"]) == 10:
                person["CurrentTime"] = convertJerkStrDateTime(person["CurrentTime"])
            dateOfObservable = DateConvertors.convertZoneToMilday(
                person["userID"],
                person["CurrentTime"],
            )
            if parser.parse(dateOfObservable) < datetime.now():
                dateOfObservable = datetime.now().strftime("%Y/%m/%d %H:%M")
            dateOfObservable = datetime.strptime(dateOfObservable, "%Y/%m/%d %H:%M")

        # pring("------------------------------------------------------------- inboxSerializer.py line 715")

        letterSum = strip_tags(letterInstance._data["body"])[:30]

        reciever = self.removeBulkPersonKeys(person)
        # this is for forward purposes
        if not forwardRecievers:
            reciever["others"] = [self.removeBulkPersonKeys(x) for x in letterInstance.recievers]
            reciever["others_count"] = len(letterInstance.recievers)
        else:
            reciever["others"] = [copy.copy(self.removeBulkPersonKeys(x)) for x in forwardRecievers]
            reciever["others_count"] = len(forwardRecievers)
        # pring("------------------------------------------------------------- inboxSerializer.py line 728")

        # reciever["others"] = [self.removeBulkPersonKeys(x) for x in reciever["others"]]

        letterSum = letterSum if letterSum != "" else " "
        newInbox = {
            'currentPositionID': person["positionID"],
            'dateOfObservable': dateOfObservable,
            'dateOfCreate': datetime.now(),
            'sender': self.removeBulkPersonKeys(
                letterInstance.creatorPosition) if sender == None else self.removeBulkPersonKeys(sender),
            'reciever': reciever,
            'letter': letterInstance._data,
            'letterSummery': letterSum,
            'labels': [],
            'readTimes': [],
            'seen': False,
            'itemType': itemType,
            'replyedInbox': replyedInbox,
            'previousInboxId': previousInboxId,
            'itemMode': itemMode
        }
        # this line is for supporting obj with None value
        if previousInboxId == None:
            newInbox.pop("previousInboxId", None)
        else:
            newInbox["previousInboxId"] = str(newInbox["previousInboxId"])
        # ----------------------------------------------
        # adding extra options to auto hamesh
        if itemType == 5:
            if "thisAutoSupposeToRecievedBy" in person:
                newInbox["reciever"]["thisAutoSupposeToRecievedBy"] = person["thisAutoSupposeToRecievedBy"]
        # pring("------------------------------------------------------------- inboxSerializer.py line 760")

        inboxSerial = InboxSerializer(data=newInbox)
        inboxSerial.is_valid(raise_exception=True)
        inboxInstance = inboxSerial.create(inboxSerial.validated_data)
        # pring("------------------------------------------------------------- inboxSerializer.py line 765")
        self.InboxNotification(inboxInstance)
        # pring("------------------------------------------------------------- inboxSerializer.py line 767")

        return inboxInstance

    def SendLetter(self, letterInstance, itemType=1, replyedInbox={}, itemMode=1, prevSenderInboxID=None):
        result = []
        # saving in draft part
        if letterInstance.letterType == 7:
            result = [self.SaveToDraftFolder(letterInstance)]
            return result

        # saving in particular part

        for person in letterInstance.recievers:
            ff = self.SendToInbox(
                person=person,
                letterInstance=letterInstance,
                itemType=itemType,
                replyedInbox=replyedInbox,
                itemMode=itemMode,
                previousInboxId=prevSenderInboxID)
            result.append(ff)

            # automatic roonevesht
            self.AutoHameshList(ff, letterInstance)

        return result

    """
    in this function i have to get sender and reciever position in chart
    then i have to retrieve all top headers
    """

    hameshPersonForDup = []

    def AutoHameshList(self, inboxInstance, letterInstance):
        # checking auto hamesh permission
        senderPosition = PositionsDocument.objects.get(id=inboxInstance.sender['id'])
        if "automation" in senderPosition.desc:
            if "permission" in senderPosition.desc['automation']:
                if "Dont_use_automated_copy_for_this_user" in senderPosition.desc['automation']["permission"]:
                    if senderPosition.desc['automation']['permission']['Dont_use_automated_copy_for_this_user'] == True:
                        return

        senderChartInstance = Chart.objects.get(id=inboxInstance.sender['chartID'])
        recieverChartInstance = Chart.objects.get(id=inboxInstance.reciever['chartID'])
        minusSet = [senderChartInstance.id, recieverChartInstance.id]
        topTop = []

        def getChartToTop(chartInstance):
            topchartInstance = chartInstance.top
            if topchartInstance != None:
                getChartToTop(topchartInstance)
            topTop.append(topchartInstance)

        getChartToTop(senderChartInstance)
        senderToTop = topTop
        topTop = []
        getChartToTop(recieverChartInstance)
        recieverChartToTop = topTop
        # this list extract just chart id to speedup distinct
        rCTT = query(recieverChartToTop).where(lambda x: x != None).select(lambda x: x.id).distinct().to_list()
        sTT = query(senderToTop).where(lambda x: x != None).select(lambda x: x.id).distinct().to_list()
        finalList = rCTT + sTT
        # finding duplicates to remove from lists
        # here i remove unnecessary charts
        dups = set([x for x in finalList if finalList.count(x) > 1])
        finalList = set(finalList) - set(dups)
        finalList = set(finalList) - set(minusSet)

        positions = PositionsDocument.objects.filter(
            chartID__in=finalList,
            userID__nin=[None],
            positionID__nin=[None])
        # recieverPersonProfile =
        self.hameshPersonForDup = []
        for p in positions:
            person = PositionDocumentSerializer(instance=p).data
            person["thisAutoSupposeToRecievedBy"] = {
                "profileName": inboxInstance.reciever['profileName'],
                "chartName": inboxInstance.reciever['chartName'],
                "positionID": inboxInstance.reciever['positionID'],
                "inboxID": str(inboxInstance.id),
            }
            # for protecting duplicated send via chart
            found = False
            for f in self.hameshPersonForDup:
                if person['id'] == f:
                    found = True
            if found == False:
                self.SendToInbox(
                    person=person,
                    letterInstance=letterInstance,
                    itemType=5,
                    replyedInbox=inboxInstance.replyedInbox,
                    itemMode=1,
                    previousInboxId=inboxInstance.previousInboxId)
                self.hameshPersonForDup.append(person["id"])
        return finalList

    def Janeshin(self):
        self = self
        pass

    def MasooleDaftar(self):
        self = self
        pass

    def create(self, validated_data):
        # pring("------------------------------------------------------------- serializer.py line 867")
        result = super(InboxSerializer, self).create(validated_data)
        inboxSerial = InboxSerializer(instance=result)
        # pring("------------------------------------------------------------- serializer.py line 870")

        self.addToElastic(
            result,
            inboxSerial,
            inboxSerial.data["reciever"])
        # pring("------------------------------------------------------------- serializer.py line 876")
        LetterHistorySerializer().createFromInbox(result)
        # pring("------------------------------------------------------------- serializer.py line 878")
        # self.AddToCounters(result)
        # pring("------------------------------------------------------------- serializer.py line 880")
        return result

    """
    This def is for :
    1st: Make document read or unread
    2st: Updating drafts ( not implemented yet and not tested )
    3st: Moving between public folders
    """

    # def getElasticByInboxID(self, positionID, inboxID):
    # client = Elasticsearch()
    # indexName = "inbox_%s" % (positionID,)

    # s = Search(using=client, index=indexName, ) \
    # .query(Q(inboxID = inboxID)).execute()

    def removeFromElastic(self, positionID, id):
        es = getElasticSearch()
        indexName = settings.ELASTIC_INBOX_INDEXING_NAME + str(positionID)
        res = es.delete(index=indexName, doc_type="inbox", id=id)
        return res

    def update(self, instance, validated_data):
        # hanling automated read time
        readTimes = instance.readTimes
        readTimes.append(datetime.now())
        validated_data["readTimes"] = readTimes
        if "letter" in validated_data:
            if "letter" in validated_data:
                if "body" in validated_data["letter"]:
                    validated_data["letterSummery"] = strip_tags(validated_data["letter"]["body"])[:30]

        # -----------------------------------------------
        result = super(InboxSerializer, self).update(instance, validated_data)
        # es = getElasticSearch()
        indexName = settings.ELASTIC_INBOX_INDEXING_NAME + str(instance.currentPositionID, )

        dabirkhaneh_itemModes = [5, 6, 9, 10, 11, 12]
        if instance.itemMode in dabirkhaneh_itemModes:
            indexName = settings.ELASTIC_SEC_INDEXING_NAME + str(instance.letter['secretariatID'])

        if "letter" in validated_data:
            if "id" in validated_data["letter"]:
                validated_data["letter"]["id"] = str(instance["letter"]["id"])

            if "sign" in validated_data["letter"]:
                if "id" in validated_data["letter"]["sign"]:
                    validated_data["letter"]["sign"]["id"] = str(validated_data["letter"]["sign"]["id"])

                if "letter" in validated_data["letter"]["sign"]:
                    validated_data["letter"]["sign"].pop("letter")

                if "position" in validated_data["letter"]["sign"]:
                    validated_data["letter"]["sign"].pop("position")

        if "letter" in validated_data:
            if "exp" in validated_data["letter"]:
                if "recievers_raw" in validated_data["letter"]["exp"]:
                    if type(validated_data["letter"]["exp"]["recievers_raw"]) == dict:
                        validated_data["letter"]["exp"]["recievers_raw"] = json.dumps(
                            validated_data["letter"]["exp"]["recievers_raw"])
        vdata = self.removeAllExtra(validated_data)
        # updating elastic

        # if es.exists(index=indexName, id=str(instance.id), doc_type="inbox") :
        # res = es.update(
        #     index=indexName,
        #     doc_type="inbox",
        #     id=str(instance.id),
        #     body={"doc": vdata},
        # )
        updateToElastic(
            _index=indexName,
            _doc_type="inbox",
            _id=str(instance.id),
            _body={"doc": vdata}
        )

        # updating inbox static counters
        # self.UpdateCounterCatchMakeSeen(instance, result)

        # updating letter history
        historyInstance = InboxHistory.objects.get(currentInboxId=instance.id)

        data = {}
        data["recieverDetail"] = historyInstance.recieverDetail
        data["recieverDetail"]["seen"] = result.seen
        data["recieverDetail"]["date"] = datetime.now()
        historyInstanceSerial = LetterHistorySerializer(
            instance=historyInstance,
            partial=True,
            data=data
        )
        historyInstanceSerial.is_valid(raise_exception=True)
        historyInstanceSerial.update(historyInstance, historyInstanceSerial.validated_data)

        # updating Notofication
        if result.seen:
            pos = Position.objects.get(id=result.reciever["positionID"])
            Notifications.objects.filter(
                userID=pos.user_id,
                extra__inboxID=str(result.id)
            ).delete()

            NotificationViewSet().changesHappened(pos.user_id)
            # cache.set(str(pos.user_id)+"TopNotification", None)
            # cache.set(str(pos.user_id)+"hasNotification", True)
        return result

    # class Inbox(Document):
    # currentPositionID = IntField()
    # dateOfObservable = DateTimeField()
    # dateOfCreate = DateTimeField(default=datetime.now())
    #     sender = DictField()
    #     star = BooleanField(default=False)
    #     reciever = DictField()
    #     """
    #     these fields are in reciever
    #     security = IntField()
    #     #
    #         1=addi
    #         2=mahramaneh
    #         3=serri
    #     periority = IntField()  #
    #         1=addi
    #         2=forri
    #         3=kheili forri
    #
    #     """
    #     letter = DictField()
    #     letterSummery = StringField(default="Autosave", required=False, null=True)
    #     labels = ListField()
    #     folders = ListField()
    #     readTimes = ListField()
    #     seen = BooleanField(default=False)
    #     """
    #     itemType:
    #         1 = this inbox item received and sent by some one else as usual inside letter
    #         2 = this inbox item is sent to a user and an inbox item listed in send letters
    #         3 = this inbox item forwarded
    #         4 = this inbox item is replied one, i mean this letter is a replay letter
    #         5 = this inbox item is auto send inbox as rooneveshte khodkar
    #         6 = this is first and beginner of a letter
    #         7 = no Type // this is for storing draft
    #
    #     """
    #     itemType = IntField(default=1)
    #     replyedInbox = DictField()  # when a sent=4 this field store old inbox body
    #     previousInboxId = ObjectIdField(null=True, required=False)  # when a sent=3 this field store old inbox body
    #     """
    #     itemMode :
    #         1= dakheli
    #         2= rooneveshte sadereh
    #         3= rooneveshte varedeh
    #         4= draft
    #         5= draft sadere
    #         6= draft varedeh
    #         7= dakheli first send
    #     """
    #     itemMode = IntField(default=1)
    #     """
    #     itemPlace :
    #         1= item in inboxes public folders
    #         2= item in archive
    #         3= item in trash
    #         4= item in trash and hide !
    #     """
    #     itemPlace = IntField(default=1)

    """
    when some one send new letter new notification must appear to the reciever
    we set notify for the following :
    inboxInstance.itemType == 1,2,3,4 and
    inboxInstance.itemMode == 1,2,3 and
    inboxInstance.itemPlace == 1

    then we have diffrent types of priority
        inboxInstance.periority
        1=addi
        2=forri
        3=kheili forri



    """

    def InboxNotification(self, inboxInstance):
        if ((inboxInstance.itemType in [1, 2, 3, 4, 10]) and (
                inboxInstance.itemMode in [1, 2, 3, 10]) and (
                inboxInstance.itemPlace in [1])):
            pos = Position.objects.get(id=inboxInstance.reciever["positionID"])
            dt = {}
            dt["type"] = 1  # means come from automation
            dt["typeOfAlarm"] = 1  # means at morabaa
            dt["periority"] = inboxInstance.reciever["periority"] if "periority" in inboxInstance.reciever else 1
            dt["informType"] = 1  # means information
            dt["userID"] = inboxInstance.reciever['userID']
            extra = {}
            extra["name"] = inboxInstance.sender['profileName']
            extra["chart"] = inboxInstance.sender['chartName']
            extra["subject"] = inboxInstance.letter['subject']
            extra["letterID"] = inboxInstance.letter['id']
            extra["inboxID"] = str(inboxInstance.id)
            extra["positionID"] = inboxInstance.sender["positionID"]
            extra["currentCompany"] = pos.company.id
            extra["currentCompanyName"] = pos.company.name
            extra["ownerPositionID"] = pos.id
            dt["extra"] = extra
            vs = NotificationsSerializer(data=dt)
            vs.is_valid(raise_exception=True)
            vs.save()

            return vs
