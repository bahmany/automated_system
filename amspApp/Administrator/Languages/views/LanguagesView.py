from rest_framework import viewsets
from amspApp.Administrator.Customers.models import Billing_Customer
from amspApp.Administrator.Customers.serializers.CustomersSerializer import CustomerSerializer
from amspApp.Administrator.Languages.serializers.LanguagesSerializer import LanguagesSerializer
from amspApp.Administrator.permission.IsSuperUser import IsSuper
from amspApp._Share.ListPagination import DetailsPagination, ListPagination
from amspApp.models import Languages

__author__ = 'mohammad'





class LanguagesRegistrationViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Languages.objects.all().order_by("-id")
    serializer_class = LanguagesSerializer
    permission_classes = (IsSuper,)


    def create(self, request, *args, **kwargs):
        return super(LanguagesRegistrationViewSet, self).create(request, *args, **kwargs)





