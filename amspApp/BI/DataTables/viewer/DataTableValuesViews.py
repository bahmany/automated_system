import io
import uuid

import xlsxwriter
from asq.initiators import query
from django.http import HttpResponse
from django.utils import timezone
from mongoengine import Q
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.BPMSystem.models import TableSelectedItems, LunchedProcessArchive, ExtraDataForTableSelectedItems
from amspApp.BPMSystem.serializers.TableSelectedItemsSerializer import TableSelectedItemsSerializer, \
    ExtraDataForTableSelectedItemsSerializer
# from amspApp.Bpms.models import LunchedProcess
from amspApp.CompaniesManagment.Processes.models import Bpmn
from amspApp.BI.DataTables.models import DataTable, DataTableValues, TemporaryDataTableValuesForProcess
from amspApp.BI.DataTables.serializers.DataTableValuesSerializer import DataTableValuesSerializer, \
    TemporaryDataTableValuesForProcessSerializer
from amspApp._Share.CharacterHandle import ConvertUnicodeEscapeCodeToEnglish, ShowUtfCharacterCode
from amspApp._Share.ListPagination import DetailsPagination
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset
from amspApp.BPMSystem.models import LunchedProcess


# try:
#     import cStringIO as StringIO
# except ImportError:
#     import StringIO


class DataTableValuesViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = DataTableValues.objects.all()
    serializer_class = DataTableValuesSerializer
    pagination_class = DetailsPagination

    # def list(self, request, *args, **kwargs):

    def destroy(self, request, *args, **kwargs):
        posInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        companyID = posInstance.companyID
        posID = posInstance.positionID

        return super(DataTableValuesViewSet, self).destroy(request, *args, **kwargs)

    # def filterDataForProcess(self):

    @detail_route(methods=["post"])
    def filterData(self, request, *args, **kwargs):
        posInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        companyID = posInstance.companyID
        posID = posInstance.positionID
        self.list(request, *args, **kwargs)
        filter = []
        for col in request.data:
            if col["dataType"] == "lookup":
                if "value" in col:
                    if type(col["value"]) == list:
                        filter.append({
                            "fieldname": col["fieldname"],
                            "value": col["value"],
                            "lookup": True
                        })
                    if type(col["value"]) == str:
                        filter.append({
                            "fieldname": col["fieldname"],
                            "value": col["value"],
                            "lookup": True})

                        # Q(values__value={"$regex": ".*" + col["value"] + ".*"}))

            if col["dataType"] == "string":
                if "value" in col:
                    if type(col["value"]) == str:
                        if len(col["value"]) > 0:
                            filter.append({
                                "fieldname": col["fieldname"],
                                "value": col["value"]
                            })
            if col["dataType"] == 'date':
                if "value" in col:
                    if type(col["value"]) == str:
                        fval = {
                            "fieldname": col["fieldname"],
                            "value": 13000000 + int(col["value"]) if col["value"] != "" else 0
                        }
                        if "filterType" in col:
                            fval["filterType"] = col["filterType"]
                            if col["filterType"] == "bt":
                                if "filterTypeVal" in col:
                                    fval["between"] = 13000000 + int(col["filterTypeVal"]) if col[
                                                                                                  "filterTypeVal"] != "" else 9999999
                        filter.append(fval)

            if col["dataType"] == 'time':
                if "value" in col:
                    if type(col["value"]) == str:
                        fval = {
                            "fieldname": col["fieldname"],
                            "value": int(col["value"]) if col["value"] != "" else 0
                        }
                        if "filterType" in col:
                            fval["filterType"] = col["filterType"]
                            if col["filterType"] == "bt":
                                if "filterTypeVal" in col:
                                    fval["between"] = int(col["filterTypeVal"]) if col["filterTypeVal"] != "" else 9999
                        filter.append(fval)
            if col["dataType"] == 'int':
                if "value" in col:
                    if type(col["value"]) == str:
                        fval = {
                            "fieldname": col["fieldname"],
                            "value": int(col["value"]) if col.get("value") else 0
                        }
                        if "filterType" in col:
                            fval["filterType"] = col["filterType"]
                            if col["filterType"] == "bt":
                                if "filterTypeVal" in col:
                                    fval["between"] = int(col["filterTypeVal"]) if col[
                                                                                       "filterTypeVal"] == "" else 99999999999999999999
                        filter.append(fval)
        finalFilter = None

        for flt in filter:
            firstFilter = None
            secondFilter = None

            if (type(flt["value"]) == list):
                firstFilter = Q(values__fieldname=flt["fieldname"])
                secondFilter = Q(values__value__in=flt["value"])

            else:
                if (type(flt["value"]) == int):
                    if (flt["value"] == 0):
                        flt["filterType"] = "gt"

                if "filterType" in flt:
                    if flt["filterType"] == "eq":
                        if "value" in flt:
                            if flt["value"]:
                                firstFilter = Q(values__fieldname=flt["fieldname"])
                                secondFilter = Q(values__value=flt["value"])
                    if flt["filterType"] == "gt":
                        if "value" in flt:
                            if flt["value"]:
                                firstFilter = Q(values__match={'fieldname': flt["fieldname"]})
                                # secondFilter = Q(values__value__gte=flt["value"])
                                secondFilter = Q(values__match={'value': {'$gte': flt["value"]}})
                    if flt["filterType"] == "lt":
                        if "value" in flt:
                            if flt["value"]:
                                firstFilter = Q(values__match={'fieldname': flt["fieldname"]})
                                # firstFilter = Q(values__fieldname=flt["fieldname"])
                                # secondFilter = Q(values__value__lte=flt["value"])
                                secondFilter = Q(values__match={'value': {'$lte': flt["value"]}})
                    if flt["filterType"] == "bt":
                        if "value" in flt:
                            if flt["value"]:
                                if "between" in flt:
                                    if flt["between"]:
                                        firstFilter = Q(values__match={'fieldname': flt["fieldname"]})
                                        secondFilter = Q(
                                            values__match={'value': {'$gte': flt["value"], '$lte': flt["between"]}})

                else:
                    firstFilter = Q(values__match={'fieldname': flt["fieldname"]})
                    if type(flt["value"]) == str:
                        if flt["value"] != "":
                            secondFilter = Q(values__value={"$regex": ".*" + flt["value"] + ".*"})
                    else:
                        if flt["value"] != "":
                            secondFilter = Q(values__value=flt["value"])

            self.queryset = self.get_queryset()
            if firstFilter != None and secondFilter != None:
                self.queryset = self.queryset.filter(firstFilter & secondFilter)

        # for excel
        if 'xls' in request.query_params:
            retData = list(self.queryset)
            beforeJson = [
                [{'fn': y["fieldname"] if "fieldname" in y else "", "v": y["value"] if "value" in y else ""} for y in
                 x.values] for x in retData]
            filename = "DataTable_" + uuid.uuid1().hex + ".xlsx"
            # fileFolder = FILE_PATH + "/"
            # filename = fileFolder + filename
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output)

            fontFormat = workbook.add_format({"font_name": "B Nazanin"})
            mySheet = workbook.add_worksheet("DBTable")
            mySheet.is_right_to_left = True
            # getting col names
            colsUn = []
            cols = [[y["fn"] for y in x] for x in beforeJson]
            for c in cols:
                for cc in c:
                    colsUn.append(cc)
            cols = query(colsUn).distinct().to_list()

            data = []
            for bJ in beforeJson:
                row = []
                for cc in cols:
                    vv = None
                    for b in bJ:
                        if b["fn"] == cc:
                            vv = b["v"] if 'v' in b else None
                    row.append(vv)

                data.append(row)
            sheetHeadres = cols
            bold = workbook.add_format({'bold': True, "font_name": "B Nazanin"})
            simple = workbook.add_format({'bold': False, "font_name": "B Nazanin"})

            cindex = 0
            for c in cols:
                mySheet.write(0, cindex, c, bold)
                cindex += 1
            dindex = 0
            for d in data:
                dindex += 1
                ddindex = 0
                for dd in d:
                    mySheet.write(dindex, ddindex, dd, simple)
                    ddindex += 1
            workbook.close()
            output.seek(0)
            # fsock = open(filename, "rb")
            # with open(output.read(), "rb") as fid:
            #     filedata = fid.read()
            # mime = GetMimeType(f.split(".")[1])
            response = HttpResponse(output,
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=%s' % (filename)
            return response

        result = self.list(request, *args, **kwargs)

        # saving filters state
        # if len(request.data) > 0:
        #     result.data.cols = request.data

        return result

        # fields to be filter

    @detail_route(methods=["get"])
    def getDataTableTmpValues(self, request, *args, **kwargs):
        lst = TemporaryDataTableValuesForProcess.objects.filter(
            dataTableLink=kwargs["id"],
            launchedProcessID=request.query_params.get("processID"),
        )
        if (lst.count() == 0):
            return Response({'values':[]})

        result = TemporaryDataTableValuesForProcessSerializer(instance=lst, many=True).data[0]
        return Response(result)

        # fields to be filter

    @detail_route(methods=["post"])
    def updateTmpDataTable(self, request, *args, **kwargs):
        # getting launched process ID
        processInstance = LunchedProcess.objects.get(id=request.data['launchedProcessID'])
        posInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(request)

        request.data['bpmnID'] = LunchedProcess.objects.get(id=request.data['launchedProcessID']).bpmn["id"]
        request.data['companyId'] = posInstance.companyID
        request.data['position_id'] = posInstance.positionID
        serial = TemporaryDataTableValuesForProcessSerializer(data=request.data)
        serial.is_valid(raise_exception=True)
        TemporaryDataTableValuesForProcess.objects.filter(
            dataTableLink=request.data.get('dataTableLink'),
            launchedProcessID=request.data.get('launchedProcessID'),
        ).delete()
        serial.save()

        return Response(serial.data)
        # fields to be filter

    @list_route(methods=["get"])
    def convertToNew(self, request, *args, **kwargs):
        list = self.queryset
        for item in list:
            valueSerial = self.serializer_class(instance=item).data
            for v in valueSerial['values']:
                if v["dataType"] == "date":
                    if "value" in v:
                        if type(v["value"]) == str:
                            if v["value"] != "":
                                v["value"] = int(v["value"].replace("/", ""))

                if v["dataType"] == "time":
                    if "value" in v:
                        if type(v["value"]) == str:
                            if v["value"] != "":
                                v["value"] = int(v["value"].replace(":", ""))
            newValSerial = self.serializer_class(instance=item, data=valueSerial)
            newValSerial.is_valid(raise_exception=True)
            newValSerial.save()

        seclist = self.queryset
        for item in seclist:
            valueSerial = self.serializer_class(instance=item).data
            for v in valueSerial['values']:
                if v["dataType"] == "date":
                    if "value" in v:
                        if type(v["value"]) == int:
                            if v["value"] < 13000000:
                                v["value"] = 13000000 + v["value"]

            newValSerial = self.serializer_class(instance=item, data=valueSerial)
            newValSerial.is_valid(raise_exception=True)
            newValSerial.save()

        return Response({"result": "succ"})

    def update(self, request, *args, **kwargs):
        # prevInstance =
        posInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        companyID = posInstance.companyID
        posID = posInstance.positionID
        prevInstance = self.get_queryset().get(id=kwargs["id"])
        prevInstance = self.get_serializer(instance=prevInstance).data
        for prevRow in prevInstance["values"]:
            for newRow in request.data["values"]:
                if prevRow["fieldname"] == newRow["fieldname"]:
                    prevRow["value"] = newRow["value"] if "value" in newRow else None

        # beforeUpate = self.get_serializer(instance=self.get_queryset().get(id=kwargs["id"]),  data = prevInstance).data

        serializer = self.get_serializer(self.get_queryset().get(id=kwargs["id"]), data=prevInstance)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @detail_route(methods=["get"])
    def getFieldNames(self, request, *args, **kwargs):
        dt = DataTable.objects.get(id=kwargs.get("id"))
        dt = [{"name": x["fieldname"], "selected": None} for x in dt.fields["list"]]
        return Response(dt)

    @list_route(methods=["post"])
    def addExtraValues(self, request, *args, **kwargs):
        # deleting all same key
        ExtraDataForTableSelectedItems.objects.filter(
            tableSelectedItemsLink=request.data.get("TableSelectedItemID")).delete()
        extraDt = dict(
            positionID=str(GetPositionViewset().GetCurrentPositionDocumentInstance(request).id),
            companyID=request.data.get("companyId"),
            tableSelectedItemsLink=request.data.get("TableSelectedItemID"),
            values=request.data.get("extraValues"),
            desc={},
        )
        dt = ExtraDataForTableSelectedItemsSerializer(data=extraDt)
        dt.is_valid(raise_exception=True)
        dt.save()
        return Response(dt.data)

    @detail_route(methods=["post"])
    def list(self, request, *args, **kwargs):
        posInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        companyID = posInstance.companyID
        posID = posInstance.positionID
        dataTableInstance = DataTable.objects.get(id=request.query_params["dt"])

        # if calling from bpmn activate bpmn
        # if the following code find it is task from bpms
        # then at the end add extra fields if it contains

        currentTaskDict = {}
        if (request.query_params.get("bpmnid") and request.query_params.get("taskID") and request.query_params.get(
                "processid")):

            # getting bpmn instance
            bpmninstance = Bpmn.objects.get(id=request.query_params.get("bpmnid"))
            processInstance = LunchedProcess.objects.filter(id=request.query_params.get("processid")).first()
            if not processInstance:  # if process completed
                processInstance = LunchedProcessArchive.objects.filter(id=request.query_params.get("processid")).first()
            for task in processInstance.bpmn['form']:
                if task["bpmnObjID"] == request.query_params.get("taskID"):
                    t = 1
                    for field in task["schema"]["fields"]:
                        if field.get("datatable") == str(dataTableInstance.id):
                            currentTaskDict = field

            # finding table

        result = {}
        self.queryset = self.get_queryset().filter(dataTableLink=dataTableInstance.id).order_by("-postDate")
        """
        not we must set filters
        """
        filter = request.query_params.get("datafilter")
        filters = []
        if filter:
            for fil in filter.split("9fv38qa"):
                filters.append({
                    'dataType': fil.split("55981v8")[1],
                    'fieldname': fil.split("55981v8")[0],
                    'value': fil.split("55981v8")[2],
                })

        for f in filters:
            if f.get("value"):
                if f.get("value") != "":
                    # regx = re.compile(f.get("value"), re.IGNORECASE)
                    # dd = Q(values__fieldname=f.get("fieldname")) & Q(values__value={'$regex': f.get("value")})
                    if f.get("dataType") == "int":
                        dd = Q(values={"$elemMatch": {
                            "value": int(f.get("value")),
                            "fieldname": f.get("fieldname"),
                        }})

                    else:
                        dd = Q(values={"$elemMatch": {
                            "value": {'$regex': f.get("value"), '$options': 'i'},
                            "fieldname": f.get("fieldname"),
                        }})
                        if f.get("value").isdigit():
                            dd = dd | Q(values={"$elemMatch": {
                                "value": int(f.get("value")),
                                "fieldname": f.get("fieldname"),
                            }})

                    self.queryset = self.queryset.filter(dd)

        # it means we are in desiginng form mode
        if (not (request.query_params.get("dataTableID")) and not (request.query_params.get("dt"))):
            return Response({})

        # for calculating selected field in bpms area
        # but when it call by another place selected count change to be zero !
        selctedCount = 0
        if request.query_params.get("bpmnid"):
            selctedCount = TableSelectedItems.objects.filter(
                bpmn=request.query_params.get("bpmnid"),
                process=request.query_params.get("processid"),
                # taskID=request.query_params.get("taskID"),
                objID=request.query_params.get("objID"),
                dataTableID=request.query_params.get("dataTableID"),
                # dataTableValueID=r["id"]
            ).count()
            justShowSelected = request.query_params.get("justShowSelected")
            if justShowSelected:
                if justShowSelected == "true":
                    qs = TableSelectedItemsSerializer(
                        instance=
                        TableSelectedItems.objects.filter(
                            bpmn=request.query_params.get("bpmnid"),
                            process=request.query_params.get("processid"),
                            # taskID=request.query_params.get("taskID"),
                            objID=request.query_params.get("objID"),
                            dataTableID=request.query_params.get("dataTableID"),
                            # dataTableValueID=r["id"]
                        ),
                        many=True
                    ).data

                    selectedValueIDs = [x["dataTableValueID"]["id"] for x in qs]

                    if len(selectedValueIDs) > 0:
                        self.queryset = self.queryset.filter(id__in=selectedValueIDs)

        rrresss = super(DataTableValuesViewSet, self).list(request, *args, **kwargs)
        result["data"] = rrresss.data
        result["selectedCount"] = selctedCount
        lst = list(dataTableInstance.fields["list"])

        for l in lst:
            if l["dataType"] == "lookup":
                l["english"] = ConvertUnicodeEscapeCodeToEnglish(ShowUtfCharacterCode(l["fieldname"])).replace(" ", "")
                if l["lookupType"] == "datatables":
                    destDataTableInstance = DataTable.objects.get(name=l["lookup_datatable_name"], companyId=companyID)
                    destValues = DataTableValues.objects.filter(dataTableLink=destDataTableInstance.id)
                    destValues = self.serializer_class(instance=destValues, many=True).data
                    lookupRes = []
                    for d in destValues:
                        display = ""
                        vlu = ""
                        for dsfn in l["lookup_datatable_displayfieldnames"].split(";"):
                            if (d["values"][0]["fieldname"] == dsfn):
                                display = d["values"][0]["value"]
                            for dsfv in l["lookup_datatable_valuefield"].split(";"):
                                if (d["values"][0]["fieldname"] == dsfv):
                                    vlu = d["values"][0]["value"]
                        lookupRes.append({
                            "display": display,
                            "value": vlu
                        })

                    l["lookupValues"] = lookupRes
                if l["lookupType"] == "static":
                    lookupRes = []
                    for lxx in l["lookup_static_items"].split("\n"):
                        lookupRes.append({
                            "display": lxx,
                            "value": lxx,
                        })
                    l["lookupValues"] = lookupRes

        # checking permissions
        # just record owner can edit rows
        for l in result["data"]["results"]:
            l["owner"] = 2  # not owner
            if l["position_id"] == posInstance.positionID:
                l["owner"] = 1  # this is owner
            # special permissions
            default_owner = l["owner"]
            for f in dataTableInstance.fields['list']:
                for ll in l["values"]:
                    l["owner"] = default_owner
                    if f["fieldname"] == ll["fieldname"]:
                        if "isLimited" in f:
                            if f["isLimited"] == True:
                                if "limitedUsers" in f:
                                    if len(f["limitedUsers"]) != 0:
                                        for limUsers in f["limitedUsers"]:
                                            if limUsers["positionID"] == posInstance.positionID:
                                                l["owner"] = 3  # invisible
                                                if "canEdit" in limUsers:
                                                    if limUsers["canEdit"] == True:
                                                        l["owner"] = 4  # can edit this record sprecific
                                                        break
                        ll["owner"] = l["owner"]
                        if l["position_id"] == posInstance.positionID:
                            ll["owner"] = 1
            if l["position_id"] == posInstance.positionID:
                l["owner"] = 1

                # for f in dataTableInstance.fields['list']:
                #     for ll in l["values"]:
                #         ll = ll

        # lst = query(lst)
        result["cols"] = lst

        for r in result["data"]["results"]:
            for rr in r["values"]:
                if "lookupValues" in rr:
                    rr.pop("lookupValues", None)

        # setting invisible permissions
        hiddenFields = []
        for templateField in dataTableInstance.fields["list"]:
            if "limitedUsers" in templateField:
                if len(templateField["limitedUsers"]) != 0:
                    for limitedUser in templateField["limitedUsers"]:
                        if posInstance.positionID == limitedUser["positionID"]:
                            if "canEdit" in limitedUser:
                                if limitedUser["canEdit"] == False:
                                    hiddenFields.append(templateField["fieldname"])
                            else:
                                hiddenFields.append(templateField["fieldname"])
        hiddenFieldsID = []
        ii = -1
        for templateField in dataTableInstance.fields["list"]:
            ii = ii + 1
            for h in hiddenFields:
                if templateField["fieldname"] == h:
                    hiddenFieldsID.append(ii)
        hiddenFieldsID.sort(reverse=True)
        for fgR in hiddenFieldsID:
            del result["cols"][fgR]

        result["canEdit"] = True
        if posInstance.positionID != dataTableInstance.position_id:
            for user in dataTableInstance["publishedUsers"]["list"]:
                if posInstance.positionID == user["positionID"]:
                    if "canEdit" not in user:
                        result["canEdit"] = False
                    else:
                        result["canEdit"] = user["canEdit"]

        # if it calls from bpmn area
        if request.query_params.get("bpmnid"):
            if request.query_params.get("from") == "pro":
                result = self.makeItForProcess(request, result)
            if currentTaskDict.get("datatable"):
                result["extraCols"] = currentTaskDict["extraField"]
                # getting extra fields values
                for dataTableValue in result.get("data").get("results"):

                    addedValueInstance = ExtraDataForTableSelectedItems.objects.filter(
                        tableSelectedItemsLink=dataTableValue.get("TableSelectedItemID"))
                    if addedValueInstance.count() > 0:
                        addedValueInstance = addedValueInstance.first()
                    else:
                        addedValueInstance = None

                    # make defaults values for cells
                    dataTableValue["extraCols"] = result["extraCols"]
                    dataTableValue["extraValues"] = result["extraCols"]

                    # this line transfer data to results
                    if dataTableValue.get("selectedBefore"):
                        addedValues = ExtraDataForTableSelectedItemsSerializer(instance=addedValueInstance).data
                        dataTableValue["extraValues"] = addedValues.get("values")

                    # if there is no values this line add empty cells
                    if not (dataTableValue["extraValues"]):
                        dataTableValue["extraValues"] = result["extraCols"]

        return Response(result)

    def makeItForProcess(self, request, result):

        for r in result["data"]["results"]:
            qs = TableSelectedItems.objects.filter(
                bpmn=request.query_params.get("bpmnid"),
                process=request.query_params.get("processid"),
                # taskID=request.query_params.get("taskID"),
                # objID=request.query_params.get("objID"),
                dataTableID=request.query_params.get("dataTableID"),
                dataTableValueID=r["id"]
            )

            r["selectedBefore"] = bool(qs.count())
            if r["selectedBefore"]:
                r["TableSelectedItemID"] = str(qs[0].id)
        return result

    def retrieve(self, request, *args, **kwargs):
        posInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        companyID = posInstance.companyID
        posID = posInstance.positionID
        instance = self.get_queryset().get(id=kwargs["id"])
        dataTableInstance = DataTable.objects.get(id=instance.dataTableLink)

        hiddenFields = []
        readonlyFields = []
        for templateField in dataTableInstance.fields["list"]:
            if "limitedUsers" in templateField:
                if len(templateField["limitedUsers"]) != 0:
                    for limitedUser in templateField["limitedUsers"]:
                        if posInstance.positionID == limitedUser["positionID"]:
                            if "canEdit" in limitedUser:
                                if limitedUser["canEdit"] == False:
                                    hiddenFields.append(templateField["fieldname"])
                            else:
                                hiddenFields.append(templateField["fieldname"])

        hiddenFieldsID = []
        # remove invisible and hidden fields
        ii = -1
        for templateField in dataTableInstance.fields["list"]:
            ii = ii + 1
            for h in hiddenFields:
                if templateField["fieldname"] == h:
                    hiddenFieldsID.append(ii)
        hiddenFieldsID.sort(reverse=True)
        # getting readonly and invisible fields name
        res = super(DataTableValuesViewSet, self).retrieve(request, *args, **kwargs)

        for fgR in hiddenFieldsID:
            for fvf in res.data["values"]:
                for hf in hiddenFields:
                    if fvf["fieldname"] == hf:
                        del res.data["values"][fgR]

        return res

    @detail_route(methods=["post"])
    def postValue(self, request, *args, **kwargs):
        posInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        companyID = posInstance.companyID
        posID = posInstance.positionID
        dataTableInstance = DataTable.objects.get(id=kwargs["id"])
        # position_id = IntField(null=False, required=True)  # first creator pos id
        # companyId = IntField(null=False, required=True)  # first creator company id
        # postDate = DateTimeField(default=datetime.now(), required=False)
        # desc = StringField(null=True, required=False)
        # exp = DictField(null=True, required=False)
        # values = DictField(null=True, required=False)
        # dataTableLink = ObjectIdField(null=False, required=True)
        data = {}
        data["position_id"] = posID
        data["companyId"] = companyID
        data["postDate"] = timezone.now()
        data["dataTableLink"] = dataTableInstance.id

        data["values"] = request.data

        serial = self.serializer_class(data=data)
        serial.is_valid(raise_exception=True)
        serial.save()

        return Response(serial.data)
