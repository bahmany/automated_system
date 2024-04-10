from rest_framework import serializers

from amspApp.Sales.models import SaleConversations, SaleConversationComments, SaleConversationItems, \
    SaleConversationCommentsReplays, SaleCurrentBasket
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class SaleConversationSerializer(DynamicFieldsDocumentSerializer):
    CustomerID = serializers.IntegerField(label="CustomerID", required=False, allow_null=True)
    PrefactorID = serializers.CharField(label="PrefactorID", required=False, allow_null=True)
    Files = serializers.DictField(label="Files", required=False, allow_null=True)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = SaleConversations


class SaleConversationCommentsSerializer(DynamicFieldsDocumentSerializer):
    confirmedBy = serializers.DictField(label="confirmBy", required=False)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = SaleConversationComments

    depth = 1

class SaleCustomerSaleBasket(DynamicFieldsDocumentSerializer):
    desc = serializers.DictField(label="Desc", required=False)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = SaleCurrentBasket

    depth = 1


class SaleConversationCommentsReplaysSerializer(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = SaleConversationCommentsReplays

    depth = 1


class SaleConversationItemsSerializer(DynamicFieldsDocumentSerializer):
    index = serializers.IntegerField(label="CustomerID", required=False, allow_null=True)
    arzeBadAzTrim = serializers.FloatField(label="CustomerID", required=False, allow_null=True)
    paymentType = serializers.CharField(label="paymentType", required=False, allow_null=True)
    itemID = serializers.CharField(label="paymentType", required=False, allow_null=True, allow_blank=True)
    itemName = serializers.CharField(label="paymentType", required=False, allow_null=True, allow_blank=True)
    comment = serializers.CharField(label="comment", required=False, allow_null=True, allow_blank=True)
    ignore = serializers.NullBooleanField(label="ignore", required=False)
    # itemID = serializers.CharField(required=False, allow_null=True, allow_blank=True)  # ID in hamkaran system
    # itemName = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = SaleConversationItems

    depth = 1
