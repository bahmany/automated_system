import json

from amspApp.BI.airflowconnector import AirflowConnector
from amspApp.BI.models import BIDatasource
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class BIDatasourceSerializers(DynamicFieldsDocumentSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = BIDatasource

    def save(self, **kwargs):
        res = AirflowConnector().get_one('connections', self.data['airflow_connection_id'])
        if res.reason == 'NOT FOUND':
            del self.data['details']['datasourceTitle']
            del self.data['details']['positionID']
            AirflowConnector().add_one('connections', self.data['details'])

        result = super(BIDatasourceSerializers, self).save(**kwargs)

        return result
