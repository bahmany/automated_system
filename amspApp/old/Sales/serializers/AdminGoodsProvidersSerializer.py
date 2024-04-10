from amspApp.Virtual.Tamin.models import GoodsProviders
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class AdminGoodsProvidersSerializer(DynamicFieldsDocumentSerializer):
    class Meta:
        model = GoodsProviders

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)
