from mongoengine import IntField
from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer, DynamicDocumentSerializer
from amspApp.FileServer.models import File, FileAtts, FileManagerItem, FileInAutomations


class FileSerializer(DynamicDocumentSerializer):
    class Meta:
        model = File
        fields = (
            "userID",
            "originalFileName",
            "decodedFileName",
            "dateOfPost",
            "downloadTimes",
            "uploaderIP",
            "extra",
        )
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)

class ImageSerializer(DynamicDocumentSerializer):
    class Meta:
        model = File
        fields = (
            "userID",
            "originalFileName",
            "decodedFileName",
            "dateOfPost",
            "downloadTimes",
        )
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)



class FileAttsSerializer(DynamicDocumentSerializer):
    class Meta:
        model = FileAtts
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)



class FileSummerySerializer(DynamicDocumentSerializer):
    size = serializers.IntegerField(source="uploaderIP.fileSize", read_only=True)
    class Meta:
        model = File
        fields = (
            "id",
            "originalFileName",
            "decodedFileName",
            "dateOfPost",
            "extra",
            "size"
        )
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)





class FileInAutomationsSerializer(DynamicDocumentSerializer):
    class Meta:
        model = FileInAutomations
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)



class FileManagerItemSerializer(DynamicDocumentSerializer):
    class Meta:
        model = FileManagerItem
    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)
