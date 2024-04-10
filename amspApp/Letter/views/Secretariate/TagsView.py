from django.http import HttpResponseForbidden
from mongoengine import Q
from rest_framework.decorators import list_route, detail_route
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.Secretariat.viewes.SecretariatsViews import SecretariatsViewSet
from amspApp.Letter.models import SecTag, SecTagItems
from amspApp.Letter.search.InboxSearch import InboxSearchViewClass
from amspApp.Letter.serializers.SecTagsSerializer import SecTagSerializer
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class SecTagsViewSet(viewsets.ModelViewSet):
    lookup_field = "id"

    serializer_class = SecTagSerializer

    queryset = SecTag.objects.all()

    def get_object(self):
        result = super(SecTagsViewSet, self).get_object()
        currentPosID = GetPositionViewset().GetCurrentPositionDocumentInstance(self.request).positionID
        if not result.PositionID:
            return result
        if result.PositionID != currentPosID:
            raise PermissionDenied()
        return result

    def get_queryset(self):

        self.queryset = SecTag.objects.filter(companyID=self.request.user.current_company_id)
        if 'q' in self.request.query_params.keys():
            if self.request.query_params["q"] != "":
                if self.request.query_params["q"] != "undefined":
                    self.queryset = self.queryset.filter(name__contains=self.request.query_params["q"]).limit(20)
        defaultSecratriat = SecretariatsViewSet().GetDefaultSecretariatInstance(self.request)
        if not InboxSearchViewClass().hasEnoughPermissionOnSecretariats(defaultSecratriat):
            raise Exception("عدم دسترسی به دبیرخانه")

        exportImport = 2  # default is Imported ...
        if "t" in self.request.query_params:
            if self.request.query_params["t"] != "":
                if self.request.query_params["t"] != "undefined":
                    exportImport = int(self.request.query_params["t"])
        if exportImport == 2:
            self.queryset = self.queryset.filter(
                Q(letterType=exportImport) | Q(letterType__ne=False))
        if exportImport == 1:
            self.queryset = self.queryset.filter(
                Q(letterType=exportImport))

        return self.queryset

    def list(self, request, *args, **kwargs):

        result = super(SecTagsViewSet, self).list(request, *args, **kwargs)
        for r in result.data:
            r["count"] = SecTagItems.objects.filter(tag=r["id"]).count()
            if not r["PositionID"]:
                permitedPosDoc = GetPositionViewset().GetCurrentPositionDocumentInstance(self.request)
            else:
                permitedPosDoc = PositionsDocument.objects.get(positionID=r["PositionID"])

            r["creator"] = GetPositionViewset().GetPositionUerProfileName(permitedPosDoc)
        return result

    @detail_route(methods=["get"])
    def removeFromLetter(self, request, *args, **kwargs):
        currentPosDoc = GetPositionViewset().GetCurrentPositionDocumentInstance(request).positionID
        selectedTag = SecTagItems.objects.get(id=kwargs['id'])
        if selectedTag.positionID == currentPosDoc:
            selectedTag.delete()
        else:
            return HttpResponseForbidden()
        return Response({})

    def create(self, request, *args, **kwargs):
        request.data["companyID"] = request.user.current_company_id
        currentPosDoc = GetPositionViewset().GetCurrentPositionDocumentInstance(request).positionID
        defaultSecratriat = SecretariatsViewSet().GetDefaultSecretariatInstance(request)
        request.data["PositionID"] = currentPosDoc
        request.data["secretariatID"] = defaultSecratriat.id
        request.data["letterType"] = int(request.data["type"])
        if InboxSearchViewClass().hasEnoughPermissionOnSecretariats(defaultSecratriat):
            return super(SecTagsViewSet, self).create(request, *args, **kwargs)
        return HttpResponseForbidden()

    def update(self, request, *args, **kwargs):
        request.data["companyID"] = request.user.current_company_id
        currentPosDoc = GetPositionViewset().GetCurrentPositionDocumentInstance(request).positionID
        defaultSecratriat = SecretariatsViewSet().GetDefaultSecretariatInstance(request)
        request.data["PositionID"] = currentPosDoc
        request.data["secretariatID"] = defaultSecratriat.id
        request.data["letterType"] = int(request.data["type"])
        return super(SecTagsViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(SecTagsViewSet, self).destroy(request, *args, **kwargs)
