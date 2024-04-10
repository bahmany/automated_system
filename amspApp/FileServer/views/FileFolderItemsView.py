from rest_framework.response import Response
from rest_framework_mongoengine import viewsets
from amspApp.FileServer.models import File, FileFolderItems, FileFolders
from amspApp.FileServer.serializers.FileFolderItemSerializer import FileFolderItemsSerializers
from amspApp.FileServer.serializers.FileSerializer import  FileSummerySerializer
from amspApp._Share.ListPagination import ListPagination


class FileFolderItemsViewset(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = FileFolderItemsSerializers
    queryset = FileFolderItems.objects.all()
    pagination_class = ListPagination



    # def get_queryset(self):
    #     self.queryset = FileFolderItems.objects.filter(
    #         userID=self.request.user.id
    #     )
    #     return super(FileFolderItemsViewset, self).get_queryset()

    def create(self, request, *args, **kwargs):
        folderInstance = FileFolders.objects.get(
            id=kwargs['folder_id'],
            userID=request.user.id)
        fileInstance = File.objects.get(
            decodedFileName=request.data['imgLink'].split("_")[len(request.data['imgLink'].split("_")) - 1],
            userID=request.user.id)
        request.data["fileID"] = str(fileInstance.id)
        request.data["folder"] = str(folderInstance.id)
        request.data["privacy"] = 1
        request.data["companies"] = []
        request.data["file"] = FileSummerySerializer(instance=fileInstance).data
        request.data["file"]["decodedFileName"] = "/api/v1/file/upload?q=thmum50_"+request.data["file"]["decodedFileName"]
        request.data.pop("imgInf", None)
        request.data.pop("imgLink", None)
        return super(FileFolderItemsViewset, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        folderInstance = FileFolders.objects.get(
            id=kwargs['folder_id'],
            userID=request.user.id)
        fileItemInstance = self.queryset.get(
            id= kwargs['id'],
            folder=folderInstance)
        fileItemInstance.file['originalFileName'] = request.data['file.originalFileName']
        fileItemInstance.save()
        return Response({})

    def list(self, request, *args, **kwargs):
        folderInstance = FileFolders.objects.get(
            id=kwargs['folder_id'],
            userID=request.user.id)
        self.queryset = self.queryset.filter(
            folder = folderInstance
        )
        return super(FileFolderItemsViewset, self).list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        folderInstance = FileFolders.objects.get(
            id=kwargs['folder_id'],
            userID=request.user.id)
        FileFolderItemsSerializers().minToCounter(folderInstance)
        return super(FileFolderItemsViewset, self).destroy(request, *args, **kwargs)




    def GetItems(self, request, *args, **kwargs):
        self.get_queryset()
        # in the following lines we can check if logined user is owner of the file or not
        folderInstance = self.queryset.get(
            id=kwargs['id'],
            userID=request.user.id)
        filesItemsQueryset = self.filter_queryset(FileFolderItems.objects.filter(
            folder=str(folderInstance.id)
        ))
        # --------------------------------------------------------------------
        page = self.paginate_queryset(filesItemsQueryset)
        if page is not None:
            serializer = FileFolderItemsSerializers(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = FileFolderItemsSerializers(filesItemsQueryset, many=True)
        return Response(serializer.data)


