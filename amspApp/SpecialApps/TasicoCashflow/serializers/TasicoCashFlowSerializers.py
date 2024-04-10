from rest_framework import serializers

from amspApp.SpecialApps.****Cashflow.models import CashFlow****TaminCompany, CashFlow****TaminDetail, \
    CashFlow****TaminProject, CashFlow****TaminIncommings, CashFlow****TaminPayments, \
    CashFlow****TaminAllDateTmp
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class CashFlow****TaminCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlow****TaminCompany


class CashFlow****TaminDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlow****TaminDetail


class CashFlow****TaminProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlow****TaminProject
        depth = 2


class CashFlow****TaminCashFlow****TaminIncommingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlow****TaminIncommings


class CashFlow****TaminPaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashFlow****TaminPayments


class CashFlow****TaminAllDateTmpSerializer(DynamicFieldsDocumentSerializer):



    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = CashFlow****TaminAllDateTmp