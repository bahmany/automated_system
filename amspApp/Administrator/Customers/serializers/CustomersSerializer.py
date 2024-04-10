from amspApp.Administrator.Customers.models import Billing_Customer
from amspApp._Share.DynamicFieldModelSerializer import DynamicFieldsModelSerializer


class CustomerSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Billing_Customer
        # fields = "__all__"