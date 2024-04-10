from datetime import datetime
import os
from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets
from amsp import settings
from amsp.settings import FILE_PATH_URL
from amspApp.CompaniesManagment.Positions.models import Position, PositionsDocument
from amspApp.CompaniesManagment.Secretariat.serializers.SecretariatsSerializers import SecretariatSerializer, \
    SecretariatSerializerPermission
from amspApp.CompaniesManagment.Secretariat.viewes.SecretariatsViews import SecretariatsViewSet
from amspApp.FileServer.serializers.FileSerializer import FileSerializer
from amspApp.Infrustructures.Classes.PublicFilters import QuerySetFilter
from amspApp.Letter.models import CompanyRecieverGroup, CompanyReciever, Inbox, Letter, Recieved, ExportTemplates
from amspApp.Letter.search.InboxSearch import InboxSearchViewClass
from amspApp.Letter.serializers.LetterSecretariatSerializer import RecievedSerializer, ExportTemplatesSerializer
from amspApp.Letter.serializers.LetterSerializer import LetterSerializer
from amspApp.Letter.views.InboxListView import InboxListViewSet
from amspApp.Letter.views.Secretariate.CompanyRecieverView import CompanyRecieverViewSet
from amspApp._Share.CharacterHandle import ShowUtfCharacterCode
from amspApp._Share.DocxGenerator import LetterTextToDownload
from amspApp._Share.ListPagination import DetailsPagination


class ExportTemplatesViewSet(viewsets.ModelViewSet):
    pagination_class = DetailsPagination
    lookup_field = "id"
    serializer_class = ExportTemplatesSerializer
    queryset = ExportTemplates.objects.all().order_by("-id")


    def get_queryset(self):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        id = SecretariatsViewSet().GetDefaultSecretariatInstanceByPositionInstance(pos).id
        self.queryset = self.queryset.filter(secID=id).order_by("-id")
        return self.queryset


    @detail_route(methods=["get"])
    def Download(self, request, *args, **kwargs):
        if kwargs["id"] == "a4":
            return Response({"addr": '/static/templates/****A4.docx'})
        if kwargs["id"] == "a5":
            return Response({"addr": '/static/templates/****A5.docx'})
        return Response({"addr": '/api/v1/file/upload?q=' + kwargs["id"]})


    @detail_route(methods=["get"])
    def Preview(self, request, *args, **kwargs):
        body = request.query_params
        letterInstance = Inbox.objects.get(id=kwargs["id"])
        letterInstance = Letter.objects.get(id=letterInstance.letter['id'])
        # templateInstance = self.queryset.get(id=body["id"])

        """

        253151 : Header
        55895  : Somareh img address
        111599  : Sign img address
        98547  : Tarikh
        58942  : Peivast
        889845 : LetterTo
        5955554: Body
        558548 : Sign Text
        778587 : Footer Text >> roonevesht recievers puts here

        """

        # converting company recs to string with breakers
        companyRecs = ""
        if "export" in letterInstance.exp:
            if "companyRecievers" in letterInstance.exp["export"]:
                for co in letterInstance.exp["export"]["companyRecievers"]:
                    recname = co["recieverName"] if "recieverName" in co else ""
                    companyRecs = companyRecs + co["name"] + " " + recname

        replaceTexts = {
            # 'typeOf': body["Template"],
            '253153': letterInstance.exp["headerText"] if "headerText" in letterInstance.exp else "",
            '55895': letterInstance.sign["generatedFileAddr"] if "generatedFileAddr" in letterInstance.sign else "",
            '98547': letterInstance.exp["dateOfSent"] if "dateOfSent" in letterInstance.exp else "",
            '58942': letterInstance.exp["attsCount"] if "attsCount" in letterInstance.exp else "",
            '889845': companyRecs,
            '5955554': letterInstance.body,
            '558548': letterInstance.exp["signText"] if "signText" in letterInstance.exp else "",
            '778587': letterInstance.exp["footerText"] if "footerText" in letterInstance.exp else ""}
        replaceTexts["dateToDownload"] = letterInstance.dateOfPost
        replaceTexts["5955554"] = replaceTexts["5955554"].replace("&nbsp;", " ")
        if body["id"] == "a4":
            addr = settings.APP_PATH + 'static/templates/****A4.docx'
        else:
            if body["id"] == "a5":
                addr = settings.APP_PATH + 'static/templates/****A5.docx'
            else:
                addr = settings.FILE_PATH + self.queryset.get(id=body["id"]).fileAddr

        replaceTexts["111599"] = letterInstance.sign["generatedSign"] if "generatedSign" in letterInstance.sign else ""

        resDocx = LetterTextToDownload(replaceTexts, addr)

        def getSize(fileobject):
            fileobject.seek(0, 2)  # move the cursor to the end of the file
            size = fileobject.tell()
            return size

        # saving to file store
        env = request._request.environ
        newFile = {
            "userID": request.user.id,
            "dateOfPost": letterInstance.dateOfPost,
            "originalFileName": ShowUtfCharacterCode(letterInstance.subject + '.docx'),
            "decodedFileName": resDocx["filename"] ,
            "uploaderIP": {


                "fileSize": os.path.getsize(resDocx["fullPath"]),
                "home": env["HOME"] if "HOME" in env else None,
                "browser": env["HTTP_USER_AGENT"] if "HTTP_USER_AGENT" in env else None,
                "ip": env["REMOTE_ADDR"] if "REMOTE_ADDR" in env else None
            }
        }

        file = FileSerializer(data=newFile)
        file.is_valid(raise_exception=True)
        file.save()

        return Response({"addr": FILE_PATH_URL+resDocx["filename"]})


    def create(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=request.user,
            company=request.user.current_company)
        request.data["positionID"] = pos.id
        request.data["secID"] = SecretariatsViewSet().GetDefaultSecretariatInstanceByPositionInstance(pos).id

        return super(ExportTemplatesViewSet, self).create(request, *args, **kwargs)

