from amspApp.BI.models import BIDashboardPage
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class BIDashboardPageSerializers(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = BIDashboardPage

    def to_representation(self, instance):
        result = super(BIDashboardPageSerializers, self).to_representation(instance)
        return result


