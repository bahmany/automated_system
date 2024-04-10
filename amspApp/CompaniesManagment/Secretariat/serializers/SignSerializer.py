from datetime import datetime
import uuid
import PIL
from PIL.Image import Image
from PIL.ImageDraw import ImageDraw
from PIL.ImageFont import ImageFont
from amsp.settings import ABSOLUTE_PATH, BASE_DIR
from amspApp.CompaniesManagment.Secretariat.models import Sign, SecretariatPermissions
from amspApp.CompaniesManagment.Secretariat.serializers.SecretariatsSerializers import SecretariatSerializer
from amspApp.FileServer.views.FileUploadView import FileUploadViewSet
from amspApp.Infrustructures.Classes import date_utils
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class SignSerializer(DynamicFieldsDocumentSerializer):
    class Meta:
        model = Sign

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


    def signLetter(self, letterInstance):
        """ 1= dakheli
            2= sadereh
            3= varedeh
            """
        # checking for sign permission
        # getting chart id

        # At first we have to get Dabirkhaneh ID
        # Then Check Its permission
        # Then Sign :)))))


        # getting secretariat permissions
        permissionInstance = SecretariatPermissions.objects.get(
            secretariat=letterInstance.secretariat["id"],
            chart=letterInstance.creatorPosition["chartID"]
        )

        if permissionInstance.permission[0] != "1":
            raise Exception("Access Denied in this Dabirkhaneh")



        # if letterInstance.letterType == 1:
        newSecCounter = {
            "dakheli_last_id": permissionInstance.secretariat.dakheli_last_id + 1 if letterInstance.letterType == 1 or letterInstance.letterType == 4 else permissionInstance.secretariat.dakheli_last_id,
            "sadere_last_id": permissionInstance.secretariat.sadere_last_id + 1 if letterInstance.letterType == 2 else permissionInstance.secretariat.sadere_last_id,
            "varede_last_id": permissionInstance.secretariat.varede_last_id + 1 if letterInstance.letterType == 3 else permissionInstance.secretariat.varede_last_id
        }
        SecUpdated = SecretariatSerializer(data=newSecCounter, instance=permissionInstance.secretariat,
                                           partial=True)
        SecUpdated.is_valid(raise_exception=True)
        SecUpdated.update(
            validated_data=SecUpdated.validated_data,
            instance=permissionInstance.secretariat)

        secFormat = ""
        secLastID = ""
        if letterInstance.letterType == 1 or letterInstance.letterType == 4:
            secFormat = SecUpdated.data["dakheli_letters_format"],
            secLastID = SecUpdated.data["dakheli_last_id"],
        if letterInstance.letterType == 2:
            secFormat = SecUpdated.data["sadereh_letters_format"],
            secLastID = SecUpdated.data["sadere_last_id"],
        if letterInstance.letterType == 3:
            secFormat = SecUpdated.data["varede_letters_format"],
            secLastID = SecUpdated.data["varede_last_id"],

        sin = self.GenerateNewSign(
            secFormat[0],
            secLastID[0],
            letterInstance.creatorPosition["userID"]
        )
        # letter = ReferenceField(Letter)
        # position = ReferenceField(PositionsDocument)
        # postDate = DateTimeField(default=datetime.now())
        # generatedFileAddr = TextField()
        # generatedSign = TextField()

        newSign = {
            'letter': letterInstance.id,
            'position': letterInstance.creatorPosition["id"],
            'postDate': datetime.now(),
            'generatedFileAddr': sin['fileAddr'],
            'generatedSign': sin['outPut']
        }

        newSign = SignSerializer(data=newSign)
        newSign.is_valid(raise_exception=True)
        newSign = newSign.create(newSign.validated_data)

        return newSign


    def GenerateNewSign(
            self,
            formatCodeOfDabirkhaneh,
            lastId,
            creatorProfileObjID
    ):
        formatCodeOfDabirkhanehArray = formatCodeOfDabirkhaneh.split(".")
        """
        y = last int of year + without "0"
        yy = two int of year + "0"
        m = int of month
        mm = int of month with  +"0"
        x = x in maximum length of code which must return to first id
        if user put X in CaseCascade it generate enumerate numbers
        """

        def ProcessSepratedParams(param, _lastId):
            currentDateMilady = datetime.now().strftime("%Y-%m-%d")
            currentDateMiladyArray = currentDateMilady.split("-")
            currentDateShamsi = date_utils.calendar_util.jd_to_persian(
                date_utils.calendar_util.gregorian_to_jd(int(currentDateMiladyArray[0]),
                                                         int(currentDateMiladyArray[1]),
                                                         int(currentDateMiladyArray[2])))
            currentDateShamsi = tuple(map(str, currentDateShamsi))
            finalStr = ""
            if param == "y": return currentDateShamsi[0][2] + currentDateShamsi[0][3]
            if param == "yy":
                finalStr = currentDateShamsi[0][2] + currentDateShamsi[0][3]
                if len(finalStr) == 1: finalStr = "0" + finalStr
                return finalStr
            if param == "m": return currentDateShamsi[1]
            if param == "mm":
                finalStr = currentDateShamsi[1]
                if len(finalStr) == 1: finalStr = "0" + finalStr
                return finalStr
            if param == "d": return currentDateShamsi[2]
            if param == "dd":
                finalStr = currentDateShamsi[2]
                if len(finalStr) == 1: finalStr = "0" + finalStr
                return finalStr
            if param == "x": return (_lastId + 1).__str__()
            return param

        outPut = ""
        arrs = []
        for fCDA in formatCodeOfDabirkhanehArray:
            outPut += ProcessSepratedParams(fCDA, lastId)
            arrs.append(ProcessSepratedParams(fCDA, lastId))

        # from PIL.Image import
        # import PIL.Image as I, PIL.ImageFont as IF, PIL.ImageDraw as ID

        def change_to_persian(outPut):
            replace = [("1", u"۱"), ("2", u"۲"), ("3", u"۳"), ("4", u"۴"), ("5", u"۵"), ("6", u"۶"), ("7", u"۷"),
                       ("8", u"۸"),
                       ("9", u"۹"), ("0", u"۰")]
            outChar = ""
            cc = ""
            for o in outPut:
                outChar = o
                for rr in replace:
                    if o == rr[0]:
                        o = rr[1]
                        outChar = rr[1]
                cc = cc + outChar
            return cc

        output_pics = []
        totalWidth = 0
        v = 0
        fontsize = 35
        # f = IF.truetype(ABSOLUTE_PATH.func_globals["BASE_DIR"] + "/dms/static/css/fonts/Yekan.ttf", fontsize, )
        f = PIL.ImageFont.truetype(BASE_DIR + "/amspApp/static/fonts/bnazanin.ttf", fontsize, )

        for a in arrs:
            v = v + 1
            t = a
            i = PIL.Image.new("L", (1000, 1000), color=255)
            d = PIL.ImageDraw.Draw(i)

            d.text((0, 0), t, fill=0, font=f)
            text_width, text_height = d.textsize(t, font=f)
            # calcing offset
            i.size = (text_width, text_height + ( fontsize - text_height ))
            totalWidth = totalWidth + i.size[0]
            output_pics.append(i)
            # i.save("/tmp/du_" + str(v) + ".png", optimize=1)
        i = PIL.Image.new("L", (totalWidth + 10, i.size[1]), color=255)
        d = PIL.ImageDraw.Draw(i)
        x = -1
        xx = 0
        from bidi.algorithm import get_display

        for a in arrs:
            x = x + 1
            t = get_display(change_to_persian(a), upper_is_rtl=True)
            # t = a
            sizeOf = (xx, 0)
            d.text(sizeOf, t, fill=0, font=f)
            xx = xx + output_pics[x].size[0]

        fileAddr = FileUploadViewSet().saveSignFile(creatorProfileObjID)

        i.save(fileAddr["fullPath"], format="PNG")

        return {"outPut": outPut, "fileAddr": fileAddr["name"]}
