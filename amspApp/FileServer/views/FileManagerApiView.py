from mimetypes import MimeTypes

from django.http import HttpResponse
from rest_framework import views
from rest_framework.response import Response

from amsp import settings
from amspApp.FileServer.views.fileManagerBridge import FileManager


class FileManagerApiView(views.APIView):
    def get(self, request, *args, **kwargs):
        fileManager = FileManager(request.user.id)

        preview = request.query_params["preview"] if "preview" in request.query_params else "false"

        if request.query_params["preview"] != "true":
            response = fileManager.download(request.query_params['path'])
            mimetype = MimeTypes()
            response = HttpResponse(
                response,
                content_type=mimetype.guess_type(request.query_params['path'])[0])
            response["Content-Disposition"] = 'attachment; filename="%s"' % request.query_params['path'].split("/")[
                len(request.query_params['path'].split("/")) - 1]
            return response
        if request.query_params["preview"] == "true":
            response = fileManager.getContent(request.query_params['path'])
            mimetype = MimeTypes()
            response = HttpResponse(
                response,
                content_type=mimetype.guess_type(request.query_params['path'])[0])
            response["Content-Disposition"] = 'attachment; filename="%s"' % request.query_params['path'].split("/")[
                len(request.query_params['path'].split("/")) - 1]
            return response

    def post(self, request, *args, **kwargs):
        fileManager = FileManager(request.user.id)
        if "params" in request.data:
            if request.data["params"]["mode"] == "list":
                return Response(fileManager.list(request.data["params"]))
            if request.data["params"]["mode"] == "rename":
                return Response(fileManager.rename(request.data["params"]))
            if request.data["params"]["mode"] == "copy":
                return Response(fileManager.copy(request.data["params"]))
            if request.data["params"]["mode"] == "delete":
                return Response(fileManager.remove(request.data["params"]))
            if request.data["params"]["mode"] == "edit":
                return Response(fileManager.edit(request.data["params"]))
            if request.data["params"]["mode"] == "getContent":
                return Response(fileManager.getContent(request.data["params"]))
            if request.data["params"]["mode"] == "addfolder":
                return Response(fileManager.createFolder(request.data["params"]))
            if request.data["params"]["mode"] == "changePermissions":
                return Response(fileManager.changePermissions(request.data["params"]))
            if request.data["params"]["mode"] == "compress":
                return Response(fileManager.compress(request.data["params"]))
            if request.data["params"]["mode"] == "extract":
                return Response(fileManager.extract(request.data["params"]))
            if request.data["params"]["mode"] == "download":
                return Response(fileManager.download(request.data["params"]))
        if "destination" in request.data:
            return Response(fileManager.upload(request))
        if "shareUsersID" in request.data:
            return Response(self.Share(request))
        if "requestedShareFolder" in request.data:
            return Response(self.RequestedShareFolder(request))

    def Share(self, request):
        fileManager = FileManager(request.user.id)
        getItemName = fileManager.shareItem(request)
        return getItemName

    def RequestedShareFolder(self, request):
        fileManager = FileManager(request.user.id)
        getItemName = fileManager.RequestedShareFolder(request)
        return getItemName
