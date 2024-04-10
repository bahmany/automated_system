from rest_framework_mongoengine.serializers import DynamicDocumentSerializer

from amspApp.Fees.models import FeeItem, Fee


class FeeSerializer(DynamicDocumentSerializer):
    class Meta:
        model = Fee
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

class FeeItemSerializer(DynamicDocumentSerializer):
    class Meta:
        model = FeeItem
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

