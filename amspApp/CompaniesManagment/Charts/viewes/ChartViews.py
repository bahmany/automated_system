from asq.initiators import query
from bson import ObjectId
from datetime import datetime
import collections
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework import status
from amspApp.CompaniesManagment.Charts.models import Chart
from amspApp.CompaniesManagment.Charts.serializers.ChartSerializers import ChartSerializer
from amspApp.CompaniesManagment.CompanyProfile.models import CompanyProfile
from amspApp.CompaniesManagment.Positions.models import Position, PositionsDocument
from amspApp.CompaniesManagment.Positions.serializers.PositionSerializer import PositionSerializer, \
    PositionDocumentSerializer
from amspApp.CompaniesManagment.Secretariat.models import Secretariat, SecretariatPermissions
from amspApp.CompaniesManagment.Secretariat.serializers.SecretariatsSerializers import SecretariatSerializer, \
    SecretariatSerializerPermission
from amspApp.CompaniesManagment.members.serializers.MemberSerializer import MembersSerializer
from amspApp.CompaniesManagment.models import Company
from amspApp.CompaniesManagment.permissions.CompanyPermissions import CanCruid, IsOwnerOrReadOnly
from amspApp.CompaniesManagment.permissions.PermissionChecker import get_permissions
from amspApp.CompaniesManagment.views.CompanyMembersJointRequestView import CompanyMembersJointRequestViewset
from amspApp.Infrustructures.Classes.PublicFilters import QuerySetFilter
from amspApp.MyProfile.models import Profile, HiddenProfiles
from amspApp.MyProfile.serializers.ProfileSerializer import ProfileSerializer, HiddenProfilesSerializer
from amspApp._Share.ListPagination import ListPagination
from django.utils.translation import ugettext_lazy as _
from amspApp.amspUser.models import MyUser
from amspApp.amspUser.serializers.UserSerializer import UserSerializer
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class ChartViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = ChartSerializer
    queryset = Chart.objects.all()
    pagination_class = ListPagination
    permission_name = "Can_Edit_company_chart"
    permission_classes = (CanCruid,)

    def get_permissions(self):
        return get_permissions(self, ChartViewSet)

    def get_queryset(self):

        compID = self.kwargs.get("companyID_id")

        if (compID == None) or (compID == "") or (compID == "undefined"):
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(self.request)
            self.kwargs["companyID_id"] = posiIns.companyID

        companyInstance = Company.objects.get(id=self.kwargs["companyID_id"])
        self.queryset = Chart.objects.filter(owner=companyInstance)
        # if self.queryset.count() == 0:
        #     self.serializer_class().create_default_chart(companyInstance)
        #     self.queryset = Chart.objects.filter(owner=companyInstance)
        return self.queryset

    def destroy(self, request, *args, **kwargs):
        instance = Chart.objects.get(
            id=kwargs["id"],
        )
        if (Chart.objects.all().filter(top=instance).count() > 0):
            return Response(status=status.HTTP_403_FORBIDDEN, data={"msg": "Please remove subbrances first"})

        # checking if this chart has position ot not

        positionCount = Position.objects.filter(chart=instance).count()

        if positionCount > 0:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"msg": "Please remove positions first"})

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def template_page(self, request, *args, **kwargs):
        return render_to_response("companyManagement/Chart/CompanyChart.html", {},
                                  context_instance=RequestContext(self.request))

    def list(self, request, *args, **kwargs):
        # getting current company if compnay id not defined
        if self.kwargs["companyID_id"] == "0" or self.kwargs["companyID_id"] == "-1" or self.kwargs[
            "companyID_id"] == "undefined":
            companyInstance = request.user.current_company
        else:
            companyInstance = Company.objects.get(id=self.kwargs["companyID_id"])
        queryset = Chart.objects.all().filter(owner=companyInstance)
        if "q" in request.query_params:
            if request.query_params["q"] != "":
                queryset = queryset.filter(title__contains=request.query_params["q"])

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, fields=('id', 'title'))
        return Response(serializer.data)

    @list_route(methods=['get'])
    def jsonRecursiveChart(self, request, *args, **kwargs):
        companyInstance = Company.objects.get(id=self.kwargs["companyID_id"])
        return Response(self.serializer_class().get_json_chart(companyInstance))

    @detail_route(methods=['post'])
    def ChangeLevel(self, request, *args, **kwargs):
        # here i have to check if the person is owner of company or not
        companyInstance = Company.objects.get(
            id=self.kwargs["companyID_id"],
        )
        chartItemInstance = Chart.objects.get(
            id=kwargs["id"],
            owner=companyInstance
        )
        chartSerial = ChartSerializer(instance=chartItemInstance, data={
            "top": Chart.objects.get(id=request.DATA["parentId"]).id}, partial=True)
        chartSerial.is_valid(raise_exception=True)
        chartSerial.save()
        return Response(chartSerial.data)

    @detail_route(methods=['post'])
    def AddNewChart(self, request, *args, **kwargs):
        # here i have to check if the person is owner of company or not
        companyInstance = Company.objects.get(
            id=self.kwargs["companyID_id"],
        )
        chartItemInstance = Chart.objects.get(
            id=kwargs["id"],
            owner=companyInstance
        )
        newChart = self.serializer_class(
            data={
                "title": request.DATA["name"],
                "top": chartItemInstance.id,
                "owner": companyInstance.id})

        newChart.is_valid(raise_exception=True)
        newChart = newChart.create(newChart.validated_data)

        return Response(self.serializer_class(instance=newChart).data)

    @detail_route(methods=['post'])
    def ChangeChartName(self, request, *args, **kwargs):
        # here i have to check if the person is owner of company or not
        if len(request.data["name"]) < 1:
            return Response(
                {
                    "status": "Bad request",
                    "message": [{"name": _("PositionName"), "message": _("This field is required")}]},
                status.HTTP_400_BAD_REQUEST
            )
        companyInstance = Company.objects.get(
            id=self.kwargs["companyID_id"],

        )
        chartItemInstance = Chart.objects.get(
            id=kwargs["id"],
            owner=companyInstance
        )
        chartSerial = ChartSerializer(instance=chartItemInstance, data={
            "title": request.data["name"]}, partial=True)
        chartSerial.is_valid(raise_exception=True)
        chartSerial.save()

        # chartItemInstance.title = request.DATA["name"]
        # chartItemInstance.save()
        #
        # res = self.serializer_class(instance=chartItemInstance)

        return Response(chartSerial.data)

    @detail_route(methods=['post'])
    def ChangeChartRank(self, request, *args, **kwargs):
        # here i have to check if the person is owner of company or not
        if request.data["rank"] < -1:
            return Response(
                {
                    "status": "Bad request",
                    "message": [{"name": _("PositionName"), "message": _("This field is required")}]},
                status.HTTP_400_BAD_REQUEST
            )
        companyInstance = Company.objects.get(id=self.kwargs["companyID_id"], )
        chartItemInstance = Chart.objects.get(
            id=kwargs["id"], owner=companyInstance)
        chartSerial = ChartSerializer(
            instance=chartItemInstance,
            data={"rank": request.data["rank"]}, partial=True)
        chartSerial.is_valid(raise_exception=True)
        chartSerial.save()
        return Response(chartSerial.data)

    @detail_route(methods=['post'])
    def ChangeCell(self, request, *args, **kwargs):
        posID = PositionsDocument.objects.filter(positionID=kwargs['id'], chartID__ne=None, companyID__ne=None,
                                                 positionID__ne=None, ).order_by('-id').first()
        if posID:
            userInstance = MyUser.objects.get(id=posID.userID)
            userInstance.cellphone = request.data.get('newCell')
            userInstance.save()

            return Response({'msg': 'ok'})
        return Response({'msg': "notok"})

    @detail_route(methods=['post'])
    def ChangePersCode(self, request, *args, **kwargs):
        posID = PositionsDocument.objects.filter(positionID=kwargs['id'], chartID__ne=None, companyID__ne=None,
                                                 positionID__ne=None, ).order_by('-id').first()
        if posID:
            userInstance = MyUser.objects.get(id=posID.userID)
            userInstance.personnel_code = request.data.get('newCell')
            userInstance.save()

            return Response({'msg': 'ok'})
        return Response({'msg': "notok"})

    @detail_route(methods=["post"])
    def UpdatePost(self, request, *args, **kwargs):
        companyInstance = Company.objects.get(
            id=self.kwargs["companyID_id"],
        )

        userInstance = MyUser.objects.get(id=request.data['UserID'])

        positionInstance = Position.objects.filter(
            company=companyInstance,
            user=userInstance,
        )

        if positionInstance.count() == 0:
            chart = Chart.objects.get(id=request.data["NewPositionID"])
            newPosition = {
                "chart": chart,
                "user": userInstance,
                "company": companyInstance,
                "post_date": datetime.now()
            }
            created = MembersSerializer().create(newPosition)
            return Response(created.data)
        positionInstance = Position.objects.get(
            company=companyInstance,
            user=userInstance,
        )
        newChartInstance = Chart.objects.get(
            owner=companyInstance,
            id=request.data['NewPositionID']
        )

        positionInstance.chart = newChartInstance
        updatingPos = MembersSerializer(instance=positionInstance, data={
            "chart": newChartInstance.id,
            "user": userInstance.id,
            "company": companyInstance.id,
            "post_date": datetime.now()

        }, partial=True)

        if updatingPos.is_valid():
            updatingPos.save()

            return Response({})

    """
    here i have to update 2 places
    1: my sql
    2: mongo
    i have to say both of them to empty user id !!! :))
    """

    @detail_route(methods=["post"])
    def ForceOut(self, request, *args, **kwargs):
        companyInstance = Company.objects.get(
            id=self.kwargs["companyID_id"],
        )

        mySqlPositionInstance = Position.objects.filter(
            id=request.data["positionID"]
        )

        if mySqlPositionInstance.count() > 0:
            updating = {"user": None}
            memSerial = MembersSerializer(instance=mySqlPositionInstance[0], data=updating, partial=True)
            memSerial.is_valid(raise_exception=True)
            memSerial.update(instance=mySqlPositionInstance[0], validated_data=memSerial.validated_data)

        return Response({})

    """
    Adding person to new position
    """

    @list_route(methods=["post"])
    def addPersonToNewPosition(self, request, *args, **kwargs):
        res = CompanyMembersJointRequestViewset().create(
            request, *args, **kwargs)
        request.data["invitationID"] = res.data["id"]

        res = CompanyMembersJointRequestViewset().DoInvite(request, *args, **kwargs)

        return res

    @list_route(methods=["post"])
    def addPersonToOldPosition(self, request, *args, **kwargs):
        companyInstance = Company.objects.get(id=int(kwargs['companyID_id']))
        userInstance = MyUser.objects.get(username=request.data['newUsername'])
        positionInstance = Position.objects.get(id=request.data['selectedPosition'])

        # check if this user has no position id
        cnt = Position.objects.filter(company_id=companyInstance.id, user_id=userInstance.id).count()

        if cnt > 0:
            raise Exception("این کاربر قبلا سمت دهی شده است - لطفا ابتدا آنرا تعلیق و سپس سمت دهی نمایید")

        memberSerial = MembersSerializer(instance=positionInstance, data={
            "user": userInstance.id
        }, partial=True)
        memberSerial.is_valid(raise_exception=True)
        memberSerial.update(positionInstance, memberSerial.validated_data)
        return Response({})

    """
    Adding person to exiting position
    """

    @list_route(methods=["post"])
    def AddToChart(self, request, *args, **kwargs):
        res = CompanyMembersJointRequestViewset().create(
            request, *args, **kwargs)
        request.data["invitationID"] = res.data["id"]

        res = CompanyMembersJointRequestViewset().DoInvite(request, *args, **kwargs)

        return res

    @detail_route(methods=["post"])
    def RemoveFromInbox(self, request, *args, **kwargs):
        companyInstance = Company.objects.get(
            id=self.kwargs["companyID_id"],
        )
        mySqlPositionInstance = Position.objects.get(
            chart=request.data["chartID"],
            company=companyInstance.id,
            user=request.data["userID"],
        )
        updating = {
            "chart": None,
            "company": None
        }
        serial = MembersSerializer(instance=mySqlPositionInstance, data=updating, partial=True)
        serial.is_valid(raise_exception=True)
        serial.update(mySqlPositionInstance, updating)
        return Response({})

    """
    This method gets long time :
    1- it gets the sec
    2- then checked sec permissions
    3- if sec has no perm then created it with all sec and then make the first one default
    4- if a chart has no default it sets the first one as default sec
    5- then return list of sec permissions
    """

    @detail_route(methods=["get"])
    def getSecWithChartPerm(self, request, *args, **kwargs):
        # getting secs
        companyInstance = Company.objects.get(
            id=self.kwargs["companyID_id"],

        )
        result = {}
        """
        byte[0] = Access to current dabir
        byte[1] = Access to current sadere
        byte[2] = Access to current varede
        """
        chartInstance = Chart.objects.get(
            owner=companyInstance,
            id=kwargs['id']
        )

        def findSadereInPerm(DabirID, items):
            for item in items:
                if item.secretariat_id == DabirID:
                    if item.permission == "":
                        return [
                            False,
                            False,
                            False
                        ]
                    else:
                        return [
                            True if item.permission[0] == "1" else False,
                            True if item.permission[1] == "1" else False,
                            True if item.permission[2] == "1" else False
                        ]
                    return item.permission
            return [
                False,
                False,
                False
            ]

        dabirList = Secretariat.objects.all().filter(company=companyInstance).order_by("id")
        permissionList = SecretariatPermissions.objects.all().filter(chart=chartInstance)
        dabirList = list(dabirList)
        dabirListDict = dabirList
        permissionList = list(permissionList)
        dabirListDict = [
            {"Name": x.name,
             "Id": x.id,
             "perm": findSadereInPerm(x.id, permissionList)} for x in dabirList
        ]
        defaultID = 0
        # detect that there is no dabir permission for the following chart
        # must creates for this
        if len(permissionList) == 0:
            for dl in dabirList:
                new = {
                    "chart": chartInstance,
                    "secretariat": dl,
                    "permission": "100",
                    "default": False,
                }
                newSer = SecretariatSerializerPermission().create(new)
                return self.getSecWithChartPerm(request, *args, **kwargs)
        for p in permissionList:
            defaultID = p.secretariat_id if p.default else 0
            if defaultID != 0:
                break;
        if defaultID == 0:
            permissionList[0].default = True
            permissionList[0].save()
            return self.getSecWithChartPerm(request, *args, **kwargs)
        for d in dabirListDict:
            if d["Id"] == defaultID:
                d["default"] = True
            else:
                d["default"] = False
        return Response(dabirListDict)

    @detail_route(methods=["post"])
    def updateSecPerm(self, request, *args, **kwargs):
        data = request.data
        companyInstance = Company.objects.get(
            id=self.kwargs["companyID_id"],
        )
        chartInstance = Chart.objects.get(
            owner=companyInstance,
            id=kwargs['id']
        )
        secInstance = Secretariat.objects.get(id=data["Id"])

        # check if has permission before or not ??

        countOf = SecretariatPermissions.objects.filter(chart=chartInstance, secretariat=secInstance).count()
        if countOf == 0:
            SecretariatSerializerPermission().create({
                "chart": chartInstance,
                "secretariat": secInstance,
                "permission": "000",
                "default": False,
            })
            return self.updateSecPerm(request, *args, **kwargs)

        permissionInstace = SecretariatPermissions.objects.get(chart=chartInstance, secretariat=secInstance)
        if data['default']:
            SecretariatPermissions.objects.filter(chart=chartInstance).update(default=False)
            permissionInstace.default = True
        permissionInstace.permission = "".join(map(str, map(int, data["perm"])))
        permissionInstace.save()
        return Response({})

    @list_route(methods=["get"])
    def GetAllCharts(self, request, *args, **kwargs):
        allCompanyInstance = Company.objects.filter(owner_user=request.user.id)
        allChartsInstance = Chart.objects.filter(owner__in=allCompanyInstance)
        queryset = allChartsInstance.filter(
            (
                    Q(owner__name__icontains=request.query_params["q"]) |
                    Q(title__icontains=request.query_params["q"])
            ) &
            (
                ~Q(top_id=None)
            )
        )
        page = self.paginate_queryset(queryset)

        # now getting empty positions
        emptyPositions = Position.objects.filter(
            Q(company__icontains=allCompanyInstance)
            &
            Q(user=None)
        )
        rendered = [collections.OrderedDict({
            "CompanyID": x.company_id,
            "CompanyName": x.company.name,
            "id": x.chart_id,
            "title": x.chart.title,
            "rank": x.chart.rank,
            "isEmpty": True,
            "positionID": x.id
        }) for x in emptyPositions]

        if page is not None:
            serializer = self.get_serializer(page, many=True, fields=('CompanyID', "id", "CompanyName", "title"))
            dt = serializer.data
            finalList = rendered + dt
            result = self.get_paginated_response(finalList)
            return result

        # serializer = self.get_serializer(queryset, many=True, fields=('CompanyID',"id","CompanyName","title"))
        # return Response(serializer.data)
        # serializer = self.get_serializer(queryset, many=True, fields=('CompanyID',"id","CompanyName","title"))
        return Response({})

    @detail_route(methods=["post"])
    def DeleteAccount(self, request, *args, **kwargs):
        # start deleting !!!
        # deleting inboxes :
        if request.user.username != "bahmany":
            return Response({"result": "Access Denied"})
        newHidden = {
            'profile': request.data['id'],
            "companyID": int(kwargs['companyID_id'])
        }
        serial = HiddenProfilesSerializer(data=newHidden)
        serial.is_valid(raise_exception=True)
        serial.save()
        return Response({})

    @list_route(methods=["get"])
    def GetAllChartsCurrent(self, request, *args, **kwargs):
        charts = list(self.queryset.filter(
            Q(owner=int(kwargs['companyID_id'])) & ~Q(top=None)
        ).order_by("title"))
        # converting charts to its upper list to send to client
        charts = query(charts).select(lambda x: {
            'id': x.id,
            'title': x.title,
            'rank': x.rank,
            'topID': x.top_id if x.top else None,
            'topTitle': x.top.title if x.top else None,
            'personelCount': x.set_position.count()
        }).to_list()
        return Response(charts)

    @list_route(methods=["get"])
    def GetAllChartsCurrentTopChart(self, request, *args, **kwargs):
        charts = list(self.queryset.filter(
            Q(owner=int(kwargs['companyID_id'])) & ~Q(id=int(request.query_params['selectedID'])),
        ).order_by("title"))
        # converting charts to its upper list to send to client
        charts = query(charts).select(lambda x: {
            'id': x.id,
            'title': x.title,
        }).to_list()
        return Response(charts)

    @detail_route(methods=['get'])
    def PositionsList(self, request, *args, **kwargs):
        queryset = PositionsDocument.objects.filter(chartID=kwargs["id"], companyID=kwargs["companyID_id"])
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PositionDocumentSerializer(page, many=True, fields=('id', 'profileName'))
            return self.get_paginated_response(serializer.data)

        serializer = PositionDocumentSerializer(queryset, many=True, fields=('id', 'profileName'))
        return Response(serializer.data)

    @list_route(methods=['get'])
    def PositionsWhitoutPageList(self, request, *args, **kwargs):
        companyInstance = Company.objects.get(id=self.kwargs["companyID_id"])
        queryset = Chart.objects.all().filter(owner=companyInstance).order_by("title")
        # queryset = PositionsDocument.objects.filter(chartID=kwargs["id"],companyID=kwargs["companyID_id"])
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = PositionDocumentSerializer(page, many=True, fields=('id', 'profileName'))
        #     return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, fields=('id', 'title'))
        return Response({'results': serializer.data})

    # @list_route(methods=['get'])
    def CreateChartFromSpecificPoint(self, chartInstance):
        hii = []

        def createChartFromTop(ci, res):
            cList = Chart.objects.filter(top=ci)
            for c in cList:
                res = createChartFromTop(c, res)
            if res: res.append(ci)

        createChartFromTop(chartInstance, hii)


