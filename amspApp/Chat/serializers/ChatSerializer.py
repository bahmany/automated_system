from rest_framework import serializers
from rest_framework_mongoengine import serializers as _serializers
from amspApp.Chat.models import Chat
from amspApp._Share.DynamicFieldsDocumentSerializer import DynamicFieldsDocumentSerializer


class ChatSerializer(DynamicFieldsDocumentSerializer):
    dest_positionID = serializers.IntegerField(required=False, allow_null=True, )  # if chatType = 1
    dest_groupID = _serializers.ObjectIdField(required=False, allow_null=True, )  # if chatType = 2
    dest_pageID = _serializers.ObjectIdField(required=False, allow_null=True, )  # if chatType = 3
    dateOfSeen = serializers.DateTimeField(required=False, allow_null=True, )
    desc = serializers.CharField(label="desc", required=False, allow_null=True)

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = Chat

class ChatListSingleSerializer(ChatSerializer):
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

    class Meta:
        model = Chat
        exclude = ('dest_groupID','dest_pageID','is_deleted', 'companyID' )
