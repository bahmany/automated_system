from amspApp.Administrator.Customers.models import Billing_Customer
from amspApp._Share.DynamicFieldModelSerializer import DynamicFieldsModelSerializer
from amspApp.models import Languages


class LanguagesSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Languages
        # fields = "__all__"