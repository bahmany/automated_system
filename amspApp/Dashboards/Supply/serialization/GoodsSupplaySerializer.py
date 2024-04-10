from amspApp.Dashboards.Supply.models import GoodsProviders, SupplementCategories
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class GoodsProvidersSerializer(DynamicFieldsDocumentSerializer):
    class Meta:
        model = GoodsProviders

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

class SupplementCategoriesSerializer(DynamicFieldsDocumentSerializer):
    class Meta:
        model = SupplementCategories

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)
