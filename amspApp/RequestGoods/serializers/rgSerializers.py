from rest_framework import serializers

from amspApp.RequestGoods.models import RequestGood, RequestGoodItems, RequestGoodItemsHamkaran, RequestGoodSigns
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class RequestGoodSerializer(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = RequestGood

class RequestGoodSignsSerializer(DynamicFieldsDocumentSerializer):
    comment = serializers.CharField(allow_blank=True, allow_null=True)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = RequestGoodSigns




class RequestGoodItemsSerializer(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = RequestGoodItems


class RequestGoodItemsHamkaranSerializer(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = RequestGoodItemsHamkaran
