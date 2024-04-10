from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer
from amspApp.Administrator.Billings.models import Billing_Strategies, Billing_Payments
from amspApp._Share.DynamicFieldModelSerializer import DynamicFieldsModelSerializer


class BillingSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Billing_Strategies


class PaymentSerializer(ModelSerializer):
    # billingStrategyLink = serializers.RelatedField(queryset=Billing_Strategies.objects.all())

    class Meta:
        model = Billing_Payments
        # fields = (
        #     'createdUserID',
        #     'dateOfPost',
        #     'billingStrategyLink',
        #     'customerLink',
        #     'loadedPrice',
        #     'bankID',
        #     'paymentType',
        #     'totalPrice',
        #     'exp',
        #     'Title'
        # )
        depth = 0



