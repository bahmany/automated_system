from datetime import datetime

from rest_framework import status
from rest_framework.decorators import api_view, list_route, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets
from amspApp.CompaniesManagment.Charts.models import Chart
from amspApp.CompaniesManagment.Positions.models import Position, PositionsDocument
from amspApp.CompaniesManagment.Positions.serializers import PositionSerializer
from amspApp.CompaniesManagment.Positions.serializers.PositionSerializer import PositionDocumentSerializer
from amspApp.CompaniesManagment.members.serializers.MemberSerializer import MembersSerializer
from amspApp.CompaniesManagment.models import Company, CompanyMembersJointRequest
from amspApp.CompaniesManagment.permissions.CompanyPermissions import CanCruid
from amspApp.CompaniesManagment.permissions.PermissionChecker import get_permissions
from amspApp.Infrustructures.Classes.PublicFilters import QuerySetFilter
from amspApp.Letter.models import CompanyReciever
from amspApp.MyProfile.models import Profile
from amspApp.MyProfile.serializers.ProfileSerializer import ProfileSerializer
from amspApp._Share.ListPagination import ListPagination, DetailsPagination
from amspApp.amspUser.models import MyUser
from django.utils.translation import ugettext as _

"""
Rules :
       1- when a position is posted no body can not change them
       2- before updating a position the remaining should be freed by company owner
       3- in the searchs members should not be appeared
       4-




"""


class PositionViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    pagination_class = ListPagination
    permission_name = "Can_remove_members"
    permission_classes = (CanCruid,)

    def get_permissions(self):
        return get_permissions(self, PositionViewSet)


    def destroy(self, request, *args, **kwargs):

        PositionsDocument.objects.filter(positionID = kwargs['id']).delete()
        result = super(PositionViewSet, self).destroy(request, *args, **kwargs)

        return result

    @detail_route(methods=["post"])
    def ChangeChartID(self, request, *args, **kwargs):

        currentPositionInstance = Position.objects.filter(id = int(kwargs['id']))

        # checking if position exitis else delete position documents
        if currentPositionInstance.count() == 0:
            PositionsDocument.objects.filter(positionID = int(kwargs['id'])).delete()
            return Response({"result":"deleted"})
        currentPositionInstance = currentPositionInstance[0]

        newChartInstance = Chart.objects.get(id = request.data['newChartID'])

        member = {
            "chart" : newChartInstance.id
        }

        memSerial = MembersSerializer(instance=currentPositionInstance, data=member, partial=True)
        memSerial.is_valid(raise_exception=True)
        memSerial.update(instance=currentPositionInstance, validated_data=memSerial.validated_data)

        return Response({})



    # security check has been remain
    # this invitation are only avalaible by the reciever user
    # but in this sprint company owner can do that
    def create(self, request, *args, **kwargs):
        companyInstance = Company.objects.get(id=kwargs["companyID_id"])
        currentUserInstance = request.user
        invitationInstance = CompanyMembersJointRequest.objects.get(id=request.data["invitationID"])
        chartInstance = Chart.objects.get(id=invitationInstance.chart)
        # the user who is suppose to get position
        userInstance = MyUser.objects.get(id=invitationInstance.sender.userID)
        # checking if position exits
        positions = Position.objects.filter(
            company=companyInstance,
            user=userInstance
        )
        if positions.count() > 0:
            return Response(
                data={
                    "message": _("This person has an exiting position in your selected company, please drop him first ")
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # ------------------------------
        newItem = {
            'chart': chartInstance,
            'user': userInstance,
            'company': companyInstance,
        }
        serializer = self.serializer_class(data=newItem)
        if serializer.is_valid():
            serializer.validated_data["chart"] = chartInstance
            serializer.validated_data["user"] = userInstance
            serializer.validated_data["company"] = companyInstance
            serializer.create(serializer.validated_data)
            headers = self.get_success_headers(serializer.data)
            invitationInstance.delete()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # this is for currnet company selector
    @list_route(methods=['get'])
    def CompaniesForCurrent(self, request, *args, **kwargs):
        queryset = PositionsDocument.objects.filter(userID=request.user.id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PositionDocumentSerializer(page, many=True, fields=('companyID', 'companyName'))
            return self.get_paginated_response(serializer.data)

        serializer = PositionDocumentSerializer(queryset, many=True, fields=('companyID', 'companyName'))
        return Response(serializer.data)



class PositionsListViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'id'
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    pagination_class = DetailsPagination

    def get_queryset(self):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)

        self.queryset = QuerySetFilter().filter(
            querySet=CompanyReciever.objects.filter(companyID=self.request.user.current_company.id),
            kwargs=self.request.query_params
        )
