from bson import ObjectId
from amspApp.CompaniesManagment.Secretariat.models import SecretariatPermissions
from amspApp.CompaniesManagment.Secretariat.serializers.SecretariatsSerializers import SecretariatSerializer
from amspApp.CompaniesManagment.Secretariat.serializers.SignSerializer import SignSerializer
from amspApp.Letter.models import Letter, Inbox
from amspApp.Letter.serializers.InboxSerializer import InboxSerializer
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class LetterSerializer(DynamicFieldsDocumentSerializer):
    class Meta:
        model = Letter

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    def create(self, validated_data):
        """
        before storing it must check user permission in current secretariat
        """
        # pring("------------------------------------------------------------- letterSerializer.py line 26")

        SecretariatSerializer().CheckPermission(validated_data)
        letterInstance = super(LetterSerializer, self).create(validated_data)
        # pring("------------------------------------------------------------- letterSerializer.py line 30")
        # letterInstance = signLetter
        # checking letter type with current permissions
        # just inside, exported and imported letter are allowed to receive sign ID
        # letter types =
        # 1=Dakheli
        #       2=Sadereh
        #       3=Varedeh
        #       4=Document
        #       5=Message
        #       6=report
        #       7=draft dekheli
        #       8=draft sadere
        #       9=draft dakheli
        # secretariat default value is : 100 means : # index[0]= dakheli 1= sadereh 2= varede
        # sign are fill just when user try not to send letter as draft or draft
        sign = SignSerializer().signLetter(letterInstance)._data if (
                letterInstance.letterType != 7 and
                letterInstance.letterType != 8 and
                letterInstance.letterType != 9 and
                letterInstance.letterType != 10 and
                letterInstance.letterType != 11) else {}
        # updating sign number directly
        letterInstance.sign = sign
        letterInstance.save()
        # pring("------------------------------------------------------------- letterSerializer.py line 55")

        # adding to sent folder of sender

        """
        letterInstance.letterType :
            1=Dakheli
            2=Sadereh
            3=Varedeh
            4=Document
            5=Message
            6=report
            7=draft dekheli
            8=draft sadere
            9=draft dakheli
            10=template sadereh
        """
        if letterInstance.letterType == 1:
            firstInbox = InboxSerializer().SaveToSentFolder(letterInstance)
            InboxSerializer().SendLetter(letterInstance=letterInstance, prevSenderInboxID=firstInbox.id)
            return letterInstance

        if letterInstance.letterType == 7:
            InboxSerializer().SaveToDraftFolder(letterInstance=letterInstance)
            return letterInstance

        if letterInstance.letterType == 4:
            firstInbox = InboxSerializer().SaveToSentFolder(letterInstance)
            InboxSerializer().SendLetter(letterInstance=letterInstance, prevSenderInboxID=firstInbox.id)
            return letterInstance

        # export letter
        if letterInstance.letterType == 2:
            firstInbox = InboxSerializer().SaveToSentFolderAsExport(letterInstance)
            if "export" in letterInstance.exp:
                if "hameshRecievers" in letterInstance.exp["export"]:
                    letterInstance.recievers = letterInstance.exp["export"]["hameshRecievers"]

                    # here we have to send the exported letter sent folder first
                    firstInbox = InboxSerializer().SaveToSentFolder(letterInstance)
                    InboxSerializer().SendLetter(
                        letterInstance=letterInstance,
                        prevSenderInboxID=firstInbox.id,
                        itemMode=1,
                        itemType=8)

            letterInstance.exp["baseInbox"] = firstInbox.id
            return letterInstance

        # import letter
        if letterInstance.letterType == 3:
            firstInbox = InboxSerializer().SaveToRecFolderAsImport(letterInstance)
            if "export" in letterInstance.exp:
                if "hameshRecievers" in letterInstance.exp["export"]:
                    letterInstance.recievers = letterInstance.exp["export"]["hameshRecievers"]
                    firstInbox = InboxSerializer().SaveToSentFolder(letterInstance)
                    InboxSerializer().SendLetter(letterInstance=letterInstance, prevSenderInboxID=firstInbox.id,
                                                 itemMode=1, itemType=10)
            letterInstance.exp["baseInbox"] = firstInbox.id
            return letterInstance

        # # export letter template
        # if letterInstance.letterType == 10:
        #     firstInbox = InboxSerializer().SaveToTemplateAsExport(letterInstance)
        #     letterInstance.exp["baseInbox"] = firstInbox.id
        #     return letterInstance

        # export letter draft
        if letterInstance.letterType == 8:
            firstInbox = InboxSerializer().SaveToDraftAsExport(letterInstance)
            letterInstance.exp["baseInbox"] = firstInbox.id
            return letterInstance

        # InboxSerializer().SendLetter(letterInstance=letterInstance, prevSenderInboxID=None)
        # return letterInstance

    """
    This field is just for updating draft
    here i must do these things
    1- updating letter instance first
    2- updating index instance second
    3- updating elastic search third
    i want to let share letter for multiple work in a document
    """

    def update(self, instance, validated_data):
        result = super(LetterSerializer, self).update(instance, validated_data)
        addTo = result._data

        # getting all inbox instances which contains the letter ,
        inboxes = Inbox.objects.filter(letter__id=result["id"])
        for inboxInstance in inboxes:
            inboxSerial = InboxSerializer(
                instance=inboxInstance,
                data={"letter": addTo},
                partial=True)
            inboxSerial.is_valid(True)
            inboxSerial.update(
                instance=inboxInstance,
                validated_data=inboxSerial.validated_data)
        return result
