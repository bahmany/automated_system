
from rest_framework_mongoengine.serializers import DynamicDocumentSerializer

from amspApp.ControlProject.models import  CalSubProjects


class ControlProjectCalSubProjectsSerializer(DynamicDocumentSerializer):

    class Meta:
        model = CalSubProjects

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)



