from datetime import datetime
from amspApp.Infrustructures.Classes.DateConvertors import convertJerkStrDateTime, sh_to_mil
from amspApp.Letter.models import InboxHistory
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer

__author__ = 'mohammad'


class LetterHistorySerializer(DynamicFieldsDocumentSerializer):
    class Meta:
        model = InboxHistory

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)



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
        3 = this inbox item forwarded
        4 = this inbox item is replied one, i mean this letter is a replay letter
        5 = this inbox item is auto send inbox as rooneveshte khodkar
        6 = this is first and beginner of a letter
        7 = no Type // this is for storing draft

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

    def createFromInbox(self, inboxInstance, defaultValue=None):

        def getFromOtherInfo(optionName, reciever):
            posID = reciever["positionID"]
            for i in reciever["others"]:
                if i["positionID"] == posID:
                    if "option" not in i:
                        return None
                    if not optionName in i["option"]:
                        return None
                    return i["option"][optionName]
            return defaultValue

        dd = getFromOtherInfo("CurrentTime", inboxInstance.reciever)
        priority = getFromOtherInfo("priority", inboxInstance.reciever)
        security = getFromOtherInfo("security", inboxInstance.reciever)
        if dd:
            dd = sh_to_mil(convertJerkStrDateTime(dd), True)
            dd = datetime.strptime(dd, "%Y/%m/%d %H:%M")
        data = {
            "letterID": inboxInstance['letter']['id'],
            "senderDetail": {
                "avatar": inboxInstance.sender["avatar"],
                "name": inboxInstance.sender["profileName"],
                "chart": inboxInstance.sender["chartName"],
                "positionID": inboxInstance.sender["positionID"],
                "userID": inboxInstance.sender["userID"],
                "date": inboxInstance.dateOfCreate,
                "inboxID": str(inboxInstance.previousInboxId)
            },
            "recieverDetail": {
                "avatar": inboxInstance.reciever["avatar"],
                "name": inboxInstance.reciever["profileName"],
                "chart": inboxInstance.reciever["chartName"],
                "positionID": inboxInstance.reciever["positionID"],
                "inboxID": str(inboxInstance.id),
                "userID": "",
                "footnote": inboxInstance.reciever["userID"],
                "dateOfCreate": datetime.now(),
                "seen": False,
                "seenDate": None,
                "defaultSec": inboxInstance.reciever["defaultSec"] if "defaultSec" in inboxInstance.reciever else "",
                "priority": int(priority) if priority else None,
                "security": int(security) if security else None,
                "cc": getFromOtherInfo("cc", inboxInstance.reciever),
                "hamesh": getFromOtherInfo("hamesh", inboxInstance.reciever),
                "dateOfObservable": dd if dd else inboxInstance.dateOfObservable,

                # "priority":inboxInstance.reciever["priority"] if "priority" in inboxInstance.reciever else "",
                # "security":inboxInstance.reciever["security"] if "security" in inboxInstance.reciever else "",
                # "cc":inboxInstance.reciever["cc"] if "cc" in inboxInstance.reciever else "",
                # "hamesh":inboxInstance.reciever["hamesh"] if "hamesh" in inboxInstance.reciever else "",
                # "hamesh":inboxInstance["reciever"]['others'][0]['option']['hamesh'],
            },
            "itemType": self.handleItemType(inboxInstance),
            "itemMode": self.handleItemMode(inboxInstance),
            "itemActivityMode": self.handleItemActivityMode(inboxInstance),
            "docType": self.handleDocType(inboxInstance)
        }
        if inboxInstance.previousInboxId != None: data["previousInboxId"] = inboxInstance.previousInboxId
        data["currentInboxId"] = inboxInstance.id
        res = self.create(data)
        return res

    def handleItemType(self, inboxInstance):
        if inboxInstance.itemType == 6: return 2
        # if inboxInstance.itemType == 10: return 2
        # if inboxInstance.itemType == 8: return 2
        return 1

    def handleItemMode(self, inboxInstance):
        if inboxInstance.itemType == 5: return 2
        return 1

    def handleItemActivityMode(self, inboxInstance):
        if inboxInstance.itemType == 4: return 2
        if inboxInstance.itemType == 3: return 3
        return 1

    def handleDocType(self, inboxInstance):
        if inboxInstance.itemPlace == 3: return 3
        if inboxInstance.itemMode == 4: return 2
        if inboxInstance.itemMode == 5: return 2
        if inboxInstance.itemMode == 6: return 2
        return 1
