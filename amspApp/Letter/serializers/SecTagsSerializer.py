from amspApp.Letter.models import SecTag, SecTagItems
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class SecTagSerializer(DynamicFieldsDocumentSerializer):

    class Meta:
        model = SecTag
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()
    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)



class SecTagItemSerializer(DynamicFieldsDocumentSerializer):

    class Meta:
        model = SecTagItems
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()
    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)



