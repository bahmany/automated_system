
from rest_framework_mongoengine import viewsets
from amspApp.CompaniesManagment.Positions.models import Position
from amspApp.Letter.models import ExportScannedAfterSend
from amspApp.Letter.serializers.LetterSecretariatSerializer import ExportScannedAfterSendSerializer

from amspApp._Share.ListPagination import DetailsPagination


class ExportScannedAfterSendViewSet(viewsets.ModelViewSet):
    pagination_class = DetailsPagination
    lookup_field = "id"
    serializer_class = ExportScannedAfterSendSerializer
    queryset = ExportScannedAfterSend.objects.all()

    def get_queryset(self):
        self.queryset = self.queryset.filter(inboxID=self.request.query_params['id']).order_by("-id")
        return self.queryset

    def create(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=request.user,
            company=request.user.current_company)
        request.data["positionID"] = pos.id
        return super(ExportScannedAfterSendViewSet, self).create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.get_queryset()
        return super(ExportScannedAfterSendViewSet, self).list(request, *args, **kwargs)



