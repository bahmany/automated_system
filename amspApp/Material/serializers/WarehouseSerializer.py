# from amspApp.Material.models import OdooWarehouses, OdooBarcodes
from rest_framework import serializers

from amspApp.Material.models import MaterialLocations, Barcodes, MaterialHamkaranTafzil, MaterialConvSale, \
    MaterialTolidOrder, MaterialTolidOrderItems
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class MaterialLocationsSerializer(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = MaterialLocations


class MaterialHamkaranTafzilSerializer(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = MaterialHamkaranTafzil


class BarcodesSerializer(DynamicFieldsDocumentSerializer):
    confirmTime = serializers.DateTimeField(allow_null=True, required=False)
    confirmLocation = serializers.BooleanField(default=False)
    confirmPositionID = serializers.IntegerField(allow_null=True, required=False)
    hamkaranSanad = serializers.IntegerField(allow_null=True, required=False)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = Barcodes


# class BarcodesSerializerForBarnameh(serializers.Serializer):
#     barcode = serializers.CharField(max_length=40)
#     locationLink = serializers.RelatedField(queryset=MaterialLocations.objects.all(), read_only=True )
#     locationLink = serializers.CharField(max_length=40)
#     x = serializers.IntegerField()
#     y = serializers.IntegerField()
#     z = serializers.IntegerField()
#     partcode = serializers.CharField(max_length=40)
#     noe = serializers.CharField(max_length=4)
#     keifiat = serializers.CharField(max_length=4)
#     temper = serializers.CharField(max_length=4)
#     sath = serializers.CharField(max_length=4)
#     zekhamat = serializers.CharField(max_length=4)
#     arz = serializers.CharField(max_length=4)
#     darajeh = serializers.CharField(max_length=4)
#     tool = serializers.CharField(max_length=4)
#     vazneKhales = serializers.IntegerField()
#     location = serializers.CharField(max_length=12)
#     dateOfPost = serializers.DateTimeField()
#     hoursInAnbar = serializers.IntegerField()
#
#     def _include_additional_options(self, *args, **kwargs):
#         return self.get_extra_kwargs()
#
#     def _get_default_field_names(self, *args, **kwargs):
#         return self.get_field_names(*args, **kwargs)
#
#     class Meta:
#         model = Barcodes
#         fields = (
#             'barcode',
#             'locationLink',
#             'x',
#             'y',
#             'z',
#             'partcode',
#             'noe',
#             'keifiat',
#             'temper',
#             'sath',
#             'zekhamat',
#             'arz',
#             'darajeh',
#             'tool',
#             'vazneKhales',
#             'location',
#             'dateOfPost',
#             'hoursInAnbar',
#         )


class MaterialConvSaleSerializer(DynamicFieldsDocumentSerializer):

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = MaterialConvSale


class MaterialTolidOrderSerializer(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = MaterialTolidOrder


class MaterialTolidIOrdertemsSerializer(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = MaterialTolidOrderItems

    def create(self, validated_data):
        result = super(MaterialTolidIOrdertemsSerializer, self).create(validated_data)

        return result

