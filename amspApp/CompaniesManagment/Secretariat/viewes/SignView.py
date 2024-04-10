from rest_framework_mongoengine import viewsets
from amspApp.CompaniesManagment.Secretariat.models import Sign
from amspApp.CompaniesManagment.Secretariat.serializers.SignSerializer import SignSerializer
from amspApp._Share.ListPagination import ListPagination


class SignViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Sign.objects.all()
    serializer_class = SignSerializer
    pagination_class = ListPagination
    # filter_backends = (filters.DjangoFilterBackend,)





