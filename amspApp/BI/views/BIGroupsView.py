from django.contrib.auth.models import Group
from mongoengine import Q
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.BI.models import BIGroups
from amspApp.BI.serializers.BIGroupsSerial import BIGroupsSerializers
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.Positions.serializers.PositionSerializer import PositionDocumentLessDataSerializer
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class BIGroupsViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = BIGroups.objects.all().order_by('-id')
    serializer_class = BIGroupsSerializers

    def list(self, request, *args, **kwargs):
        result = super(BIGroupsViewSet, self).list(request, *args, **kwargs)
        for r in result.data:
            r['user_count'] = len(r['groupMember'])
            # del r['groupMember']
        return result

    def initial(self, request, *args, **kwargs):
        # airflow = AirflowConnector()
        # airflow.get_list('connections')

        if request.method != "GET" and request.method != "DELETE":
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            # _mutable = request.data._mutable
            # request.data._mutable = True
            request.data["positionID"] = posiIns.positionID
            # request.data._mutable = _mutable
        return super(BIGroupsViewSet, self).initial(request, *args, **kwargs)

    @list_route(methods=["get"])
    def get_all_member(self, request, *args, **kwargs):
        if request.query_params["q"] == 'undefined':
            request.query_params["q"] = ''
        if request.query_params["q"] == None:
            request.query_params["q"] = ''
        q = Q(profileName__contains=request.query_params["q"]) | Q(chartName__contains=request.query_params["q"])
        qq = Q(companyID=self.request.user.current_company_id) & Q(userID__ne=None)
        q = q & qq
        positions = PositionsDocument.objects.filter(q).limit(30)
        posins = PositionDocumentLessDataSerializer(instance=positions, many=True).data
        return Response(posins)

    def destroy(self, request, *args, **kwargs):
        instance = self.queryset.get(id=kwargs.get('id'))
        if len(instance.groupMember) > 0:
            return Response({'msg': 'ابتدا اعضا را حذف نمایید'}, status=status.HTTP_400_BAD_REQUEST)
        return super(BIGroupsViewSet, self).destroy(request, *args, **kwargs)
