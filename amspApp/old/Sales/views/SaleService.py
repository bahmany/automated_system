import csv
import tempfile
import uuid

import os

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from amspApp.Sales.permissions.basePermissions import AllAccess
from amspApp.Sales.views.SalesView import SalesViewSet


@permission_classes([AllAccess])
@authentication_classes([AllowAny])
@csrf_exempt
def getMojoodiCsv(request):
    # kwargs["isItExcel"] = True
    result = SalesViewSet().getMojoodiesNoAuth(request)
    res = []

    for r in result.data["results"]:
        p = {}
        p["MojoodiForoosh"] = r["total"]
        p["PartCode"] = r["PartCode"]
        p["keifiat"] = r["keifiat"]
        p["keshvar"] = r["keshvar"]
        p["sath"] = r["sath"]
        p["temper"] = r["temper"]
        p["arz"] = r["arz"]
        p["zekhamat"] = r["zekhamat"]
        p["anbar"] = r["qty"]
        p["qtyPish"] = r["qtyPish"]
        p["qtyConv"] = r["qtyConv"]

        res.append(p)

    # vv = dicttoxml(res, custom_root='test', attr_type=False)
    if len(res) == 0:
        return Response({})

    headings = list(res[0].keys())

    def generateGuidName():
        return uuid.uuid4().hex + uuid.uuid4().hex

    decodeName = generateGuidName()
    temp_file = os.path.join(tempfile.gettempdir(), 'tmp_' + decodeName + '_insecure.tmp')
    with open(temp_file, "w", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, headings)
        dict_writer.writeheader()
        dict_writer.writerows(res)

    # with open(temp_file,'w', newline='') as myCSVFile:
    #     csvWriter = csv.writer(myCSVFile, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
    #     csvWriter.writerow(headings)
    #     for data in res:
    #         csvWriter.writerow(data)

    # output = io.BytesIO()
    # fileAddr = os.path.join(tmpdir, 'excel.xlsx')

    resp = HttpResponse('')
    with open(temp_file, 'r') as tmp:
        filename = tmp.name.split('/')[-1]
        resp = HttpResponse(tmp, content_type='text/csv;charset=UTF-8')
        resp['Content-Disposition'] = "attachment; filename=bahmany.csv"

    return resp