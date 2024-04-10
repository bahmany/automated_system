from rest_framework_mongoengine.serializers import DocumentSerializer
from amspApp.CompaniesManagment.Hamkari.models import Hamkari


class HamkariSerializer(DocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = Hamkari