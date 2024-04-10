from amspApp.BI.models import BIMenu, BIMenuItem, BIDashboardPage
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer
from rest_framework import serializers


class BIMenuSerializers(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = BIMenu


class BIMenuItemSerializers(DynamicFieldsDocumentSerializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=BIMenuItem.objects.all(), required=False, allow_null=True)
    page = serializers.PrimaryKeyRelatedField(queryset=BIDashboardPage.objects.all(), required=False, allow_null=True)
    # parent = serializers.RelatedField(source='id', read_only=True)


    def parent_to_representation(self, instance):
        result = super(BIMenuItemSerializers, self).to_representation(instance)
        return result

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = BIMenuItem


class BIMenuItemSumSerializers(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = BIMenuItem
        depth = 1
