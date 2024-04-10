import chunk
import json
import os
import shutil
import uuid
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from rest_framework import views
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from amsp.settings import FILE_PATH
from amspApp.FileServer.models import File
from amspApp.FileServer.serializers.FileSerializer import FileSerializer
from amspApp._Share.CharacterHandle import ShowUtfCharacterCode
from amspApp._Share.GetMime import GetMimeType


class BpmsFileViewSet(object):
    fileFolder = FILE_PATH+"bpms/"

    def generateGuidName(self):
        return uuid.uuid4().hex + uuid.uuid4().hex

    def createEngineTempFile(self, engineBinary):
        fileName=self.fileFolder + str(self.generateGuidName())
        fh = open(fileName, "wb")
        fh.write(engineBinary)
        fh.close()
        return fileName

    def updateEngineTempFile(self,fileAddr,newData):
        fh = open(fileAddr, "wb")
        fh.write(newData)
        fh.close()
        return fileAddr

    def getEngineTempFile(self, fileAddr):
        with open(fileAddr,"rb") as fh:
            engineBinary = fh.read()
        fh.close()
        return engineBinary

    def deleteEngineTempFile(self):
        pass
