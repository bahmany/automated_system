import base64
import os

from amspApp.Sales.serializers.KhoroojSerializer import HamkaranKhoroojFilesSerializer, KhoroojSMSSerializer

try:
    from StringIO import StringIO, BytesIO
except ImportError:
    from io import StringIO, BytesIO

from datetime import datetime

from PIL import Image
from django.utils import timezone

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import AllowAny

from amsp.settings import FILE_PATH, MEDIA_ROOT
from amspApp.FileServer.models import File
from amspApp.Sales.models import ExitsSMS, ExtisFiles, HamkaranKhoroojSMS, HamkaranKhoroojFiles
from amspApp.Sales.permissions.basePermissions import AllAccess
from amspApp.Sales.serializers.ExitsSerializer import ExtisFilesSerializer, ExitsSMSSerializer


@permission_classes([AllAccess])
@authentication_classes([AllowAny])
@csrf_exempt
def prevHavaleh(request):
    # try:
    uid = request.path.split("/")[2]
    if len(uid) != 6:
        return render_to_response('others/errors/invalid.html', {}, context_instance=RequestContext(request))
    instance = HamkaranKhoroojSMS.objects.get(linkID=uid)
    files = HamkaranKhoroojFiles.objects.filter(khoroojLink=instance.khoroojLink)
    if len(files) == 0:
        return render_to_response('others/errors/not_found.html', {}, context_instance=RequestContext(request))
    ser = HamkaranKhoroojFilesSerializer(instance=files, many=True).data
    if len(ser) > 0:
        sx = KhoroojSMSSerializer(instance=instance, data={"seenDate": timezone.now()}, partial=True)
        sx.is_valid(raise_exception=True)
        sx.save()
        ff = ser[0]["Files"]["uploaded"]
        images = []
        for f in ff:
            fileToDownload = File.objects.filter(decodedFileName=f['imgInf']['orgname'])
            if len(fileToDownload) > 0:
                fileToDownload = fileToDownload[0]
                # fileToDownload = fileToDownload[0]
                # reading file into memory---
                views = {
                    'userID': request.user.id,
                    'dateOf': datetime.now()
                }

                h = fileToDownload.originalFileName
                folderName = os.path.join(fileToDownload.dateOfPost.strftime("%Y_%m_%d"),
                                          fileToDownload.dateOfPost.strftime("%H"))
                destFolder = os.path.join(FILE_PATH, "userUploads", folderName)
                fullPath = os.path.abspath(os.path.join(destFolder, f['imgInf']['orgname']))

                size = 1000, 1400
                if os.path.exists(fullPath):
                    temp = BytesIO()
                    photo = Image.open(fullPath).convert('RGBA')
                    photo.putalpha(255)
                    photo = photo.resize(size)
                    photo.save(temp, format="png")
                    photo = Image.open(temp)
                    watermark = Image.open(os.path.abspath(os.path.join(MEDIA_ROOT, 'watermark.png', ))).convert('RGBA')
                    watermark = watermark.resize(size)
                    photo.paste(watermark, (0, -100,), watermark)
                    temp2 = BytesIO()
                    photo.save(temp2, format="png")
                    # response = HttpResponse(temp2.getvalue(), content_type="image/png")
                    # response['Content-Disposition'] = 'attachment; filename=%s' % (
                    #         f['imgInf']['name'].split('.')[0] + ".png")
                    tp = temp2.getvalue()
                    output_s = base64.b64encode(tp)
                    images.append(output_s)
                    # image/png

            # f["imgLink"] = f["imgLink"].replace("thmum50_", "thmum700_")
        return render_to_response('Sales/Khorooj/havaleh.html', {'images': images, instance: ser},
                                  context_instance=RequestContext(request))
        # else:
        #     return render_to_response('Sales/Khorooj/havaleh.html', {instance: ser},
        #                               context_instance=RequestContext(request))
    # except:
    #     return render_to_response('others/errors/invalid.html', {}, context_instance=RequestContext(request))
