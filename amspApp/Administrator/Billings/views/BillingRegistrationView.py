from rest_framework import viewsets
from amspApp.Administrator.Billings.models import Billing_Strategies, Billing_Payments
from amspApp.Administrator.Billings.serializers.BillingSerializer import BillingSerializer, PaymentSerializer
from amspApp.Administrator.Customers.forms.PaymentForm import PaymentForm
from amspApp.Administrator.Customers.models import Billing_Customer
from amspApp.Administrator.Customers.serializers.CustomersSerializer import CustomerSerializer
from amspApp.Administrator.permission.IsSuperUser import IsSuper
from amspApp._Share.ListPagination import DetailsPagination, ListPagination

__author__ = 'mohammad'





class BillingRegistrationViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Billing_Strategies.objects.all().order_by("-id")
    serializer_class = BillingSerializer
    pagination_class = ListPagination
    permission_classes = (IsSuper,)

    def create(self, request, *args, **kwargs):
        request.data["createdUserID"] = request.user.id
        return super(BillingRegistrationViewSet, self).create(request, *args, **kwargs)



class PaymentViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Billing_Payments.objects.all().order_by("-id")
    serializer_class = PaymentSerializer
    pagination_class = ListPagination

    def create(self, request, *args, **kwargs):
        # request.data["billingStrategyLink_id"] = int(request.data['billingStrategyLink'])
        # request.data["billingStrategyLink"] = int(request.data['billingStrategyLink'])
        # request.data["billingStrategyLink"] = Billing_Strategies.objects.get(id = int(request.data['billingStrategyLink']))
        request.data["createdUserID"] = request.user.id
        pf = PaymentForm(request.data)
        if pf.is_valid():
            ss = pf.save()
        return ss


    def retrieve(self, request, *args, **kwargs):
        result = super(PaymentViewSet, self).retrieve(request, *args, **kwargs)
        result.data["billingStrategyLink"] = str(result.data["billingStrategyLink"])
        result.data["customerLink"] = str(result.data["customerLink"])
        return result



        # return super(PaymentViewSet, self).create(request, *args, **kwargs)





