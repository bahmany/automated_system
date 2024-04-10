from rest_framework_mongoengine.serializers import DynamicDocumentSerializer
from amspApp.FileServer.models import FileFolderItems


class FileFolderItemsSerializers(DynamicDocumentSerializer):
    class Meta:
        model = FileFolderItems

    def _include_additional_options(self, *args, **kwargs):
        return self.get_extra_kwargs()

    def _get_default_field_names(self, *args, **kwargs):
        return self.get_field_names(*args, **kwargs)


    def create(self, validated_data):
        self.addToCounter(validated_data["folder"], None)
        return super(FileFolderItemsSerializers, self).create(validated_data)

    def update(self, instance, validated_data):
        self.addToCounter(validated_data["folder"], instance.folder)
        return super(FileFolderItemsSerializers, self).update(instance, validated_data)

    def addToCounter(self, newFolderInstance, prevFileFolderInstance):
        newFolderInstance.count = newFolderInstance.count + 1
        newFolderInstance.save()
        if prevFileFolderInstance != None:
            prevFileFolderInstance.count = prevFileFolderInstance.count - 1
            prevFileFolderInstance.save()
    def minToCounter(self, folderInstance):
        folderInstance.count = folderInstance.count - 1
        folderInstance.save()
