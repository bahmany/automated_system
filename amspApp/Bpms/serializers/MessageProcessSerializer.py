from rest_framework_mongoengine.serializers import *

from amspApp.Bpms.models import LunchedProcessMessages
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class MessageProcessSerializer(DynamicFieldsDocumentSerializer):
    # bpmnForCreate = serializers.CharField(label="bpmn",
    #                              style={'template': 'forms/base-templates/selectAngular.html',
    #                                     'cssclass': 'col-md-12', 'ngmodel': 'lunchedProcess.bpmnForCreate',
    #                                     'ngoptions': 'obj.id as obj.name for obj in bpmns'},write_only=True)
    #
    # name = serializers.CharField(label="name", style={'template': 'forms/base-templates/input.html',
    #                                                   'cssclass': 'col-md-12',
    #                                                   'ngmodel': 'lunchedProcess.name'})
    bpmnName = serializers.CharField(source='bpmn.name', read_only=True)
    bpmnId = serializers.CharField(source='bpmn.id', read_only=True)


    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = LunchedProcessMessages
        # fields = (
        #     'id', 'user_id', 'bpmnForCreate','bpmn','bpmnName','bpmnId','thisStep', 'thisPerformer','pastSteps', 'thisStatus', 'name',
        #     'formData')
        depth = 1
