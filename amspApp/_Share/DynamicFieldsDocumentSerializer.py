from rest_framework_mongoengine.serializers import DocumentSerializer


class DynamicFieldsDocumentSerializer(DocumentSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)
        requestObj = kwargs.pop('request', None)
        currentPositionObj = kwargs.pop('currentPositionObj', None)
        dataFields = kwargs.pop('dataFields', None)
        self.requestObj = requestObj
        self.currentPositionObj = currentPositionObj
        self.dataFields = dataFields
        # Instantiate the superclass normally
        super(DynamicFieldsDocumentSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
