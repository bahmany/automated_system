import pickle

from rest_framework_mongoengine.serializers import *

from amspApp.Bpms.BpmEngine import BpmEngine
from amspApp.Bpms.models import LunchedProcess
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.Processes.models import Bpmn
from amspApp.CompaniesManagment.Processes.serializers.BpmnSerializer import BpmnSerializer
from amspApp.FileServer.views.BpmsFileView import BpmsFileViewSet
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class LunchedProcessSerializer(DynamicFieldsDocumentSerializer):
    bpmnForCreate = serializers.CharField(label="bpmn",
                                 style={'template': 'forms/base-templates/selectAngular.html',
                                        'cssclass': 'col-md-12', 'ngmodel': 'lunchedProcess.bpmnForCreate',
                                        'ngoptions': 'obj.id as obj.name for obj in bpmns'},write_only=True)

    name = serializers.CharField(label="name", style={'template': 'forms/base-templates/input.html',
                                                      'cssclass': 'col-md-12',
                                                      'ngmodel': 'lunchedProcess.name'})
    bpmnName = serializers.CharField(source='bpmn.name', read_only=True)
    bpmnId = serializers.CharField(source='bpmn.id', read_only=True)


    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = LunchedProcess
        # fields = (
        #     'id', 'user_id', 'bpmnForCreate','bpmn','bpmnName','bpmnId','thisStep', 'thisPerformer','pastSteps', 'thisStatus', 'name',
        #     'formData')
        depth = 1

    def create(self, validated_data, **kwargs):
        validated_data['user_id'] = int(kwargs['request'].user.pk)
        validated_data['bpmn'] = BpmnSerializer(Bpmn.objects.get(id=validated_data['bpmnForCreate'])).data
        current_pos=PositionsDocument.objects.get(userID=kwargs['request'].user.id,
                                                                      companyID=kwargs[
                                                                          'request'].user.current_company.id)
        validated_data['position_id'] = current_pos.id
        validated_data['positionName'] = current_pos.profileName
        new = LunchedProcess.objects.create(**validated_data)
        engineInstance = BpmEngine(new.bpmn['xml'], new.bpmn['form'], new.bpmn['userTasks'], new.pk)
        enginefileClass = BpmsFileViewSet()
        enginefileClass = enginefileClass.createEngineTempFile(pickle.dumps(engineInstance))
        new.engineInstance = enginefileClass
        new.save()
        engineInstance.run()

        return new
