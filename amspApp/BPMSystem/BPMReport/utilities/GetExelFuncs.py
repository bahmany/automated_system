# coding=utf-8
import datetime
from time import strptime
import uuid
from bson import ObjectId
import xlsxwriter
from amsp.settings import FILE_PATH
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh_with_time, mil_to_sh


def ReportToExel(data, hearNames, hearIds):
    filename = uuid.uuid1().hex + "Report.xlsx"
    fileFolder = FILE_PATH+"XLSreportsBpms/"
    filename = fileFolder + filename
    workbook = xlsxwriter.Workbook(filename)
    fontFormat = workbook.add_format({"font_name": "B Nazanin"})
    mySheet = workbook.add_worksheet("Report")
    sheetHeadres = ["نوع کار", "عنوان کار", "آغازگر کار", "تاریخ آغاز کار", "آیا پایان یافته"]
    sheetHeadres += hearNames

    # ========== add our reports header here =================
    bold = workbook.add_format({'bold': True})
    i = 0
    for header in sheetHeadres:
        mySheet.write(0, i, header, bold)
        i += 1
    # ========== add our reports data here =================
    indexR = 1
    for item in data:
        posFieldList = []
        tabelFieldList = []
        if 'processObjs' in item:
            for tht in item['processObjs']:
                if tht['type'] == 'chartPositionselectlist':
                    posFieldList.append(tht['name'])
                elif tht['type'] == 'amftabel':
                    tabelFieldList.append(tht['name'])
        mySheet.write(indexR, 0, item['bpmnName'], fontFormat)
        mySheet.write(indexR, 1, item['lpName'], fontFormat)
        mySheet.write(indexR, 2, item['lpPositionName'], fontFormat)
        mySheet.write(indexR, 3,
                      mil_to_sh_with_time(item['lpStartDate'].replace('T', ' ').split('.')[0]),
                      fontFormat)
        mySheet.write(indexR, 4, 'بله' if item['isDone'] else 'خیر', fontFormat)
        indexC = 5
        for formItm in hearIds:
            if formItm in item['formData'].keys():
                if formItm in posFieldList:
                    posObj = PositionsDocument.objects.get(id=ObjectId(item['formData'][formItm]))
                    mySheet.write(indexR, indexC, posObj.profileName + ' - ' + posObj.chartName, fontFormat)
                elif formItm in tabelFieldList:
                    mySheet.write(indexR, indexC, ' ', fontFormat)
                else:
                    mySheet.write(indexR, indexC, item['formData'][formItm], fontFormat)
            else:
                mySheet.write(indexR, indexC, ' ', fontFormat)
            indexC += 1
        indexR += 1

    workbook.close()
    return filename