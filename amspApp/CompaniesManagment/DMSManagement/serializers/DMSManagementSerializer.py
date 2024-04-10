import pickle
from bson import ObjectId
from datetime import datetime
from rest_framework_mongoengine.serializers import *
from amspApp.BPMSystem.models import LunchedProcess, LunchedProcessArchive, DoneProcessArchive
from amspApp.CompaniesManagment.DMSManagement.models import DMS
from amspApp.CompaniesManagment.DMSManagement.models import docModel
from amspApp.CompaniesManagment.DMSManagement.models import docRelated
from amspApp.CompaniesManagment.DMSManagement.models import docFormat
from amspApp.CompaniesManagment.DMSManagement.models import docType
from amspApp.CompaniesManagment.DMSManagement.models import docZone
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.Processes.models import Bpmn
from amspApp.CompaniesManagment.Processes.serializers.BpmnSerializer import BpmnSerializer
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class DMSManagementSerializer(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    docCode = serializers.CharField(required=False, allow_blank=True)
    docType = serializers.PrimaryKeyRelatedField(queryset=docType.objects.all(), write_only=True)
    docTypeRead = serializers.CharField(source='docType.id', read_only=True)
    docZone = serializers.PrimaryKeyRelatedField(queryset=docZone.objects.all(), write_only=True)
    docZoneRead = serializers.CharField(source='docZone.id', read_only=True)
    docModel = serializers.PrimaryKeyRelatedField(queryset=docModel.objects.all(), write_only=True)
    docModelRead = serializers.CharField(source='docModel.id', read_only=True)
    docFormat = serializers.PrimaryKeyRelatedField(queryset=docFormat.objects.all(), write_only=True)
    docFormatRead = serializers.CharField(source='docFormat.id', read_only=True)
    docRelated = serializers.PrimaryKeyRelatedField(queryset=docRelated.objects.all(), write_only=True)
    docRelatedRead = serializers.CharField(source='docRelated.id', read_only=True)

    class Meta:
        model = DMS
        fields = (
            'docType',
            'docZone',
            'docModel',
            'docFormat',
            'docRelated',
            'docTypeRead',
            'docZoneRead',
            'docModelRead',
            'docFormatRead',
            'docRelatedRead',
            'name',
            'docCode',
            'postDate',
            'allFiles',
            'visible')
        depth = 1

    def create(self, validated_data, **kwargs):
        posId = PositionsDocument.objects.get(userID=kwargs['request'].user.id,
                                              companyID=kwargs['request'].user.current_company.id)
        validated_data['position_id'] = posId.id
        validated_data['companyId'] = kwargs['request'].user.current_company.id
        if DMS.objects.filter(companyId=validated_data["companyId"],
                              name=validated_data['name']).count() > 0:
            raise serializers.ValidationError({"name": ["name must be unique"]})
        flg = 1
        for itm in validated_data['allFiles']:
            if itm['isCurr'] and flg:
                validated_data['currentFile'] = itm['dir']
                itm['isCurr'] = True
                validated_data['latestPostDate'] = itm['date']
                flg = 0
            else:
                itm['isCurr'] = False
        if flg and len(validated_data['allFiles']) != 0:
            validated_data['currentFile'] = validated_data['allFiles'][0]['dir']
            validated_data['allFiles'][0]['isCurr'] = True
            validated_data['latestPostDate'] = validated_data['allFiles'][0]['date']

        super(DMSManagementSerializer, self).create(validated_data)
        return {}

    def update(self, instance, validated_data):

        validated_data['position_id'] = instance.position_id

        validated_data['companyId'] = instance.companyId
        checkquey = DMS.objects.filter(companyId=validated_data["companyId"],
                                       name=validated_data['name'])
        if checkquey.count() >= 1:
            if checkquey.count() == 1:
                if checkquey[0].name == validated_data['name']:
                    if validated_data['id'] != checkquey[0].id:
                        raise serializers.ValidationError({"name": ["name must be unique"]})
            else:
                raise serializers.ValidationError({"name": ["name must be unique"]})
        del validated_data['id']
        flg = 1
        for itm in validated_data['allFiles']:
            if itm['isCurr'] and flg:
                validated_data['currentFile'] = itm['dir']
                itm['isCurr'] = True
                validated_data['latestPostDate'] = itm['date']
                flg = 0
            else:
                itm['isCurr'] = False
        if flg and len(validated_data['allFiles']) != 0:
            validated_data['currentFile'] = validated_data['allFiles'][0]['dir']
            validated_data['allFiles'][0]['isCurr'] = True
            validated_data['latestPostDate'] = validated_data['allFiles'][0]['date']

        return super(DMSManagementSerializer, self).update(instance, validated_data)


class InboxDMSManagementSerializer(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    # name = serializers.CharField(source='name', read_only=True)
    # docCode = serializers.CharField(source='docType.name', read_only=True)
    id = serializers.CharField(read_only=True)
    docType = serializers.CharField(source='docType.name', read_only=True)
    docZone = serializers.CharField(source='docZone.name', read_only=True)
    docFormat = serializers.CharField(source='docFormat.name', read_only=True)
    docRelated = serializers.CharField(source='docRelated.name', read_only=True)
    docModel = serializers.CharField(source='docModel.name', read_only=True)
    allFiles = serializers.ListField(read_only=True)
    # currentFile = serializers.CharField(source='docType.name', read_only=True)
    # postDate = serializers.CharField(source='docType.name', read_only=True)
    latestPostDate = serializers.DateTimeField(read_only=True)
    visible = serializers.IntegerField(read_only=True)

    class Meta:
        model = DMS
        fields = (
            'id',
            'name',
            'docCode',
            'docType',
            'docZone',
            'docFormat',
            'docRelated',
            'docModel',
            'allFiles',
            'currentFile',
            'postDate',
            'latestPostDate',
            'visible')
        depth = 2

    def create(self, validated_data, **kwargs):
        return 0


class InboxUserDMSSerializer(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    # name = serializers.CharField(source='name', read_only=True)
    # docCode = serializers.CharField(source='docType.name', read_only=True)
    docType = serializers.CharField(source='docType.name', read_only=True)
    docZone = serializers.CharField(source='docZone.name', read_only=True)
    docFormat = serializers.CharField(source='docFormat.name', read_only=True)
    docRelated = serializers.CharField(source='docRelated.name', read_only=True)
    docModel = serializers.CharField(source='docModel.name', read_only=True)
    # currentFile = serializers.CharField(source='docType.name', read_only=True)
    # postDate = serializers.CharField(source='docType.name', read_only=True)
    latestPostDate = serializers.DateTimeField(read_only=True)

    class Meta:
        model = DMS
        fields = (
            'name',
            'docCode',
            'docType',
            'docZone',
            'docFormat',
            'docRelated',
            'docModel',
            'currentFile',
            'postDate',
            'latestPostDate')
        depth = 2

    def create(self, validated_data, **kwargs):
        return 0



