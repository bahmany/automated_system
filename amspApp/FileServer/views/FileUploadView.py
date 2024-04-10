import os
import shutil
import tempfile
import uuid
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache import never_cache
from rest_framework import status
from rest_framework import views
from rest_framework import viewsets
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from wand.image import Image as _img

from amsp.settings import FILE_PATH, STATIC_ROOT
from amspApp.CompaniesManagment.Positions.models import Position
from amspApp.FileServer.models import File, FileAtts
from amspApp.FileServer.serializers.FileSerializer import FileAttsSerializer, FileSerializer
from amspApp._Share.CharacterHandle import ShowUtfCharacterCode
from amspApp._Share.GetMime import GetMimeType


class FileUploaderTemplate(views.APIView):
    def get(self, request, *args, **kwargs):
        return render_to_response(
            "share/filecloud/FilesCloud.html",
            {}, context_instance=RequestContext(request))


class FileManagerTemplate(views.APIView):
    def get(self, request, *args, **kwargs):
        return render_to_response(
            "share/fileManager/fileManager.html",
            {}, context_instance=RequestContext(request))


class FileUploadViewSet(views.APIView):
    parser_classes = (FileUploadParser,)

    # fileFolder = "/var/www/amspfiles/"
    # appFolder = "/var/www/amsPlus/"

    def generateGuidName(self):
        return uuid.uuid4().hex + uuid.uuid4().hex

    def loadFile(self, request, *args, **kwargs):
        pass

    def returnNoPrev(self):
        f = "noPrev_notFound.jpg"
        static_root = STATIC_ROOT
        finalRoot = os.path.abspath(
            os.path.join(os.path.abspath(static_root), "images/noPrev_notFound.jpg", ))
        fsock = open(finalRoot, "rb")
        mime = GetMimeType("." + f.split(".")[len(f.split(".")) - 1])
        response = HttpResponse(fsock, content_type=mime)
        response['Content-Disposition'] = 'attachment; filename=%s' % (f)
        return response

    def getFolderName(self, dateOfPost, fileEncodedName):
        folderName = os.path.join(dateOfPost.strftime("%Y_%m_%d"), dateOfPost.strftime("%H"))
        destFolder = os.path.join(FILE_PATH, "userUploads", folderName)

        if not os.path.isdir(destFolder):
            path = Path(destFolder)
            path.mkdir(parents=True)

        fullPath = os.path.abspath(os.path.join(destFolder, fileEncodedName))

        return fullPath

    def getPath(self, decodedFilename):
        if decodedFilename == "undefined":
            return None
        fileInstance = File.objects.get(decodedFileName=decodedFilename)
        f = fileInstance.originalFileName
        folderName = os.path.join(fileInstance.dateOfPost.strftime("%Y_%m_%d"),
                                  fileInstance.dateOfPost.strftime("%H"))
        destFolder = os.path.join(FILE_PATH, "userUploads", folderName)
        fullPath = os.path.abspath(os.path.join(destFolder, decodedFilename))
        return fullPath

    @never_cache
    def get(self, request, format=None):
        fileEncoded = request.query_params.get("q", None)

        # try:
        fileToDownload = File.objects.filter(decodedFileName=fileEncoded)

        if (fileEncoded == None):
            fileSerial = FileSerializer(instance=fileToDownload.first()).data
            return Response(fileSerial)

        if fileToDownload.count() == 0:
            return self.returnNoPrev()

        fileToDownload = fileToDownload[0]
        # fileToDownload = fileToDownload[0]
        # reading file into memory---
        views = {
            'userID': request.user.id,
            'dateOf': datetime.now()
        }

        f = fileToDownload.originalFileName
        folderName = os.path.join(fileToDownload.dateOfPost.strftime("%Y_%m_%d"),
                                  fileToDownload.dateOfPost.strftime("%H"))
        destFolder = os.path.join(FILE_PATH, "userUploads", folderName)
        fullPath = os.path.abspath(os.path.join(destFolder, fileEncoded))

        # if not os.path.isfile(fullPath):
        #     return self.returnNoPrev()

        if os.path.exists(fullPath):
            fsock = open(fullPath, "rb")
            mime = GetMimeType("." + f.split(".")[len(f.split(".")) - 1])
            response = HttpResponse(fsock, content_type=mime)
            response['Content-Disposition'] = 'attachment; filename=%s' % (f)
            return response
        else:
            # raise Exception(fullPath)
            return self.returnNoPrev()

            # ----------------------------

    def getImage(self, fileEncoded=""):
        fileToDownload = File.objects.filter(decodedFileName=fileEncoded).first()
        if fileToDownload == None:
            return self.returnNoPrev()
        f = fileToDownload.originalFileName
        folderName = os.path.join(fileToDownload.dateOfPost.strftime("%Y_%m_%d"),
                                  fileToDownload.dateOfPost.strftime("%H"))
        destFolder = os.path.join(FILE_PATH, "userUploads", folderName)
        fullPath = os.path.abspath(os.path.join(destFolder, fileEncoded))
        if os.path.exists(fullPath):
            fsock = open(fullPath, "rb")
            mime = GetMimeType("." + f.split(".")[len(f.split(".")) - 1])
            response = HttpResponse(fsock, content_type=mime)
            response['Content-Disposition'] = 'attachment; filename=%s' % (f)
            return response
        else:
            return self.returnNoPrev()

    def saveSignFile(self, creatorUserID):
        decodeName = self.generateGuidName()
        dateOfPost = datetime.now()

        folderName = os.path.join(dateOfPost.strftime("%Y_%m_%d"),
                                  dateOfPost.strftime("%H"))
        destFolder = os.path.join(FILE_PATH, "userUploads", folderName)
        filename = os.path.join(destFolder, decodeName)

        if not os.path.isdir(destFolder):
            path = Path(destFolder)
            path.mkdir(parents=True)

        newFile = {
            "userID": creatorUserID,
            "originalFileName": "GeneratedSign.png",
            "dateOfPost": dateOfPost,
            "decodedFileName": decodeName,
            "uploaderIP": {
                "fileSize": -1,
                "home": "",
                "browser": {},
                "ip": "127.0.0.1"
            }
        }
        newFile = File(**newFile)
        newFile.save()
        return {"name": decodeName, "fullPath": filename}

    def add_corners(self, im, rad):
        circle = Image.new('L', (rad * 2, rad * 2), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
        alpha = Image.new('L', im.size, 255)
        w, h = im.size
        alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        im.putalpha(alpha)
        return im

    def convert(self, filepdf):
        # used to generate temp file name. so we will not duplicate or replace anything
        uuid_set = str(uuid.uuid4().fields[-1])[:5]

        img = _img(filename=filepdf + "[0]", resolution=200)
        img.compression_quality = 80
        dir = tempfile.gettempdir()
        path = os.path.abspath(os.path.join(dir, "temp%s.jpg" % uuid_set))
        img.save(filename=path)
        return path

    def convertWithIndex(self, filepdf, pageIndex):
        # used to generate temp file name. so we will not duplicate or replace anything
        uuid_set = str(uuid.uuid4().fields[-1])[:5]
        img = _img(filename=filepdf + "[" + str(pageIndex) + "]", resolution=200)
        img.compression_quality = 80
        dir = tempfile.gettempdir()
        path = os.path.abspath(os.path.join(dir, "temp%s.jpg" % uuid_set))
        img.save(filename=path)
        return path

    def saveImgToDB(self, userID, documentName, tmppath, fileType=".jpg"):
        # ...
        # do some staff with uploaded file
        # ...

        decodeName = self.generateGuidName()
        dateOfPost = datetime.now()
        folderName = os.path.join(dateOfPost.strftime("%Y_%m_%d"), dateOfPost.strftime("%H"))
        destFolder = os.path.join(FILE_PATH, "userUploads", folderName)
        if not os.path.isdir(destFolder):
            path = Path(destFolder)
            path.mkdir(parents=True)

        destPath = os.path.join(destFolder, decodeName)
        shutil.copyfile(tmppath, destPath)
        os.remove(tmppath)

        # decodeName = self.generateGuidName()

        newFile = {
            "userID": userID,
            "dateOfPost": datetime.now(),
            "originalFileName": ShowUtfCharacterCode(documentName) + fileType,
            "decodedFileName": decodeName,
            "uploaderIP": {
                "fileSize": os.path.getsize(destPath),
                "home": "manual",
                "browser": "manual",
                "ip": "127.0.0.1"
            }
        }

        newFile1 = File(**newFile)
        newFile1.save()

        # ------------------------------------------------------------
        # ------------------------------------------------------------
        # ------------------------------------------------------------
        # Creating thumbs

        """
        thmum600_
        thmum200_
        thmum100_
        thmum50_
        thmum50CC_
        thmum100CC_
        """
        fileType = "JPG"
        if fileType in ("PNG", "JPG", "JPEG", "BMP", "GIF", "TIFF", "PDF", "SVG", "TILL"):
            img = Image.open(os.path.join(destFolder, decodeName))

            imgResizeMedium = img.resize((500, 700), Image.ANTIALIAS)
            imgResizeMedium.convert('RGB').save(os.path.join(destFolder, "thmum700_" + decodeName), "PNG", quality=10,
                                                optimize=True, progressive=True)
            newFile["decodedFileName"] = "thmum700_" + decodeName
            newFile1 = File(**newFile)
            newFile1.save()

            imgResizeMedium = img.resize((200, 200), Image.ANTIALIAS)
            imgResizeMedium.convert('RGB').save(os.path.join(destFolder, "thmum200_" + decodeName), "PNG", quality=10,
                                                optimize=True, progressive=True)
            newFile["decodedFileName"] = "thmum200_" + decodeName
            newFile1 = File(**newFile)
            newFile1.save()

            imgResizeSmall = img.resize((100, 100), Image.ANTIALIAS)
            imgResizeSmall.convert('RGB').save(os.path.join(destFolder, "thmum100_" + decodeName), "PNG", quality=10,
                                               optimize=True, progressive=True)
            newFile["decodedFileName"] = "thmum100_" + decodeName
            newFile1 = File(**newFile)
            newFile1.save()

            imgResizeTiny = img.resize((50, 50), Image.ANTIALIAS)
            imgResizeTiny.convert('RGB').save(os.path.join(destFolder, "thmum50_" + decodeName), "PNG", quality=10,
                                              optimize=True, progressive=True)
            newFile["decodedFileName"] = "thmum50_" + decodeName
            newFile1 = File(**newFile)
            newFile1.save()

            newFile["decodedFileName"] = "thmum50CC_" + decodeName
            newFile1 = File(**newFile)
            newFile1.save()

            newFile["decodedFileName"] = "thmum100CC_" + decodeName
            newFile1 = File(**newFile)
            newFile1.save()

        # ------------------------------------------------------------
        # ------------------------------------------------------------
        # ------------------------------------------------------------

        return decodeName

    def post(self, request, *args, **kwargs):
        file_obj = ""
        if "upload" in request.FILES:
            file_obj = request.FILES['upload']
        if "file" in request.FILES:
            file_obj = request.FILES['file']

        if "pic" in request.FILES:
            file_obj = request.FILES['pic']

        # 25 mb
        max_upload_size = (1024 * 1024) * 125
        if file_obj.size > max_upload_size:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # ...
        # do some staff with uploaded file
        # ...
        decodeName = self.generateGuidName()
        chunk = request.REQUEST.get('chunk', '0')
        chunks = request.REQUEST.get('chunks', '0')

        temp_file = os.path.join(tempfile.gettempdir(), 'tmp_' + decodeName + '_insecure.tmp')
        with open(temp_file, ('wb' if chunk == '0' else 'ab')) as f:
            for content in file_obj.chunks():
                f.write(content)
        stored_filename = ""

        dateOfPost = datetime.now()
        folderName = os.path.join(dateOfPost.strftime("%Y_%m_%d"), dateOfPost.strftime("%H"))
        destFolder = os.path.join(FILE_PATH, "userUploads", folderName)
        if not os.path.isdir(destFolder):
            path = Path(destFolder)
            path.mkdir(parents=True)

        destPath = os.path.join(destFolder, decodeName)
        shutil.copyfile(temp_file, destPath)
        os.remove(temp_file)

        env = request._request.environ

        newFile = {
            "userID": request.user.id,
            "dateOfPost": dateOfPost,
            "originalFileName": ShowUtfCharacterCode(file_obj.name),
            "decodedFileName": decodeName,
            "uploaderIP": {
                "fileSize": file_obj.size,
                "home": env["HOME"] if "HOME" in env else None,
                "browser": env["HTTP_USER_AGENT"] if "HTTP_USER_AGENT" in env else None,
                "ip": env["REMOTE_ADDR"] if "REMOTE_ADDR" in env else None
            }
        }

        fileType = newFile["originalFileName"].split(".")[
            len(newFile["originalFileName"].split(".")) - 1
            ].upper()

        if fileType == "TIFF":
            tmp_img = Image.open(os.path.join(destFolder, decodeName))
            tmp_img.convert('RGB').save(os.path.join(destFolder, decodeName), "PNG", quality=10,
                                        optimize=True, progressive=True)
            a = newFile["originalFileName"].split(".")
            newFile["originalFileName"] = a[0] + ".PNG"
            fileType = "PNG"

        # converting first page to jpeg
        filePDFAddr = ""
        if fileType == "PDF":
            filePDFAddr = self.convert(os.path.abspath(os.path.join(destFolder, decodeName)))

        newFile1 = File(**newFile)
        newFile1.save()

        # ------------------------------------------------------------
        # ------------------------------------------------------------
        # ------------------------------------------------------------
        # Creating thumbs

        """
        thmum600_
        thmum200_
        thmum100_
        thmum50_
        thmum50CC_
        thmum100CC_
        """
        if fileType in ("PNG", "JPG", "JPEG", "BMP", "GIF", "TIFF", "PDF", "SVG", "TILL"):
            if fileType == "PDF":
                img = Image.open(filePDFAddr)
            else:
                img = Image.open(os.path.join(destFolder, decodeName))

            imgResizeMedium = img.resize((500, 700), Image.ANTIALIAS)
            imgResizeMedium.convert('RGB').save(os.path.join(destFolder, "thmum700_" + decodeName), "PNG", quality=10,
                                                optimize=True, progressive=True)
            newFile["decodedFileName"] = "thmum700_" + decodeName
            newFile1 = File(**newFile)
            newFile1.save()

            imgResizeMedium = img.resize((200, 200), Image.ANTIALIAS)
            imgResizeMedium.convert('RGB').save(os.path.join(destFolder, "thmum200_" + decodeName), "PNG", quality=10,
                                                optimize=True, progressive=True)
            newFile["decodedFileName"] = "thmum200_" + decodeName
            newFile1 = File(**newFile)
            newFile1.save()

            imgResizeSmall = img.resize((100, 100), Image.ANTIALIAS)
            imgResizeSmall.convert('RGB').save(os.path.join(destFolder, "thmum100_" + decodeName), "PNG", quality=10,
                                               optimize=True, progressive=True)
            newFile["decodedFileName"] = "thmum100_" + decodeName
            newFile1 = File(**newFile)
            newFile1.save()

            imgResizeTiny = img.resize((50, 50), Image.ANTIALIAS)
            imgResizeTiny.convert('RGB').save(os.path.join(destFolder, "thmum50_" + decodeName), "PNG", quality=10,
                                              optimize=True, progressive=True)
            newFile["decodedFileName"] = "thmum50_" + decodeName
            newFile1 = File(**newFile)
            newFile1.save()

            radImage = imgResizeSmall
            if fileType != "TIFF":
                radImage = self.add_corners(imgResizeSmall, 50)
            radImage.convert('RGB').save(os.path.join(destFolder, "thmum50CC_" + decodeName), "PNG", quality=10,
                                         optimize=True, progressive=True)
            newFile["decodedFileName"] = "thmum50CC_" + decodeName
            newFile1 = File(**newFile)
            newFile1.save()

            radImage = imgResizeSmall
            if fileType != "TIFF":
                radImage = self.add_corners(imgResizeMedium, 100)
            radImage.convert('RGB').save(os.path.join(destFolder, "thmum100CC_" + decodeName), "PNG", quality=10,
                                         optimize=True, progressive=True)
            newFile["decodedFileName"] = "thmum100CC_" + decodeName
            newFile1 = File(**newFile)
            newFile1.save()

        # ------------------------------------------------------------
        # ------------------------------------------------------------
        # ------------------------------------------------------------

        result = {"name": decodeName}
        if "upload" in request.FILES:  # if upload from fck content
            funcNum = request.QUERY_PARAMS["CKEditorFuncNum"]
            message = ""
            url = "/api/v1/file/upload?q=" + decodeName
            hh = "<script type='text/javascript'>window.parent.CKEDITOR.tools.callFunction({0}, '{1}', '{2}');</script>".format(
                funcNum, url, message)
            return HttpResponse(hh)
        result['filename'] = ShowUtfCharacterCode(file_obj.name)
        return Response(result)


class FileAttsViewset(viewsets.ModelViewSet):
    lookup_field = "id"
    serializer_class = FileAttsSerializer
    queryset = FileAtts.objects.all()

    def create(self, request, *args, **kwargs):
        positionInstance = Position.objects.get(user=request.user, company=request.user.current_company)
        request.data["userID"] = request.user.id
        request.data["positionID"] = positionInstance.id
        return super(FileAttsViewset, self).create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        positionInstance = Position.objects.get(user=request.user, company=request.user.current_company)
        instance = self.queryset.get(id=kwargs["id"], userID=request.user.id)
        res = self.serializer_class(instance=instance).data
        return Response(res)
