import io
from datetime import datetime, timedelta

import xlsxwriter
from mongoengine import Q
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.ControlProject.permissions.ControlProjectBase import IsOwnerOrReadOnly_CostCol
from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh, sh_to_mil, mil_to_sh_with_time, \
    changeDateNameToShamsiDate
from amspApp.Infrustructures.Classes.MongoEngineSearchFilterBackend import FilterDataTables
from amspApp.MyProfile.models import Profile
from amspApp.Sales.models import SalesCustomerProfileSalesRequestsSizes, SalesCustomerProfile
from amspApp.Sales.permissions.basePermissions import CanCruidSale, IsHeSalePerson
from amspApp.Sales.serializers.CustomerProfileSerializer import CustomerProfileSalesRequestsSizesSerializer, \
    CustomerProfileSerializer
from amspApp.Sales.views.sheetSaleDict import sheetRequests
from amspApp.Sales.views.un_sheetSaleDict import un_sheetRequests
from amspApp._Share.ListPagination import ListPagination, DataTablesPagination
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class SalesCustomerProfileSalesRequestsSizesViewSet(viewsets.ModelViewSet):
    pagination_class = ListPagination
    lookup_field = "id"
    serializer_class = CustomerProfileSalesRequestsSizesSerializer
    # queryset = SalesCustomerProfileSalesRequestsSizes.objects.all().order_by('-desc.tarikheSabt')
    queryset = SalesCustomerProfileSalesRequestsSizes.objects.all().order_by('-id')
    permission_classes = (IsOwnerOrReadOnly_CostCol, CanCruidSale, IsHeSalePerson,)
    filter_backends = (FilterDataTables,)
    search_fields = ("profileLink__name", "desc__zekhamat",)
    datatablesTypes = {
        'desc.zekhamat': 'int',
        'desc.temper': 'int',
        'desc.tool': 'int',
        'desc.arz': 'int',
        'desc.qty': 'int',
    }

    def update(self, request, *args, **kwargs):
        request.data["desc"]["tarikheSabt"] = datetime.strptime(sh_to_mil(request.data["desc"]["tarikheSabt"]),
                                                                "%Y/%m/%d")
        request.data["desc"]["tarikheSabtShamsi"] = request.data["desc"]["tarikheSabt"]
        request.data["desc"]["tarikheSabtShamsiDayName"] = changeDateNameToShamsiDate(
            request.data["desc"]["tarikheSabt"].strftime("%A"))

        result = super(SalesCustomerProfileSalesRequestsSizesViewSet, self).update(request, *args, **kwargs)
        return result

    def create(self, request, *args, **kwargs):
        request.data["desc"]["tarikheSabt"] = datetime.strptime(sh_to_mil(request.data["desc"]["tarikheSabt"]),
                                                                "%Y/%m/%d")
        request.data["desc"]["tarikheSabtShamsi"] = request.data["desc"]["tarikheSabt"]
        request.data["desc"]["tarikheSabtShamsiDayName"] = changeDateNameToShamsiDate(
            request.data["desc"]["tarikheSabt"].strftime("%A"))
        result = super(SalesCustomerProfileSalesRequestsSizesViewSet, self).create(request, *args, **kwargs)
        return result

    def retrieve(self, request, *args, **kwargs):
        result = super(SalesCustomerProfileSalesRequestsSizesViewSet, self).retrieve(request, *args, **kwargs)
        result.data["desc"]["tarikheSabt"] = mil_to_sh(result.data["desc"].get('tarikheSabt'))
        return result

    def get_queryset(self):
        if "profileID" in self.request.query_params:
            if self.request.query_params["profileID"]:
                self.queryset = self.queryset.filter(profileLink=self.request.query_params["profileID"])
        return super(SalesCustomerProfileSalesRequestsSizesViewSet, self).get_queryset()

    @list_route(methods=["GET"])
    def updateFromGoogleSheet(self, request, *args, **kwargs):
        return
        google = sheetRequests
        posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        insertBulk = []
        for key in list(google.keys()):
            profileInstance = SalesCustomerProfile.objects.filter(
                Q(hamkaranCode=str(google[key].get('codeHamkaran'))) |
                Q(name__icontains=str(google[key].get('name')))
            )
            if profileInstance.count() == 0:
                prof = dict(
                    positionID=posiIns.positionID,
                    companyID=posiIns.companyID,
                    name=google[key]["name"],
                    hamkaranCode=str(google[key]["codeHamkaran"])
                )
                prof = CustomerProfileSerializer(data=prof)
                prof.is_valid(raise_exception=True)
                prof = prof.save()
                profileInstance = prof
            else:
                profileInstance = profileInstance[0]

            """
            Year
:
1396
arz
:
1
letterID
:
12
month
:
"اردیبهشت"
payType
:
"نقدی"
qty
:
213212
sayType
:
"فوری"
sayseason
:
"تابستان"
temper
:
1
tool
:
1
typeOfAsk
:
"کارشناسی"
zekhamat
:
1
            """

            dt = dict(
                positionID=posiIns.positionID,
                companyID=posiIns.companyID,
                profileLink=str(profileInstance.id),
                desc=dict(
                    qty=google[key].get('qty', 0) * 1000,
                    arz=google[key].get('arz'),
                    zekhamat=google[key].get('zakhamat'),
                    tool=google[key].get('tool'),
                    temper=google[key].get('temper'),
                    letterID=google[key].get('shomarehSabt'),
                    month=None,
                    payType=google[key].get('sharayetePardakht'),
                    sayType=google[key].get('zamaneMasraf'),
                    sayseason=None,
                    typeOfAsk=google[key].get('typeOfAsk'),
                    tarikheSabt=datetime.strptime(sh_to_mil(google[key].get('tarikheSabt').split("T")[0],
                                                            ResultSplitter="-",
                                                            returnSecond=False), "%Y-%m-%d") if google[key].get(
                        'tarikheSabt')
                    else datetime.now())
            )

            scc = CustomerProfileSalesRequestsSizesSerializer(data=dt)
            scc.is_valid(raise_exception=True)
            scc.save()
        return Response({})

    @list_route(methods=["GET"])
    def UN_updateFromGoogleSheet(self, request, *args, **kwargs):
        return
        google = un_sheetRequests
        posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        insertBulk = []
        for key in list(google.keys()):
            profileInstance = SalesCustomerProfile.objects.filter(
                Q(name__icontains=str(google[key].get('customername')))
            )
            if profileInstance.count() == 0:
                prof = dict(
                    positionID=posiIns.positionID,
                    companyID=posiIns.companyID,
                    name=google[key]["customername"],
                )
                prof = CustomerProfileSerializer(data=prof)
                prof.is_valid(raise_exception=True)
                prof = prof.save()
                profileInstance = prof
            else:
                profileInstance = profileInstance[0]

            """
            Year
:
1396
arz
:
1
letterID
:
12
month
:
"اردیبهشت"
payType
:
"نقدی"
qty
:
213212
sayType
:
"فوری"
sayseason
:
"تابستان"
temper
:
1
tool
:
1
typeOfAsk
:
"کارشناسی"
zekhamat
:
1
            """

            dt = dict(
                positionID=posiIns.positionID,
                companyID=posiIns.companyID,
                profileLink=str(profileInstance.id),
                desc=dict(
                    qty=google[key].get('qty', 0) * 1000,
                    arz=google[key].get('arz'),
                    zekhamat=google[key].get('zakhamat'),
                    tool=google[key].get('tool'),
                    temper=google[key].get('temper'),
                    letterID=google[key].get('shomarehSabt'),
                    month=None,
                    payType=google[key].get('sharayetePardakht'),
                    sayType=google[key].get('zamaneMasraf'),
                    sayseason=None,
                    typeOfAsk=google[key].get('typeOfAsk'),
                    tarikheSabt=datetime.strptime(sh_to_mil(google[key].get('tarikheSabt').split("T")[0],
                                                            ResultSplitter="-",
                                                            returnSecond=False), "%Y-%m-%d") if google[key].get(
                        'tarikheSabt')
                    else datetime.now())
            )

            scc = CustomerProfileSalesRequestsSizesSerializer(data=dt)
            scc.is_valid(raise_exception=True)
            scc.save()
        return Response({})

    @list_route(methods=["GET"])
    def createShamsiDate(self, request, *args, **kwargs):
        scp = SalesCustomerProfileSalesRequestsSizes.objects.all()
        for s in scp:
            s.update(set__desc__tarikheSabtShamsi=mil_to_sh(s.desc['tarikheSabt']))
            s.update(
                set__desc__tarikheSabtShamsiDayName=changeDateNameToShamsiDate(s.desc["tarikheSabt"].strftime("%A")))
        return Response({})

    @detail_route(methods=["GET"])
    def dup(self, request, *args, **kwargs):
        reqIns = self.queryset.get(id=kwargs['id'])
        reqIns = self.serializer_class(instance=reqIns).data
        reqIns['profileLink'] = reqIns['profileLink']['id']
        del reqIns['id']
        del reqIns['dateOfPost']
        newSer = self.serializer_class(data=reqIns)
        newSer.is_valid(raise_exception=True)
        newSer.save()
        return Response({})

    @list_route(methods=["GET"])
    def getForDataTables(self, request, *args, **kwargs):
        if request.user.groups.filter(name='foroosh').count() == 0:
            return Response({})
        self.pagination_class = DataTablesPagination
        result = self.list(request, args, kwargs)
        return result

    @list_route(methods=["GET"])
    def downloadExcel(self, request, *args, **kwargs):

        result = SalesCustomerProfileSalesRequestsSizes.objects.all()
        result = CustomerProfileSalesRequestsSizesSerializer(instance=result, many=True).data

        output = io.BytesIO()
        # fileAddr = os.path.join(tmpdir, 'excel.xlsx')

        workbook = xlsxwriter.Workbook(output)

        fontFormat = workbook.add_format({"font_name": "B Nazanin"})
        mySheet = workbook.add_worksheet("DBTable")
        mySheet.is_right_to_left = True

        bold = workbook.add_format({'bold': True, "font_name": "B Nazanin"})
        simple = workbook.add_format({'bold': False, "font_name": "B Nazanin"})

        # worksheet = workbook.add_worksheet()

        row = 0
        col = 0
        """
        نام مشتری	نام مشتری همکاران	ضخامت (mm)	عرض (mm)	طول برش (mm)	میزان (تن)	تمپر	زمان مصرف	شرایط پرداخت	تاریخ ثبت	شماره ثبت
        """

        # first rows
        mySheet.write(0, 0, 'نام مشتری', bold)
        mySheet.write(0, 1, 'ضخامت (mm)', bold)
        mySheet.write(0, 2, 'عرض (mm)', bold)
        mySheet.write(0, 3, 'طول برش (mm)', bold)
        mySheet.write(0, 4, 'میزان (تن)', bold)
        mySheet.write(0, 5, 'تمپر', bold)
        mySheet.write(0, 6, 'زمان مصرف', bold)
        mySheet.write(0, 7, 'شرایط پرداخت', bold)
        mySheet.write(0, 8, 'تاریخ ثبت', bold)
        mySheet.write(0, 9, 'شماره ثبت', bold)

        row = 1
        for r in result:
            ccc = r['desc']
            mySheet.write(row, 0, r['profileLink']['name'], simple)
            mySheet.write(row, 1, ccc.get('zekhamat'), simple)
            mySheet.write(row, 2, ccc.get('arz'), simple)
            mySheet.write(row, 3, ccc.get('tool'), simple)
            mySheet.write(row, 4, ccc.get('qty'), simple)
            mySheet.write(row, 5, ccc.get('temper'), simple)
            mySheet.write(row, 6, ccc.get('sayType'), simple)
            mySheet.write(row, 7, ccc.get('payType'), simple)
            mySheet.write(row, 8, mil_to_sh(ccc.get('tarikheSabt')), simple)
            mySheet.write(row, 9, ccc.get('letterID'), simple)

            row += 1

        workbook.close()

        output.seek(0)

        dt = datetime.now()
        dt = mil_to_sh_with_time(dt).replace("/", "_").replace(" ", "__").replace(":", "_")

        from django.http import HttpResponse
        response = HttpResponse(output,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=%s' % (dt + ".xlsx")

        # self.pagination_class = DataTablesPagination
        # result = self.list(request, args, kwargs)
        return response

    def initial(self, request, *args, **kwargs):
        if request.method != "GET" and request.method != "DELETE":
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            request.data["positionID"] = posiIns.positionID
            request.data["companyID"] = posiIns.companyID
        return super(SalesCustomerProfileSalesRequestsSizesViewSet, self).initial(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        result = super(SalesCustomerProfileSalesRequestsSizesViewSet, self).list(request, *args, **kwargs)
        ress = result.data.get("results") if result.data.get("results") else result.data.get("aaData")
        for d in ress:
            positionDoc = PositionsDocument.objects.filter(
                positionID=d["positionID"],
                companyID=request.user.current_company_id, )
            d["desc"]["zekhamat"] = d["desc"].get("zekhamat", 0)
            d["desc"]["arz"] = d["desc"].get("arz", 0)
            d["desc"]["tool"] = d["desc"].get("tool", 0)
            d["desc"]["temper"] = d["desc"].get("temper", 0)
            d["desc"]["sayType"] = d["desc"].get("sayType", "")
            d["desc"]["payType"] = d["desc"].get("payType", "")
            d["desc"]["letterID"] = d["desc"].get("letterID", "")
            d["desc"]["qty"] = d["desc"].get("qty", 0)
            d["dateOfPost"] = mil_to_sh(d["dateOfPost"])
            d["desc"]["tarikheSabt"] = mil_to_sh(d["desc"]["tarikheSabt"])

            if positionDoc.count() != 0:
                positionDoc = positionDoc[0]
                profileInstance = Profile.objects.get(userID=positionDoc.userID)
                d["positionName"] = positionDoc.profileName
                d["positionSemat"] = positionDoc.chartName
                d["avatar"] = profileInstance.extra["profileAvatar"]["url"]
            else:
                d["positionName"] = "حذف شده"
                d["positionSemat"] = "حذف شده"
                d["avatar"] = "/static/images/avatar_empty.jpg"
        return result

    # def template_view_base(self, request):
    #     return render_to_response('Sales/Profile/add.html', {}, context_instance=RequestContext(request))

    @list_route(methods=["GET"])
    def getTop10(self, request, *args, **kwargs):
        days = []
        daynames = []
        for d in range(0, 15):
            now = datetime.now() - timedelta(days=d)
            if not now.strftime("%A") in ['Friday', 'Thursday']:
                days.append(dict(
                    dayName=changeDateNameToShamsiDate(now.strftime("%A")),
                    day=now
                ))
                daynames.append(changeDateNameToShamsiDate(now.strftime("%A")))
        qr = list(SalesCustomerProfileSalesRequestsSizes.objects.filter(
            desc__tarikheSabt__gt=datetime.now() - timedelta(days=10),
            desc__tarikheSabt__lt=datetime.now()
        ).aggregate({
            '$lookup': {
                'from': 'sales_customer_profile',
                'localField': 'profileLink',
                'foreignField': '_id',
                'as': 'profile'
            }}, {
            '$group': {
                "_id": {"tarikheSabt": "$desc.tarikheSabt"},
                "count": {"$sum": 1},
                "sumOfQty": {"$sum": "$desc.qty"},
                "details": {"$addToSet": {"companyNames": "$profile.name", "zekhamat": "$desc.zekhamat"}}
            }
        }
        ))
        daynames = []
        for q in qr:
            q["dateOfMil"] = q["_id"]["tarikheSabt"]
            q["dateOfSh"] = mil_to_sh(q["_id"]["tarikheSabt"])
            q['dateStr'] = changeDateNameToShamsiDate(q["_id"]["tarikheSabt"].strftime("%A"))
            daynames.append(q['dateStr'])

        return Response(
            dict(
                daynames=daynames,
                details=qr))
