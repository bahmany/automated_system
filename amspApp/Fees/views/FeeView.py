from rest_framework_mongoengine import viewsets

from amspApp.Fees.models import Fee
from amspApp.Fees.serializers.FeeSerializer import FeeSerializer
from amspApp._Share.ListPagination import DataTableForNewDatables_net


class FeeViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Fee.objects.all().order_by('-id')
    serializer_class = FeeSerializer
    pagination_class = DataTableForNewDatables_net

    SahmbariCols = [
        dict(numericFormat={}, dataType='text', readOnly=True, id=1, data='radeef', title='ردیف'),
        dict(numericFormat={}, dataType='text', readOnly=True, id=1, data='name1', title='ضخامت'),
        dict(numericFormat={}, dataType='text', readOnly=True, id=1, data='name2', title='تمپر'),
        dict(numericFormat={}, dataType='text', readOnly=True, id=1, data='fee', title='قیمت'),
        dict(numericFormat={}, dataType='text', readOnly=True, id=1, data='fee_with_vat', title='قیمت با ارزش افزوده'),

    ]