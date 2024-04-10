import pickle
from bson import ObjectId
from rest_framework_mongoengine.serializers import *
from amspApp.BPMSystem.models import LunchedProcess, LunchedProcessArchive, DoneProcessArchive
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.Processes.models import Bpmn
from amspApp.CompaniesManagment.Processes.serializers.BpmnSerializer import BpmnSerializer
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class DPAShowDataSerializer(DynamicFieldsDocumentSerializer):
    formData = serializers.SerializerMethodField('get_form_data',read_only=True)
    stepName = serializers.SerializerMethodField('get_step_name',read_only=True)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = DoneProcessArchive
        fields = (
            'formData', 'stepName')
        depth = 1

    def create(self, validated_data, **kwargs):
        return 0
    def get_form_data(self, obj):
        result = {}
        currentPosition = self.currentPositionObj
        if 'formData' in obj:
            pass
    def get_step_name(self, obj):
        result = {}
        currentPosition = self.currentPositionObj
        if 'formData' in obj:
            pass