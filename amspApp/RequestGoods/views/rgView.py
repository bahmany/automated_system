from datetime import datetime

from django.contrib.auth.models import Group
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets
from mongoengine import Q

from amspApp.CompaniesManagment.Charts.models import Chart
from amspApp.CompaniesManagment.Connections.models import ConnectionPools, Connections
from amspApp.CompaniesManagment.Connections.viewes.ConnectionsViews import ConnectionsViewSet
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.Positions.serializers.PositionSerializer import PositionDocumentSerializer
from amspApp.Infrustructures.Classes.DateConvertors import is_valid_shamsi_date, sh_to_mil, getCurrentYearShamsi2digit
from amspApp.RequestGoods.models import RequestGood, RequestGoodSigns
from amspApp.RequestGoods.serializers.rgSerializers import RequestGoodSerializer, RequestGoodItemsHamkaranSerializer, \
    RequestGoodSignsSerializer
from amspApp.RequestGoods.views import rg_process
from amspApp.Sales.views.ExitsView import ExitsViewSet
from amspApp._Share.ListPagination import DetailsPagination
from amspApp.amspUser.views.UserView import UserViewSet
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset
from amspApp.RequestGoods.models import RequestGoodItemsHamkaran
import itertools
import re
from asq.initiators import query


class RequestGoodViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = RequestGood.objects.all().order_by("-id")
    serializer_class = RequestGoodSerializer
    pagination_class = DetailsPagination
    pagination_class.page_size = 50

    """
    -9  = moteghazi
    -10 = raeese moteghazi
    -11 = modire vahed
    -12 = sarparaste vahed
    
    flattening list 
    list(itertools.chain.from_iterable([x for x in query(self.process).select(lambda x:x['sargroup_kala'])])) 
    """

    process = rg_process.process

    def initial(self, request, *args, **kwargs):
        if request.method != "GET" and request.method != "DELETE":
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            request.data["positionID"] = posiIns.positionID
        return super(RequestGoodViewSet, self).initial(request, *args, **kwargs)

    @detail_route(methods=["GET"])
    def requesterGetThis(self, request, *args, **kwargs):
        currentPosition = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        instanceOf = self.queryset.get(id=kwargs.get("id"))
        groupsOf = request.user.groups.filter(name="group_anbar").count()
        if groupsOf < 1:
            return Response({'errcode': 2, 'msg': 'شما مجاز به تایید نیستید'})
        # checking if sign before
        exp = instanceOf.exp
        if exp.get('get_this'):
            return Response({'errcode': 2, 'msg': 'قبلا این گزینه امضا شده است'})
        if exp.get('send_tamin'):
            return Response({'errcode': 2, 'msg': 'قبلا این گزینه امضا شده است'})
        exp['get_this'] = True
        exp['get_this_positionID'] = currentPosition.positionID
        exp['get_this_date'] = datetime.now()
        exp['get_this_type'] = 1  # 1 means directly after request
        gins = RequestGoodSerializer(instance=instanceOf, data={"exp": exp}, partial=True)
        gins.is_valid(raise_exception=True)
        gins.save()
        exp['signStepID'] = 9
        exp['moteghaziPositionID'] = instanceOf.positionID
        self.sendNotif(exp)
        return Response(gins.data)

    @detail_route(methods=["GET"])
    def getMojoodi(self, request, *args, **kwargs):
        # currentPosition = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        pool = ConnectionPools.objects.get(name="AccGetCurrentMojoodi")
        sql = pool.sqls[0]["code"]
        sql = sql.replace("<:Year:>", getCurrentYearShamsi2digit())
        sql = sql.replace("<:PartRef:>", kwargs['id'])
        connection = Connections.objects.get(databaseName="sgdb")
        connection = ConnectionsViewSet().getConnection(connection)
        connection.execute(sql)
        sql_res = connection.fetchall()
        sql_res[0]['sumQty'] = sql_res[0]['sumQty'] if sql_res[0]['sumQty'] != None else 0
        sql_res[0]['sumQty'] = str(sql_res[0]['sumQty'])
        return Response(sql_res[0])

    @detail_route(methods=["POST"])
    def taminAcceptedDates(self, request, *args, **kwargs):
        currentPosition = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        instanceOf = self.queryset.get(id=kwargs.get("id"))
        groupsOf = request.user.groups.filter(name="group_tamin").count()
        if groupsOf < 1:
            return Response({'errcode': 2, 'msg': 'شما مجاز به تایید نیستید'})
        # checking if sign before
        exp = instanceOf.exp
        if exp.get('tamin_accepted'):
            return Response({'errcode': 2, 'msg': 'قبلا این گزینه امضا شده است'})
        exp['tamin_accepted'] = True
        exp['tamin_accepted_positionID'] = currentPosition.positionID
        exp['tamin_accepted_date'] = datetime.now()
        exp['tamin_accepted_type'] = 1  # 1 means directly after request
        exp['date_end'] = request.data.get('date_end')
        exp['ordering_date'] = request.data.get('ordering_date')
        exp['schedule_date'] = request.data.get('schedule_date')
        if not is_valid_shamsi_date(exp['date_end']):
            return Response({'errcode': 2, 'msg': 'لطفا تاریخ را صحیح وارد نمایید'})
        if not is_valid_shamsi_date(exp['ordering_date']):
            return Response({'errcode': 2, 'msg': 'لطفا تاریخ را صحیح وارد نمایید'})
        if not is_valid_shamsi_date(exp['schedule_date']):
            return Response({'errcode': 2, 'msg': 'لطفا تاریخ را صحیح وارد نمایید'})
        exp['date_end_mil'] = datetime.strptime(sh_to_mil(exp['date_end']), "%Y/%m/%d")
        exp['ordering_date_mil'] = datetime.strptime(sh_to_mil(exp['ordering_date']), "%Y/%m/%d")
        exp['schedule_date_mil'] = datetime.strptime(sh_to_mil(exp['schedule_date']), "%Y/%m/%d")

        gins = RequestGoodSerializer(instance=instanceOf, data={"exp": exp}, partial=True)
        gins.is_valid(raise_exception=True)
        gins.save()
        exp['signStepID'] = 11
        exp['moteghaziPositionID'] = instanceOf.positionID
        self.sendNotif(exp)

        return Response(gins.data)

    @detail_route(methods=["POST"])
    def uploadDarkhastKharid(self, request, *args, **kwargs):
        currentPosition = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        instanceOf = self.queryset.get(id=kwargs.get("id"))
        groupsOf = request.user.groups.filter(name="group_tamin").count()
        if groupsOf < 1:
            return Response({'errcode': 2, 'msg': 'شما مجاز به تایید نیستید'})
        # checking if sign before
        exp = instanceOf.exp
        if exp.get('havaleh_froosh_file'):
            return Response({'errcode': 2, 'msg': 'قبلا این گزینه امضا شده است'})
        exp = request.data
        if exp.get("havaleh_foroosh_file") == None:
            return Response({'errcode': 2, 'msg': 'عکسی آپلود نشده است'})

        exp['havaleh_froosh_file_finished'] = True
        exp['havaleh_froosh_file_positionID'] = currentPosition.positionID
        exp['havaleh_froosh_file_date'] = datetime.now()
        exp['havaleh_froosh_file_type'] = 1  # 1 means directly after request

        gins = RequestGoodSerializer(instance=instanceOf, data={"exp": exp}, partial=True)
        gins.is_valid(raise_exception=True)
        gins.save()
        exp['signStepID'] = 12
        exp['moteghaziPositionID'] = instanceOf.positionID
        self.sendNotif(exp)

        return Response(gins.data)

    @detail_route(methods=["GET"])
    def thisMustTamin(self, request, *args, **kwargs):
        currentPosition = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        instanceOf = self.queryset.get(id=kwargs.get("id"))
        groupsOf = request.user.groups.filter(name="group_anbar").count()
        if groupsOf < 1:
            return Response({'errcode': 2, 'msg': 'شما مجاز به تایید نیستید'})

        # checking if sign before

        exp = instanceOf.exp

        if exp.get('get_this'):
            return Response({'errcode': 2, 'msg': 'قبلا این گزینه امضا شده است'})
        if exp.get('send_tamin'):
            return Response({'errcode': 2, 'msg': 'قبلا این گزینه امضا شده است'})

        exp['send_tamin'] = True
        exp['send_tamin_positionID'] = currentPosition.positionID
        exp['send_tamin_date'] = datetime.now()
        exp['send_tamin_type'] = 1  # 1 means directly after request
        gins = RequestGoodSerializer(instance=instanceOf, data={"exp": exp}, partial=True)
        gins.is_valid(raise_exception=True)
        gins.save()
        exp['signStepID'] = 10
        exp['moteghaziPositionID'] = instanceOf.positionID
        exp['inst'] = instanceOf
        self.sendNotif(exp)
        return Response(gins.data)

    @list_route(methods=["GET"])
    def goodsRefresh(self, request, *args, **kwargs):
        pool = ConnectionPools.objects.get(name="Acc_vwGroupPart")
        sql = pool.sqls[0]["code"]
        connection = Connections.objects.get(databaseName="sgdb")
        connection = ConnectionsViewSet().getConnection(connection)
        connection.execute(sql)
        sql_res = connection.fetchall()
        dt = []
        for d in sql_res:
            dt.append({
                "dateOfPost": datetime.now(),
                "exp": d

            })
        ex = ExitsViewSet()
        for d in dt:
            d["exp"]["Title"] = ex.fixChar(d["exp"]["Title"])
            d["exp"]["PartName"] = ex.fixChar(d["exp"]["PartName"])
            d["exp"]["UnitName"] = ex.fixChar(d["exp"]["UnitName"])

        for d in dt:
            ccnt = RequestGoodItemsHamkaran.objects.filter(exp__PartCode=ex.fixChar(d["exp"]["PartCode"]))
            if ccnt.count() == 0:
                ser = RequestGoodItemsHamkaranSerializer(data=d)
                ser.is_valid(raise_exception=True)
                ser.save()
            else:
                ser = RequestGoodItemsHamkaranSerializer(instance=ccnt.first(), data=d, partial=True)
                ser.is_valid(raise_exception=True)
                ser.save()

        return Response({})

    @list_route(methods=["POST"])
    def postDraftFirstStep(self, request, *args, **kwargs):
        currentPosition = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        dateOfPost = datetime.now()
        rgType = request.data.get("selectedItem")
        requestItems = request.data.get("requestItems")
        id = request.data.get("id")
        # it means it is new instance
        if id == "1":
            dt = {
                'positionID': currentPosition.positionID,
                'dateOfPost': dateOfPost,
                'rgPriority': 2,
                'rgType': rgType,
                'draft': True,
                'exp': {
                    'requestItems': requestItems
                },
            }
            ins = RequestGoodSerializer(data=dt)
            ins.is_valid(raise_exception=True)
            ins.save()
            return Response(ins.data)

        dt = {
            'positionID': currentPosition.positionID,
            'dateOfPost': dateOfPost,
            'rgPriority': 2,
            'rgType': rgType,
            'draft': True,
            'exp': {
                'requestItems': requestItems
            },
        }
        ins = RequestGood.objects.get(id=id)
        ins = RequestGoodSerializer(instance=ins, data=dt, partial=True)
        ins.is_valid(raise_exception=True)
        ins.save()
        return Response(ins.data)

    @list_route(methods=["POST"])
    def postStartFirstStep(self, request, *args, **kwargs):

        # checking validation
        allForm = request.data
        if allForm.get("selectedItem") not in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
            return Response(
                {'errcode': 2, 'msg': 'لطفا یکی از گروه های کالایی را انتخاب نمایید'}
            )

        requests = allForm['requestItems']
        for r in requests:
            if r.get("exp") == None:
                return Response({"errcode": 2, "msg": "لطفا اطلاعات خواسته شده در قسمت انتخاب کالا را تکمیل کنید"})
            if r.get("exp").get("selectedItem") is None:
                return Response({"errcode": 2, "msg": "لطفا اطلاعات خواسته شده در قسمت انتخاب کالا را تکمیل کنید"})
            if r.get("mizan") is None:
                return Response({"errcode": 2, "msg": "لطفا اطلاعات خواسته شده در قسمت انتخاب کالا را تکمیل کنید"})
            if r.get("tarikhe_niaz") is None:
                return Response({"errcode": 2, "msg": "لطفا اطلاعات خواسته شده در قسمت انتخاب کالا را تکمیل کنید"})
            if is_valid_shamsi_date(r.get("tarikhe_niaz")) == False:
                return Response({"errcode": 2, "msg": "لطفا در ورود تاریخ های نیاز دقت نمایید"})

        currentPosition = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        # checking if starter is allowed to start or not
        reqTable = query(self.listOfRequest(request, *args, **kwargs).data['flat']).where(
            lambda x: x['value'] == request.data.get("selectedItem")).first()

        starter = reqTable['runners']['request'][0]['positions'][0]
        if starter['chartID'] != currentPosition.chartID:
            return Response({"errcode": 2, "msg": "شما مجاز به اعلام این درخواست نیستید"})

        dateOfPost = datetime.now()
        rgType = request.data.get("selectedItem")
        requestItems = request.data.get("requestItems")
        id = request.data.get("id")
        # it means it is new instance
        if id == "1":
            dt = {
                'positionID': currentPosition.positionID,
                'dateOfPost': dateOfPost,
                'rgPriority': 2,
                'rgType': rgType,
                'draft': False,
                'exp': {
                    'requestItems': requestItems
                },
            }
            ins = RequestGoodSerializer(data=dt)
            ins.is_valid(raise_exception=True)
            ins.save()
            return Response(ins.data)

        dt = {
            'positionID': currentPosition.positionID,
            'dateOfPost': dateOfPost,
            'rgPriority': 2,
            'rgType': rgType,
            'draft': False,
            'exp': {
                'requestItems': requestItems
            },
        }
        ins = RequestGood.objects.get(id=id)
        ins = RequestGoodSerializer(instance=ins, data=dt, partial=True)
        ins.is_valid(raise_exception=True)
        ins.save()
        return Response(ins.data)

    @list_route(methods=["POST"])
    def signDarkhast(self, request, *args, **kwargs):

        signPass = request.data.get('signpass')
        uvs = UserViewSet()
        signPassIsOK = uvs.checkUserSignPass(request.user, signPass)

        if not signPassIsOK:
            return Response({'errcode': 2, 'msg': 'رمز دوم اشتباه است'})

        current_signer = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        current_signer_chart_id = current_signer.chartID
        ins = RequestGood.objects.get(id=request.data.get("idof"))
        signStepID = request.data.get("stepID")
        tableOfSigns = self.listOfRequest(request, *args, **kwargs).data.get("flat")
        signers = query(tableOfSigns).where(lambda x: x['value'] == ins.rgType).first()['runners']
        """
        1 = request
        2 = confirm
        3 = approve
        """
        if signStepID == 1:
            signerChartID = signers['request'][0]['positions'][0]['chartID']
            if current_signer_chart_id != signerChartID:
                return Response({"errcode": 3, "msg": "شما مجاز به امضا زدن نیستید"})

        if signStepID == 2:
            signerChartID = signers['confirm'][0]['positions'][0]['chartID']
            if current_signer_chart_id != signerChartID:
                return Response({"errcode": 3, "msg": "شما مجاز به امضا زدن نیستید"})
        if signStepID == 3:
            signerChartID = signers['approve'][0]['positions'][0]['chartID']
            if current_signer_chart_id != signerChartID:
                return Response({"errcode": 3, "msg": "شما مجاز به امضا زدن نیستید"})

        # checking for duplicated signs to prevent
        dps_count = RequestGoodSigns.objects.filter(
            Q(requestGoodLink=str(ins.id)) &
            Q(positionID=current_signer.positionID) &
            Q(signStepID=signStepID)
        ).count()

        if dps_count > 0:
            return Response({"errcode": 4, "msg": "قبلا امضا زده اید"})

        signing = {
            "requestGoodLink": str(ins.id),
            "positionID": current_signer.positionID,
            "dateOfPost": datetime.now(),
            "signStepID": signStepID,
            "comment": request.data.get("comment", "")
        }

        if signStepID == 3:
            rq = RequestGood.objects.get(id=str(ins.id))
            exp = rq.exp
            exp['has_three_sign'] = True
            rqs = RequestGoodSerializer(instance=rq, data={"exp": exp}, partial=True)
            rqs.is_valid(raise_exception=True)
            rqs.save()

        ss = RequestGoodSignsSerializer(data=signing)
        ss.is_valid(raise_exception=True)

        listOfRequestsType = self.listOfRequest(request, args, kwargs)
        currentLow = query(listOfRequestsType.data['flat']).where(lambda x:x['value'] == ss.data['requestGoodLink']['rgType']).first_or_default(None)
        ss = ss.save()
        ss = RequestGoodSignsSerializer(instance=ss).data
        ss['selected_details'] = currentLow
        ss = self.handleCurrent(ss)
        self.sendNotif(ss)
        return Response(ss)

    def sendNotif(self, ss):
        # group_anbar     group_tamin
        a = 1
        msg = ""
        reciversUserID = []
        requester_ins = PositionsDocument.objects.filter(positionID=ss['requestGoodLink']['positionID'],
                                                         userID__ne=None, chartID__ne=None).first()
        if ss['signStepID'] == 1: # confirm
            msg = """بعنوان تایید کننده همکنون برگه درخواستی که توسط %s تنظیم شده منتظر تایید شماست""" % (requester_ins.profileName,)
            chartID = ss['selected_details']['runners']['confirm'][0]['positions'][0]['chartID']
            positions = PositionsDocument.objects.filter(chartID = chartID, userID__ne = None, positionID = ss['positionID'])
            reciversUserID = [p.userID for p in positions]

        if ss['signStepID'] == 2: # approve
            msg = """درخواست تنظیم شده توسط %s جهت تصویت همکنون منتظر تایید شماست""" % (requester_ins.profileName,)
            chartID = ss['selected_details']['runners']['approve'][0]['positions'][0]['chartID']
            positions = PositionsDocument.objects.filter(chartID = chartID, userID__ne = None, positionID = ss['positionID'])
            reciversUserID = [p.userID for p in positions]


        if ss['signStepID'] == 9: # moteghazi get this from anbar
            msg = """کالای درخواستی به متقاضی تحویل داده شد"""
            positionIns = PositionsDocument.objects.filter(positionID = ss['moteghaziPositionID'], userID__ne = None).first()
            reciversUserID = [positionIns.userID]
        if ss['signStepID'] == 10: # moteghazi get this from anbar
            msg = """تقاضای مورد نظر توسط انبار به تامین ارجا داده شد"""
            positionIns = PositionsDocument.objects.filter(positionID = ss['moteghaziPositionID'], userID__ne = None).first()
            reciversUserID = [positionIns.userID]
        if ss['signStepID'] == 11: # moteghazi get this from anbar
            msg = """توافق حاصل شده برای تاریخ تامین توسط واحد بازرگانی ثبت گردید"""
            positionIns = PositionsDocument.objects.filter(positionID = ss['moteghaziPositionID'], userID__ne = None).first()
            reciversUserID = [positionIns.userID]
        if ss['signStepID'] == 12: # moteghazi get this from anbar
            msg = """برگه درخواست خرید کالا توسط انبار به واحد تامین ارسال شد"""
            positionIns = PositionsDocument.objects.filter(positionID = ss['moteghaziPositionID'], userID__ne = None).first()
            reciversUserID = [positionIns.userID]

        dt = {
            'type': 8,
            'typeOfAlarm': 3,
            'informType': 8,
            'userID': reciversUserID,
        }
        pass

    @list_route(methods=["GET"])
    def listOfRequest(self, request, *args, **kwargs):
        res = query(list(itertools.chain.from_iterable(
            [x for x in query(self.process).select(lambda x: x['sargroup_kala'])]))).order_by(
            lambda x: x['value']).to_list()
        """
    -9  = moteghazi
    -10 = raeese moteghazi
    -11 = modire vahed
    -12 = sarparaste vahed
    
    در چارت ****ی
    modirha = 15
    raees = 14
    sarparast = 13 
    
        """

        def getPositionsDoc(request, chartIDs):
            for chartID in chartIDs:
                if not chartID in [-9, -10, -11, -12]:
                    poss = list(PositionsDocument.objects.filter(chartID=chartID, positionID__ne=None, userID__ne=None))
                    poss = PositionDocumentSerializer(instance=poss, many=True).data
                    poss = list(PositionDocumentSerializer(instance=poss, many=True).data)
                    return poss
                if chartID == -9:
                    poss = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
                    poss = PositionDocumentSerializer(instance=poss).data
                    return [poss]

                # getting top chart
                poss = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
                currentChart = poss.chartID

                def getTopChart(currentChart, poss):
                    cu = Chart.objects.get(id=currentChart)
                    cpl = list(PositionsDocument.objects.filter(chartID=cu.id, positionID__ne=None, userID__ne=None))
                    cpl = list(PositionDocumentSerializer(instance=cpl, many=True).data)
                    poss.append(cpl)
                    if cu.top == None:
                        return poss
                    cp = Chart.objects.get(id=cu.top.id)
                    return getTopChart(cp.id, poss)

                ress = getTopChart(currentChart, [])
                ress = query(ress).where(lambda x: len(x) > 0).to_list()
                ress = query(ress).where(lambda x: len(x) > 0).select(lambda x: x[0]).to_list()
                for r in ress:
                    r['rank'] = Chart.objects.get(id=r['chartID']).rank
                ress = query(ress).order_by(lambda x: x['rank']).to_list()

                """
                یعنی وقتی نوبت به امضای سرپرست واحد رسیده باشه
                در اینجا کلی مسئله هست
                 = 13   

                """

                if chartID == -12:
                    pers = query(ress).where(lambda x: x['rank'] == 13).first_or_default(None)
                    if pers is not None:
                        return [pers]

                    pers = query(ress).where(lambda x: x['rank'] > 13).first_or_default(None)
                    if pers is not None:
                        return [pers]

                    if pers is None:
                        return [GetPositionViewset().GetCurrentPositionDocumentInstance(request)]

                """
                = 14
                """

                if chartID == -10:
                    pers = query(ress).where(lambda x: x['rank'] == 14).first_or_default(None)
                    if pers is not None:
                        return [pers]

                    pers = query(ress).where(lambda x: x['rank'] > 14).first_or_default(None)
                    if pers is not None:
                        return [pers]

                    if pers is None:
                        return [GetPositionViewset().GetCurrentPositionDocumentInstance(request)]
                """
                =15
                """

                if chartID == -11:
                    pers = query(ress).where(lambda x: x['rank'] == 15).first_or_default(None)
                    if pers is not None:
                        return [pers]

                    pers = query(ress).where(lambda x: x['rank'] > 15).first_or_default(None)
                    if pers is not None:
                        return [pers]

                    if pers is None:
                        return [GetPositionViewset().GetCurrentPositionDocumentInstance(request)]

        for pr in self.process:
            for p in pr['sargroup_kala']:
                for key in list(p['runners'].keys()):
                    for rrr in p['runners'][key]:
                        rrr["positions"] = getPositionsDoc(request, rrr['chartIDs'])
        ss = []
        fl = [x['sargroup_kala'] for x in self.process]
        for f in fl:
            for ff in f:
                ss.append(ff)

        flat = ss
        newflat = []

        def addToFlat(aa, newFlatter, mode, value):
            for aaa in aa['positions']:
                newFlatter.append(
                    {
                        "positionID": aaa['positionID'],
                        "chartID": aaa['chartID'],
                        "userID": aaa['userID'],
                        "radeef": a['value'],
                        "mode": mode,
                        "value": value,
                    }
                )
            return newFlatter

        for a in flat:
            for aa in a['runners']['request']:
                newflat = addToFlat(aa, newflat, 'request', a['value'])
            for aa in a['runners']['confirm']:
                newflat = addToFlat(aa, newflat, 'confirm', a['value'])
            for aa in a['runners']['approve']:
                newflat = addToFlat(aa, newflat, 'approve', a['value'])

        return Response({"s": self.process, "flat": ss, "flat_list": newflat})

    def sendRGNotification(self, rgInstance, defname):
        pass

    def retrieve(self, request, *args, **kwargs):
        result = super(RequestGoodViewSet, self).retrieve(request, *args, **kwargs)
        signs = RequestGoodSigns.objects.filter(requestGoodLink=result.data['id'])
        result.data['signs'] = RequestGoodSignsSerializer(instance=signs, many=True).data
        return result

    def list(self, request, *args, **kwargs):
        # getting list of request signers table
        poss = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        request_signs = self.listOfRequest(request, *args, **kwargs)
        flat_list = request_signs.data['flat_list']
        # -----------------------------
        # getting params
        not_finished = request.query_params.get("nf")
        has_roll = request.query_params.get("hr")
        archive = request.query_params.get("a")
        search = request.query_params.get("s")
        not_finished = True if not_finished == "true" else False
        has_roll = True if has_roll == "true" else False
        archive = True if archive == "true" else False
        # getting current user signs in three mode
        # request    confirm   approve
        approveIDs = query(flat_list).where(
            lambda x: (x['chartID'] == poss.chartID) and (x['mode'] in ['confirm', ['approve']])).to_list()
        approveValues = query(approveIDs).select(lambda x: x['value']).to_list()

        qs = Q(positionID=poss.positionID)
        ps = Q()
        if not_finished:
            ps = ps | Q(exp__finished=False)
        if archive:
            ps = ps | Q(exp__finished=True)
        if has_roll:
            ps = ps | Q(rgType__in=approveValues)
        qq = qs | ps

        self.queryset = self.queryset.filter(qq)
        result = super(RequestGoodViewSet, self).list(request, *args, **kwargs)
        for r in result.data['results']:
            r['summ'] = ""
            if r.get('exp'):
                if r.get('exp').get('requestItems'):
                    for rr in r.get('exp').get('requestItems'):
                        if rr.get('exp'):
                            rr = rr.get("exp")
                            if rr.get("selectedItem"):
                                rr = rr.get("selectedItem")
                                if rr.get("item"):
                                    if r["summ"] != "":
                                        r["summ"] = r["summ"] + " - " + rr['item']["PartName"]
                                    else:
                                        r["summ"] = rr['item']["PartName"]
            pd = PositionsDocument.objects.filter(positionID=r['positionID']).first()
            r['profileName'] = pd.profileName
            r['chartName'] = pd.chartName
            r['avatar'] = pd.avatar
            r['signs'] = RequestGoodSignsSerializer(instance=RequestGoodSigns.objects.filter(requestGoodLink=r['id']),
                                                    many=True).data
            r['selected_details'] = query(request_signs.data['flat']).where(
                lambda x: x['value'] == r['rgType']).first_or_default(None)
            # calculating current sign
            currentPerson = {}
            r = self.handleCurrent(r)

        return result

    @list_route(methods=["GET"])
    def goodsHamkaranList(self, request, *args, **kwargs):
        self.listOfRequest(request, *args, **kwargs)
        str = request.query_params.get("q")
        res = list(
            RequestGoodItemsHamkaran.objects.filter(
                # Q(exp__Title__contains=str) |
                Q(exp__PartName__contains=str) |
                Q(exp__PartCode__contains=str)
            ).aggregate({
                "$group": {
                    "_id": "$exp.Parent",
                    "Title": {"$first": "$exp.Title"},
                    "result": {"$push": {"item": "$exp"}},

                },

            }, {"$project": {
                "_id": 1,
                "Title": 1,
                "result": {"$slice": ["$result", 15]}
            }})
        )

        return Response(res)

    def handleCurrent(self, r):
        signs = RequestGoodSigns.objects.filter(requestGoodLink=r['id'])
        if r['selected_details']:
            if signs.count() == 0:
                poss = r['selected_details']['runners']['request'][0]['positions'][0]
                r['currentPositionToConfirm'] = poss['chartName']
                r['currentChartIDToConfirm'] = poss['chartID']
                r['currentPositionToConfirmID'] = 1
            if signs.count() == 1:
                poss = r['selected_details']['runners']['request'][0]['positions'][0]
                r['currentPositionToConfirm'] = poss['chartName']
                r['currentChartIDToConfirm'] = poss['chartID']
                r['currentPositionToConfirmID'] = 2
            if signs.count() == 2:
                poss = r['selected_details']['runners']['request'][0]['positions'][0]
                r['currentPositionToConfirm'] = poss['chartName']
                r['currentChartIDToConfirm'] = poss['chartID']
                r['currentPositionToConfirmID'] = 3
            if signs.count() == 3:
                r['currentPositionToConfirm'] = 'اعلام وضعیت توسط انبار'
                r['currentPositionToConfirmID'] = 4
            if r['exp'].get('send_tamin'):
                if r['exp'].get('send_tamin') == True:
                    r['currentPositionToConfirm'] = 'منتظر نظر تامین'
                    r['currentPositionToConfirmID'] = 5
            if r['exp'].get('get_this'):
                if r['exp'].get('get_this') == True:
                    r['currentPositionToConfirm'] = 'دریافت شده توسط متقاضی'
                    r['currentPositionToConfirmID'] = 6
            if r['exp'].get('tamin_accepted'):
                if r['exp'].get('tamin_accepted') == True:
                    r['currentPositionToConfirm'] = 'منتظر آپلود برگه درخواست خرید توسط انبار'
                    r['currentPositionToConfirmID'] = 7
            if r['exp'].get('havaleh_froosh_file_finished'):
                if r['exp'].get('havaleh_froosh_file_finished') == True:
                    r['currentPositionToConfirm'] = 'تامین در واحد بازرگانی'
                    r['currentPositionToConfirmID'] = 8
        return r

    def sendNotification(self, r):
        pass
