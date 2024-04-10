import uuid

from rest_framework_mongoengine.serializers import DocumentSerializer

from amspApp.BI.DataTables.models import DataTable


class DataTableSerializer(DocumentSerializer):


    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


    class Meta:
        model = DataTable

    def create(self, validated_data):
        for l in validated_data.get("fields").get("list"):
            if not l.get("uid"):
                l["uid"] = uuid.uuid4().hex
        return super(DataTableSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        for l in validated_data.get("fields").get("list"):
            if not l.get("uid"):
                l["uid"] = uuid.uuid4().hex
        return super(DataTableSerializer, self).update(instance, validated_data)


