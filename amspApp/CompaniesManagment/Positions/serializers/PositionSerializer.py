from rest_framework import serializers
from amspApp.CompaniesManagment.Positions.models import Position,PositionsDocument, PositionSentHistory
from amspApp._Share.DynamicFieldModelSerializer import DynamicFieldsModelSerializer
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer
from amspApp.amspUser.models import MyUser


class PositionSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Position
        fields = ("id", "company", "chart", "user", "post_date")
        depth = 1



class PositionDocumentSerializer(DynamicFieldsDocumentSerializer):
    last = serializers.ListField(allow_null=True)
    postDate = serializers.DateTimeField(allow_null=True)
    chartID = serializers.IntegerField(allow_null=True)
    userID = serializers.IntegerField(allow_null=True)
    companyID = serializers.IntegerField(allow_null=True)
    chartName = serializers.CharField(allow_null=True)
    profileName = serializers.CharField(allow_null=True)
    companyName = serializers.CharField(allow_null=True)
    profileID = serializers.CharField(allow_null=True)
    avatar = serializers.CharField(allow_null=True)
    # postDate = serializers.DateTimeField(allow_null=True)
    defaultSec = serializers.IntegerField(allow_null=True)
    # last = serializers.ListField(allow_null=True)
    positionID = serializers.IntegerField(allow_null=True)
    hasBulkSentPermission = serializers.IntegerField(allow_null=True)
    isPositionAllowedToSendDirectly = serializers.IntegerField(allow_null=True)
    isPositionIgonreAssistantHardSent = serializers.IntegerField(allow_null=True)
    desc = serializers.DictField(allow_null=True)

    class Meta:
        model = PositionsDocument
        depth = 1



    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

# class PositionDocumentSerializerForEmzaList(PositionDocumentSerializer):
#     def to_representation(self, instance):

class PositionDocumentLessDataSerializer(DynamicFieldsDocumentSerializer):
    last = serializers.ListField(allow_null=True)
    postDate = serializers.DateTimeField(allow_null=True)
    chartID = serializers.IntegerField(allow_null=True)
    userID = serializers.IntegerField(allow_null=True)
    companyID = serializers.IntegerField(allow_null=True)
    chartName = serializers.CharField(allow_null=True)
    profileName = serializers.CharField(allow_null=True)
    companyName = serializers.CharField(allow_null=True)
    profileID = serializers.CharField(allow_null=True)
    avatar = serializers.CharField(allow_null=True)
    # postDate = serializers.DateTimeField(allow_null=True)
    defaultSec = serializers.IntegerField(allow_null=True)
    # last = serializers.ListField(allow_null=True)
    positionID = serializers.IntegerField(allow_null=True)
    hasBulkSentPermission = serializers.IntegerField(allow_null=True)
    isPositionAllowedToSendDirectly = serializers.IntegerField(allow_null=True)
    isPositionIgonreAssistantHardSent = serializers.IntegerField(allow_null=True)
    desc = serializers.DictField(allow_null=True)

    class Meta:
        model = PositionsDocument
        depth = 1
        fields = ('chartID','userID','chartName','profileName','avatar','positionID',)

    def to_representation(self, instance):
        result = super(PositionDocumentLessDataSerializer, self).to_representation(instance)
        userinstance = MyUser.objects.get(id = result['userID'])
        result['personnel_code'] = userinstance.personnel_code
        return result



    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

class PrositionSerializerJustUsername(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ("id", "user")
        depth = 0




class PositionSentHistorySerializer(DynamicFieldsDocumentSerializer):
    class Meta:
        model = PositionSentHistory
        depth = 1

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)
