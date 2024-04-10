from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from amspApp.CompaniesManagment.Charts.models import ChartZones, ZoneItems, Chart
from amspApp.CompaniesManagment.Charts.serializers.ZoneSerializers import ZoneSerializer, ZoneItemsSerializer
from amspApp.CompaniesManagment.Positions.models import Position, PositionsDocument
from amspApp.CompaniesManagment.members.serializers.MemberSerializer import MembersDocumentSerializer
from amspApp.CompaniesManagment.models import Company
from amspApp.CompaniesManagment.permissions.CompanyPermissions import CanCruid
from amspApp.CompaniesManagment.permissions.PermissionChecker import get_permissions
from amspApp._Share.ListPagination import ListPagination

__author__ = 'mohammad'


class ZoneViewSet(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = ZoneSerializer
    pagination_class = ListPagination
    permission_name = "Can_Edit_company_chart"
    permission_classes = (CanCruid,)

    def get_permissions(self):
        return get_permissions(self, ZoneViewSet)



    def get_queryset(self):
        self.queryset = ChartZones.objects.filter(
            company_id=self.kwargs["companyID_id"]
        ).order_by("-id")
        return self.queryset

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)




    @detail_route(methods=['get'])
    def GetListWithSelected(self, request, *args, **kwargs):
        zones = list(self.get_queryset())
        companyInstance = Company.objects.get(
            id=self.kwargs["companyID_id"])

        if kwargs["id"] == "0":
            selected = ChartZones.objects.filter(company = companyInstance)
        else:
            chartInstance = Chart.objects.get(id = kwargs["id"])
            selected = chartInstance.set_zones.all()


        result = []
        for z in zones:
            ss = {}
            ss["id"] = z.id
            ss["title"] = z.title
            ss["company"] = z.company_id
            ss["post_date"] = z.post_date
            ss["selected"] = False
            if kwargs["id"] != "0":
                for s in selected:
                    if s.zone_id == z.id:
                        ss["selected"] = True

            result.append(ss)
        returnResult = {
            "results":result
        }

        return Response(returnResult)


    @detail_route(methods=['post'])
    def ToggleZone(self, request, *args, **kwargs):
        companyInstance = Company.objects.get(
            id=self.kwargs["companyID_id"])
        chartInstance = Chart.objects.get(
            id=request.DATA['selectedChartID']
        )

        zoneInstance = ChartZones.objects.get(id=request.DATA["id"])

        ZoneItems.objects.all().filter(
            zone=zoneInstance,
            chart=chartInstance,
        ).delete()
        if request.DATA["selected"]:
            newInstance = {
                "zone": zoneInstance.id,
                "chart": chartInstance.id
            }
            newInstance = ZoneItemsSerializer(data=newInstance)
            if newInstance.is_valid():
                newInstance.save()
                return Response(newInstance.data)
            else:
                return Response(newInstance.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status.HTTP_200_OK)

    @list_route(methods=['get'])
    def GetZoneMembers(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        SelectedZoneInstance = ChartZones.objects.get(
            id = request.query_params["id"],
            company = self.request.user.current_company
            )
        SelectedZoneItems = ZoneItems.objects.filter(zone = SelectedZoneInstance)

        Charts = Chart.objects.filter(id__in = [x.chart_id for x in SelectedZoneItems])

        posDocList = PositionsDocument.objects.filter(chartID__in = [x.id for x in Charts])

        res = []
        for p in posDocList:
            xx = MembersDocumentSerializer(instance=p).data
            xx.pop("desc", None)
            res.append(xx)
        return Response(res)


