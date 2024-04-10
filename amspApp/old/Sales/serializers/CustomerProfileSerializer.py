from asq.initiators import query
from rest_framework import serializers

from amspApp.Sales.models import TaminProject, SalesCustomerProfile, SalesCustomerProfileSalesRequestsSizes, \
    HamkaranSalesCustomerProfile, HamkaranCustomerAddress, HamkaranCustomerNotes
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class CustomerProfileSerializer(DynamicFieldsDocumentSerializer):
    desc = serializers.CharField(label="desc", required=False, allow_null=True)
    hamkaranCode = serializers.CharField(required=False, allow_null=True)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = SalesCustomerProfile

    depth = 1


class CustomerProfileSalesRequestsSizesSerializer(DynamicFieldsDocumentSerializer):
    desc = serializers.DictField(label="desc", required=False, allow_null=True)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = SalesCustomerProfileSalesRequestsSizes

    depth = 1


class HamkaranSalesCustomerProfileSerializer(DynamicFieldsDocumentSerializer):
    CustomerID = serializers.CharField(required=False, allow_null=True)
    exp = serializers.DictField(label="exp", required=False, allow_null=True)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = HamkaranSalesCustomerProfile

    depth = 1


class HamkaranCustomerAddressSerializer(DynamicFieldsDocumentSerializer):
    CustomerAddressID = serializers.IntegerField(required=False, allow_null=True)
    exp = serializers.DictField(label="exp", required=False, allow_null=True)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = HamkaranCustomerAddress

    depth = 1



class HamkaranCustomerNotesSerializer(DynamicFieldsDocumentSerializer):

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = HamkaranCustomerNotes

    def get_phones(self, CounterpartDLCode):
        phones = []
        hpf = HamkaranSalesCustomerProfile.objects.filter(exp__PartyRef = CounterpartDLCode).first()
        if hpf == None:
            return phones
        notes = HamkaranCustomerNotes.objects.filter(EntityRef=int(hpf.exp['CustomerID'])).first()
        if notes:
            note = notes.Notes
            phones = ["09" + x[:9] if x!= '' else None for x in note.split("09")]
            phones = query(phones).where(lambda x:x!=None).distinct().to_list()
        return phones

