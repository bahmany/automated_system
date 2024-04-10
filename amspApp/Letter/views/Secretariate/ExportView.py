from datetime import datetime

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.CompaniesManagment.Positions.models import Position, PositionsDocument
from amspApp.CompaniesManagment.Secretariat.serializers.SecretariatsSerializers import SecretariatSerializer, \
    SecretariatSerializerPermission
from amspApp.CompaniesManagment.Secretariat.viewes.SecretariatsViews import SecretariatsViewSet
from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh
from amspApp.Letter.models import Inbox, Letter, ExportScannedAfterSend, Recieved
from amspApp.Letter.search.InboxSearch import InboxSearchViewClass
from amspApp.Letter.serializers.InboxSerializer import InboxSerializer
from amspApp.Letter.serializers.LetterSerializer import LetterSerializer
from amspApp.Letter.serializers.SecTagsSerializer import SecTagItemSerializer
from amspApp.Letter.views.InboxListView import InboxListViewSet
from amspApp._Share.ListPagination import DetailsPagination


class SecExportViewSet(viewsets.ModelViewSet):
    pagination_class = DetailsPagination
    lookup_field = "id"
    serializer_class = LetterSerializer
    queryset = Letter.objects.all()

    def template_view(self, request, *args, **kwargs):
        return render_to_response("letter/Secretariat/Letters/Export/NewExport.html",
                                  {}, context_instance=RequestContext(request))

    def template_view_sidebar(self, request, *args, **kwargs):
        return render_to_response("letter/Secretariat/sidebar/base.html",
                                  {}, context_instance=RequestContext(request))

    def template_view_export_list(self, request, *args, **kwargs):
        return render_to_response("letter/Secretariat/Letters/Export/ExportLettersList.html",
                                  {}, context_instance=RequestContext(request))

    def template_view_export_prev(self, request, *args, **kwargs):
        return render_to_response("letter/Secretariat/Letters/Export/Preview.html",
                                  {}, context_instance=RequestContext(request))

    def template_view_export_recieved(self, request, *args, **kwargs):
        return render_to_response("letter/Secretariat/Letters/Export/Recieved.html",
                                  {}, context_instance=RequestContext(request))

    def template_view_export_scan(self, request, *args, **kwargs):
        return render_to_response("letter/Secretariat/Letters/Export/Scan.html",
                                  {}, context_instance=RequestContext(request))

    def template_view_export_templates(self, request, *args, **kwargs):
        return render_to_response("letter/Secretariat/Letters/Export/Template.html",
                                  {}, context_instance=RequestContext(request))

    def template_view_import_templates(self, request, *args, **kwargs):
        return render_to_response("letter/Secretariat/Letters/Import/NewImport.html",
                                  {}, context_instance=RequestContext(request))

    def template_view_export_export_import_list(self, request, *args, **kwargs):
        return render_to_response("letter/Secretariat/Letters/Import/ImportLetterList.html",
                                  {}, context_instance=RequestContext(request))

    def template_view_export_import_preview(self, request, *args, **kwargs):
        return render_to_response("letter/Secretariat/Letters/Import/PreviewImport.html",
                                  {}, context_instance=RequestContext(request))

    def create(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        posDoc = PositionsDocument.objects.get(positionID=pos.id,
                                               companyID=self.request.user.current_company.id)
        request.data["creatorPositionID"] = pos.id
        request.data["creatorPosition"] = posDoc._data
        request.data["creatorPosition"]["id"] = str(request.data["creatorPosition"]["id"])
        secInstance = SecretariatsViewSet().GetDefaultSecretariatInstanceByPositionInstance(pos)
        request.data["secretariatID"] = secInstance.secretariat.id
        request.data["secretariat"] = SecretariatSerializer(instance=secInstance.secretariat).data
        request.data["secretariatPermissionID"] = secInstance.id
        request.data["secretariatPermission"] = SecretariatSerializerPermission(instance=secInstance).data
        request.data["dateOfPost"] = timezone.now()

        if request.data["letterType"] == 8 or request.data["letterType"] == 10:
            if "body" in request.data:
                if request.data["body"] is None:
                    request.data["body"] = " "
            else:
                request.data["body"] = " "
        result = super(SecExportViewSet, self).create(request, *args, **kwargs)
        return result

    def list(self, request, *args, **kwargs):
        result = InboxSearchViewClass().get(request, format=None, itemModes="Dabirkhaneh")
        for rd in result.data["results"]:
            rd["scan_count"] = ExportScannedAfterSend.objects.filter(inboxID=rd["id"]).count()
            rd["rec_count"] = Recieved.objects.filter(inboxID=rd["id"]).count()
            if 'letter' in rd:
                if 'exp' in rd['letter']:
                    if 'dateOfSent' in rd['letter']['exp']:
                        if rd['letter']['exp']['dateOfSent'] != "":
                            if int(rd['letter']['exp']['dateOfSent'].split("/")[0]) > 2000:
                                rd['letter']['exp']['dateOfSent'] = mil_to_sh(rd['letter']['exp']['dateOfSent'],
                                                                              splitter="/")

        return result

    @detail_route(methods=["get"])
    def get_prev(self, request, *args, **kwargs):
        inboxInstance = Inbox.objects.get(
            id=request.query_params["id"])
        result = InboxSerializer(instance=inboxInstance)
        result = result.data
        if 'sign' in result['letter']:
            if 'generatedFileAddr' in result['letter']['sign']:
                result['letter']['sign']['generatedFileAddr'] = \
                    result['letter']['sign']['generatedFileAddr'].split("/")[
                        len(result['letter']['sign']['generatedFileAddr'].split("/")) - 1]
                result['letter']['sign']['generatedFileAddr'] = "/api/v1/file/upload?q=" + result['letter']['sign'][
                    'generatedFileAddr']
        result['letter']['body'] = result['letter']['body'].replace("&nbsp;", " ")
        result['letterSummery'] = result['letterSummery'].replace("&nbsp;", " ")
        return Response(result)

    def update(self, request, *args, **kwargs):
        self.get_queryset()
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        posDoc = PositionsDocument.objects.get(positionID=pos.id,
                                               companyID=self.request.user.current_company.id)

        request.data["creatorPositionID"] = pos.id
        request.data["creatorPosition"] = posDoc._data
        request.data["creatorPosition"]["id"] = str(request.data["creatorPosition"]["id"])
        secInstance = SecretariatsViewSet().GetDefaultSecretariatInstanceByPositionInstance(pos)
        request.data["secretariatID"] = secInstance.secretariat.id
        request.data["secretariat"] = SecretariatSerializer(instance=secInstance.secretariat).data
        request.data["secretariatPermissionID"] = secInstance.id
        request.data["secretariatPermission"] = SecretariatSerializerPermission(instance=secInstance).data
        request.data["dateOfPost"] = datetime.now()

        if 'letterType' in request.data:
            if request.data["letterType"] == 8 or request.data["letterType"] == 10:
                if "body" in request.data:
                    if request.data["body"] is None:
                        request.data["body"] = " "
                    if request.data["body"] == "":
                        request.data["body"] = " "
                else:
                    request.data["body"] = " "

        result = super(SecExportViewSet, self).update(request, *args, **kwargs)

        for tag in request.data["tags"]:
            dt = {
                "tag": tag["id"],
                "letterID": result.data["id"],
                "positionID": pos.id
            }
            tagSerial = SecTagItemSerializer(data=dt)
            tagSerial.is_valid(raise_exception=True)
            tagSerial.save()

        return result

    @detail_route(methods=["post"])
    def changeSuspend(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        letterID = Inbox.objects.get(id=kwargs["id"]).letter["id"]
        letterInstance = self.queryset.get(id=letterID)
        exp = letterInstance["exp"]
        if not "export" in exp:
            exp["export"] = {}
        exp["export"]["suspended"] = request.data["is_export_suspended"]
        letter = LetterSerializer(data={"exp": exp}, instance=letterInstance, partial=True)
        letter.is_valid(raise_exception=True)
        letter.save()
        return Response({})

    def destroy(self, request, *args, **kwargs):
        InboxListViewSet().deleteForEver(request, *args, **kwargs)
        return Response({})
