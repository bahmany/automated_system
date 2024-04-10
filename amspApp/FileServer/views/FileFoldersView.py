from asq.initiators import query
from bson import ObjectId
from rest_framework import serializers
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets
from amspApp.FileServer.models import FileFolders, FileFolderItems
from amspApp.FileServer.serializers.FileFolderItemSerializer import FileFolderItemsSerializers


class FileFoldersViewset(viewsets.ModelViewSet):
    from amspApp.FileServer.serializers.FileFolderSerializer import FileFoldersSerializers
    lookup_field = "id"
    serializer_class = FileFoldersSerializers

    def get_queryset(self):
        self.queryset = FileFolders.objects.filter(userID=self.request.user.id).order_by("name").limit(100)
        return super(FileFoldersViewset, self).get_queryset()

    def list(self, request, *args, **kwargs):
        result = super(FileFoldersViewset, self).list(request, *args, **kwargs)
        return result

    def destroy(self, request, *args, **kwargs):
        self.get_queryset()
        return super(FileFoldersViewset, self).destroy(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request.data["userID"] = request.user.id
        return super(FileFoldersViewset, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.get_queryset()
        """
        -------------------------------------------------------------------------------------------
        -------------------------------------------------------------------------------------------
        -------------------------------------------------------------------------------------------
        -------------------------------------------------------------------------------------------
        here is a problem
        when a user change a parent to its child every thing bread
                raise serializers.ValidationError(
                    {"status": "Bad request", "message": [{"name": "Recursion Error", "message": "Same parent"}]})
        """
        beforeUpdateInstance = self.queryset.get(id=request.data["id"])

        def checkRecursiveBreak(obj, newParentID):
            if rootToCheck == str(obj.id):
                raise serializers.ValidationError(
                    {"status": "Bad request", "message": [{"name": "Recursion Error", "message": "Same parent"}]})
            else:
                folders = self.queryset.filter(parentFolder=str(obj.id))
                for f in folders:
                    checkRecursiveBreak(f, newParentID)

        rootToCheck = request.data["parentFolder"]
        checkRecursiveBreak(beforeUpdateInstance, rootToCheck)
        """
        -------------------------------------------------------------------------------------------
        -------------------------------------------------------------------------------------------
        -------------------------------------------------------------------------------------------
        -------------------------------------------------------------------------------------------
        """

        request.data.pop("children", None)
        request.data.pop("count", None)
        request.data.pop("id", None)
        if "parentFolder" in request.data:
            if request.data["parentFolder"] == None:
                request.data.pop("parentFolder", None)

        request.data["userID"] = request.user.id
        return super(FileFoldersViewset, self).update(request, *args, **kwargs)

    @list_route(methods=["get"])
    def getRecursive(self, request, *args, **kwargs):

        def generateRec(folder, _foldersList):
            newRes = []
            fres = []
            newRes = query(_foldersList).select(lambda x: x).where(
                lambda x: str(x["parentFolder"]) == str(folder.id)).to_list()
            for nR in newRes:
                fres.append({
                    "id": str(nR.id),
                    "name": nR.name,
                    "parentFolder": str(nR.parentFolder),
                    "privacy": nR.privacy,
                    "count": nR.count,
                    "dateOfCreate": nR.dateOfCreate,
                    "children": generateRec(nR, _foldersList)
                })
            return fres


        self.get_queryset()
        foldersList = list(self.queryset)
        result = []

        justTopFolders = query(foldersList).select(lambda x: x).where(
            lambda x: x["parentFolder"] == None).to_list()
        for jTF in justTopFolders:
            cc = {
                "id": str(jTF.id),
                "name": jTF.name,
                "parentFolder": jTF.parentFolder,
                "privacy": jTF.privacy,
                "count": jTF.count,
                "dateOfCreate": jTF.dateOfCreate,
                "children": generateRec(jTF, foldersList),
            }
            result.append(cc)
        return Response(result)

    @list_route(methods=["post"])
    def UpdateFileToFolder(self,request, *args, **kwargs):
        self.get_queryset()
        folderInstance = self.queryset.get(
            id = request.data['folderID'],
            userID = request.user.id
        )
        fileItemInstance =  FileFolderItems.objects.get(
            id = request.data["fileID"]
        )

        newFolderID = {
            "folder" : folderInstance.id,
        }

        ser = FileFolderItemsSerializers(data=newFolderID, instance=fileItemInstance, partial=True)
        ser.is_valid(raise_exception=True)
        ser.update(fileItemInstance, ser.validated_data)

        return Response({})















