from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework.filters import OrderingFilter
from rest_framework_mongoengine import viewsets

from amspApp.ControlProject.permissions.ControlProjectBase import IsOwnerOrReadOnly_CostCol
from amspApp.Infrustructures.Classes.MongoEngineSearchFilterBackend import MongoSearchFilter, FilterCompanyID
from amspApp.QC.models import QCAuditingSchedule
from amspApp.QC.serializers.QCAuditShedualsSerializer import QCAuditingScheduleSerializer
from amspApp.Sales.permissions.basePermissions import CanCruidSale
from amspApp._Share.ListPagination import DetailsPagination


class QCqcScheduleViewSet(viewsets.ModelViewSet):

    pagination_class = DetailsPagination
    lookup_field = "id"
    serializer_class = QCAuditingScheduleSerializer
    queryset = QCAuditingSchedule.objects.all().order_by('-id')
    permission_classes = (IsOwnerOrReadOnly_CostCol, CanCruidSale)
    filter_backends = (MongoSearchFilter, FilterCompanyID, OrderingFilter)
    search_fields = ("desc__Sharh",)

    def template_view_read(self, request):
        return render_to_response('QC/Scheduals/base.html', {}, context_instance=RequestContext(request))
