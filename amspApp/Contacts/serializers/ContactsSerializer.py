from rest_framework_mongoengine.serializers import DynamicDocumentSerializer
from amspApp.Contacts.models import Contacts, ContactsGroups, ContactsGroupItems

__author__ = 'mohammad'


class ContactsSerializer(DynamicDocumentSerializer):
    class Meta:
        model = Contacts

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class ContactsGroupsSerializer(DynamicDocumentSerializer):
    class Meta:
        model = ContactsGroups

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


class ContactsGroupItemsSerializer(DynamicDocumentSerializer):
    class Meta:
        model = ContactsGroupItems
        depth = 1

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)
