from copy import copy
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from mongoengine import QuerySet
from rest_framework.decorators import list_route
from rest_framework_mongoengine import viewsets
from rest_framework.response import Response
from amspApp.CompaniesManagment import Positions
from amspApp.CompaniesManagment.Positions.models import Position, PositionsDocument
from rest_framework import status
from amspApp.CompaniesManagment.Positions.serializers.PositionSerializer import PositionDocumentSerializer
from amspApp.CompaniesManagment.members.serializers.MemberSerializer import MembersDocumentSerializer, \
    MembersDocumentSerializerForPerm
from amspApp.CompaniesManagment.models import Company
from amspApp.Letter.serializers.InboxFolderSerializer import InboxFolderSerializer
from amspApp.Letter.serializers.InboxSerializer import InboxSerializer
from amspApp._Share.ListPagination import ListPagination, DetailsPagination


class AccessToSecratariatViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    serializer_class = MembersDocumentSerializerForPerm
    pagination_class = DetailsPagination
    queryset = PositionsDocument.objects.all()

    """
    something remains :
    a person who has company manager roles can edit this panel
    """

    def update(self, request, *args, **kwargs):
        positionInstance = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        defaultCompanyInstance = self.request.user.current_company
        filter = {
            "id": request.data['desc']['automation']['SelectedCompanyID'],
            "owner_user": self.request.user.id
        }
        selectCompanyInstance = Company.objects.get(**filter)
        posDesc = PositionsDocument.objects.get(positionID=positionInstance.id)
        posDescSerial = PositionDocumentSerializer(instance=posDesc).data
        posDescSerialDesc = posDescSerial['desc']
        posDescSerialDesc["automation"] = {}
        posDescSerialDesc["automation"]["permission"] = request.data['desc']['automation']['permission']
        request.data['desc'].update(posDescSerialDesc)
        return super(AccessToSecratariatViewSet, self).update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        positionInstance = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        defaultCompanyInstance = self.request.user.current_company
        filter = {
            "id": request.query_params['comid'],
            "owner_user": self.request.user.id
        }
        selectCompanyInstance = Company.objects.get(**filter)

        selectedPersonDocumentInstance = PositionsDocument.objects.get(id=kwargs["id"])
        selectedPersonInstance = Position.objects.get(
            id=selectedPersonDocumentInstance.positionID,
            company=selectCompanyInstance)

        return Response(selectedPersonDocumentInstance.desc)

    def template_view(self, request, *args, **kwargs):
        return render_to_response(
            "settings/automations/AccessToSecratariats.html",
            {}, context_instance=RequestContext(request))

    def getSecPer(self, posID):
        positionDocumentInstance = PositionsDocument.objects.get(positionID=posID)
        '''
        sent to person tabs contains 4 tabs :
        1- all person
        2- groups
        3- chart
        4- zone
        5- send to all
        this def create and check permitted tabs according to security settings
        '''

        tabsDisallow = []
        # if nothing set into positionDocumentInstance.desc then it means has all access
        tabs = ['Members', 'Groups', 'Positions', 'Zones', 'All']

        if positionDocumentInstance.desc:
            if 'automation' in positionDocumentInstance.desc:
                if 'permission' in positionDocumentInstance.desc['automation']:
                    if 'not_Allowed_sent_to_Members' in positionDocumentInstance.desc['automation']['permission']:
                        if positionDocumentInstance.desc['automation']['permission']['not_Allowed_sent_to_Members']:
                            tabsDisallow.append("Members")
                    if 'not_Allowed_sent_to_Groups' in positionDocumentInstance.desc['automation']['permission']:
                        if positionDocumentInstance.desc['automation']['permission']['not_Allowed_sent_to_Groups']:
                            tabsDisallow.append("Groups")
                    if 'not_Allowed_sent_to_Positions' in positionDocumentInstance.desc['automation']['permission']:
                        if positionDocumentInstance.desc['automation']['permission']['not_Allowed_sent_to_Positions']:
                            tabsDisallow.append("Positions")
                    if 'not_Allowed_sent_to_Zones' in positionDocumentInstance.desc['automation']['permission']:
                        if positionDocumentInstance.desc['automation']['permission']['not_Allowed_sent_to_Zones']:
                            tabsDisallow.append("Zones")
                    if 'not_Allowed_sent_to_All' in positionDocumentInstance.desc['automation']['permission']:
                        if positionDocumentInstance.desc['automation']['permission']['not_Allowed_sent_to_All']:
                            tabsDisallow.append("All")
        finalTab = []
        for t in tabs:
            found = False
            for tA in tabsDisallow:
                if tA == t:
                    found = True
            if found == False:
                finalTab.append(t)
        return finalTab

    def send_Just_with_Chart_limitation(self, posID):
        justSendToChart = False
        positionDocumentInstance = PositionsDocument.objects.get(positionID=posID)
        if positionDocumentInstance.desc:
            if 'automation' in positionDocumentInstance.desc:
                if 'permission' in positionDocumentInstance.desc['automation']:
                    if 'send_Just_with_Chart_limitation' in positionDocumentInstance.desc['automation']['permission']:
                        if positionDocumentInstance.desc['automation']['permission']['send_Just_with_Chart_limitation']:
                            justSendToChart = True
        return justSendToChart

    def not_Allowed_sent_to_All(self, posID):
        not_Allowed_sent_to_All = False
        positionDocumentInstance = PositionsDocument.objects.get(positionID=posID)
        if positionDocumentInstance.desc:
            if 'automation' in positionDocumentInstance.desc:
                if 'permission' in positionDocumentInstance.desc['automation']:
                    if 'not_Allowed_sent_to_All' in positionDocumentInstance.desc['automation']['permission']:
                        if positionDocumentInstance.desc['automation']['permission']['not_Allowed_sent_to_All']:
                            not_Allowed_sent_to_All = True
        return not_Allowed_sent_to_All

    @list_route(methods=["get"])
    def getPermittedSendTab(self, request, *args, **kwargs):
        positionInstance = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)

        return Response(self.getSecPer(positionInstance.id))
