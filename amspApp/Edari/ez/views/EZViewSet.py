import json
from datetime import datetime, timedelta
from urllib.parse import urlencode

import bs4
from asq.initiators import query
from httplib2 import Http
from mongoengine import Q
from rest_framework import status
from rest_framework.decorators import list_route, detail_route
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.CompaniesManagment.Charts.models import Chart
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.Positions.serializers.PositionSerializer import PositionDocumentLessDataSerializer
from amspApp.Infrustructures.Classes.DateConvertors import sh_to_mil, mil_to_sh
from amspApp._Share.ListPagination import DataTableForNewDatables_net
from amspApp.amspUser.models import MyUser
from amspApp.Edari.ez.models import Ez
from amspApp.Edari.ez.serializers.EzSerializer import EzSerializer
from amspApp.Edari.hz.views.HZViewSet import HZViewSet
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class EZViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Ez.objects.all().order_by('-id')
    serializer_class = EzSerializer
    pagination_class = DataTableForNewDatables_net

    dtcols = [
        {'type': "string", 'data': 'status', 'title': 'وضعیت'},
        {'type': "string", 'data': 'tarikheAnjam', 'title': 'تاریخ انجام'},
        {'type': "string", 'data': 'JahateAnjameh', 'title': 'جهت'},
        {'type': "string", 'data': 'typeOf', 'title': 'نوع'},

    ]

    pagination_class.dtcols = dtcols

    def destroy(self, request, *args, **kwargs):
        posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        instance = self.queryset.get(id=kwargs.get('id'))
        if instance.typeOf == 1:
            return Response({"message": "فقط درفت ها قابلیت حذف دارند"}, status=status.HTTP_400_BAD_REQUEST)

        if posiIns.userID != request.user.id:
            return Response({"message": "مجوز حذف این خط را ندارید"}, status=status.HTTP_400_BAD_REQUEST)
        result = super(EZViewSet, self).destroy(request, *args, **kwargs)
        return result

    @list_route(methods=["get"])
    def getDatatableCols(self, request, *args, **kwargs):
        return Response(self.dtcols)

    @list_route(methods=['get'])
    def getPersonelList(self, request, *args, **kwargs):
        posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        chartID = posiIns.chartID
        personnelInMyChart = []
        personnelInMyChart.append(chartID)

        def allChartDetect(__chartID):
            cs = Chart.objects.filter(top=__chartID)
            for c in cs:
                personnelInMyChart.append(c.id)
                allChartDetect(c.id)

        allChartDetect(chartID)
        personnelInMyChart = query(personnelInMyChart).distinct(lambda x: x).to_list()
        # charts = Chart.objects.filter(id__in=personnelInMyChart)
        positions = PositionsDocument.objects.filter(chartID__in=personnelInMyChart, userID__ne=None)
        poss = PositionDocumentLessDataSerializer(instance=positions, many=True).data
        # userIds = query(poss).select(lambda x:x['userID']).to_list()
        # userInst = MyUser.objects.filter(id__in = userIds)
        for p in poss:
            userInds = MyUser.objects.get(id=p["userID"])
            p["personnel_code"] = userInds.personnel_code
            if p["personnel_code"] == "0":
                p["personnel_code"] = None

        return Response(poss)

    def list(self, request, *args, **kwargs):
        q1 = Q(positionID=GetPositionViewset().GetCurrentPositionDocumentInstance(request).positionID)

        q2 = Q(desc__approvers__pos_masoole_edari__userID=request.user.id)
        q3 = Q(desc__approvers__pos_modire_mali__userID=request.user.id)
        q4 = Q(desc__approvers__pos_modire_vahede_darkhat__userID=request.user.id)
        q5 = Q(desc__approvers__pos_modire_vahede_darkhat_after_sign__userID=request.user.id)
        q6 = Q(desc__approvers__pos_vahede_darkhat__userID=request.user.id)
        q7 = Q(desc__approvers__pos_vahede_darkhat_after_sign__userID=request.user.id)

        q_total = q1 | q2 | q3 | q4 | q5 | q6 | q7

        qq1 = Q(typeOf=1) if request.query_params['draftha'] == 'true' else Q()
        qq2 = Q(typeOf=2) & Q(desc__commit__ne=True) if request.query_params['taeed_nashodeha'] == 'true' else Q()
        qq3 = Q(desc__commit=True) if request.query_params['taeed_shodeha'] == 'true' else Q()
        q_total = q_total & (qq1 | qq2 | qq3)
        self.queryset = self.queryset.filter(q_total)
        result = super(EZViewSet, self).list(request, *args, **kwargs)
        for r in result.data['data']:
            can_convert_to_draft = True
            r["typeOf"] = "درفت" if r["typeOf"] == 1 else "فرآیند"
            if r["desc"].get("commit", False) == True:
                r["typeOf"] = "پایان"
            status = "تایید شده"
            if r.get("desc", {}).get("approvers", {}).get("pos_modire_mali", {}).get("approved",
                                                                                     False) == False and r.get("desc",
                                                                                                               {}).get(
                "approvers", {}).get("pos_masoole_edari", {}).get("approved", False) == False:
                status = "منظر امضای تایید کننده"

            if r.get("desc", {}).get("approvers", {}).get("pos_modire_vahede_darkhat_after_sign", {}).get("approved",
                                                                                                          False) == False:
                status = "منتظر امضای مدیر متقاضی"

            if r.get("desc", {}).get("approvers", {}).get("pos_vahede_darkhat_after_sign", {}).get("approved",
                                                                                                   False) == False:
                status = "منتظر امضای متقاضی"

            if r.get("desc", {}).get("approvers", {}).get("pos_modire_vahede_darkhat", {}).get("approved",
                                                                                               False) == False:
                status = "منتظر امضای مدیر متقاضی"

            if r.get("desc", {}).get("approvers", {}).get("pos_vahede_darkhat", {}).get("approved", False) == False:
                status = "منتظر امضای متقاضی"

            if r.get("desc", {}).get("approvers", {}).get("pos_masoole_edari", {}).get("approved",
                                                                                       False) == True or r.get("desc",
                                                                                                               {}).get(
                "approvers", {}).get("pos_masoole_edari", {}).get("approved", False) == True:
                status = "تایید شده"

            # r["tarikheAnjam"] = mil_to_sh(r["tarikheAnjam"]) if r["tarikheAnjam"] else "فرآیند"
            r["status"] = status

        return result

    def retrieve(self, request, *args, **kwargs):
        result = super(EZViewSet, self).retrieve(request, *args, **kwargs)
        return result

    @list_route(methods=["post"])
    def saveDraft(self, request, *args, **kwargs):
        dt = request.data
        dt["positionID"] = GetPositionViewset().GetCurrentPositionDocumentInstance(request).positionID
        dt["dateOfPost"] = datetime.now()
        dt["tarikheAnjam"] = datetime.strptime(sh_to_mil(request.data['tarikheAnjam']), "%Y/%m/%d") if request.data.get(
            'tarikheAnjam') else datetime.now()
        dt["typeOf"] = 1
        if request.data.get("id"):
            instance = self.queryset.get(id=request.data.get("id"))
            del request.data['id']
            ser = self.serializer_class(instance=instance, data=dt, partial=True)
            ser.is_valid(raise_exception=True)
            ser = ser.save()
            ser = self.serializer_class(instance=ser).data
            return Response(ser)
        ser = self.serializer_class(data=dt)
        ser.is_valid(raise_exception=True)
        ser = ser.save()
        ser = self.serializer_class(instance=ser).data
        return Response(ser)

    @list_route(methods=["get"])
    def get_report(self, request, *args, **kwargs):
        result = list(self.queryset.aggregate(
            {"$group": {"_id": "$tarikheAnjam", "count": {"$sum": 1}, "data": {"$push": '$$ROOT'}}},
            {"$project": {
                "_id": 1,
                "data": 1,
                "count": 1,
                "pers": "$data.desc.pers"
            }},
            {"$sort": {"_id": -1}},
            {"$limit": 50},
            {"$skip": 0}
        ))

        for r in result:
            countOfPersonnel = 0

            lud = []
            ez_pers = []
            for c in r['data']:
                for p in c['desc'].get('pers', []):
                    if p.get('personnel_code'):
                        lud.append(p.get('personnel_code'))
                        ez_pers.append(p)

            r["tedade_personnel"] = query(lud).distinct(lambda x: x).count()
            r["personnel_code"] = query(lud).distinct(lambda x: x).to_list()
            pers_for_report = query(ez_pers).distinct(lambda x: x['personnel_code']).to_list()
            for p in pers_for_report:
                p['az'] = int(p.get('az', '0').replace(":", ""))
                p['ta'] = int(p.get('ta', '0').replace(":", ""))
            r['times'] = []
            for i in range(0, 24):
                r['times'].append(
                    {
                        "title": "{}:00 - {}:59".format(str(i), str(i)),
                        "count": query(pers_for_report).where(
                            lambda x: x['az'] >= 0 and x['ta'] <= int(str(i) + "59")).count(),
                        "per_list": query(pers_for_report).where(
                            lambda x: x['az'] >= 0 and x['ta'] <= int(str(i) + "59")).to_list()
                    })

                if r["tedade_personnel"] > 1:
                    aa = 1

        return Response(result)

    @detail_route(methods=["post"])
    def removePerFromList(self, request, *args, **kwargs):
        instance = self.queryset.get(id=kwargs.get('id'))
        currentPos = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        if not request.user.id in [instance.desc['approvers']['pos_vahede_darkhat']['userID'],
                                   instance.desc['approvers']['pos_modire_vahede_darkhat']['userID'], ]:
            return Response({"message": "فقط درخواست کننده و مدیر آن میتواند لیست را نفر را حذف کند"},
                            status=status.HTTP_400_BAD_REQUEST)

        if instance.desc.get("commit", False) == True:
            return Response({"message": "پس از تایید نمیوان حذف کرد"},
                            status=status.HTTP_400_BAD_REQUEST)

        desc = instance.desc
        newpers = []
        for p in desc['pers']:
            if p['userID'] != request.data.get('userID'):
                newpers.append(p)

        desc['pers'] = newpers
        ser = self.serializer_class(instance=instance, data={"desc": desc}, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    @detail_route(methods=["get"])
    def removeApprovedEz(self, request, *args, **kwargs):
        instance = self.queryset.get(id=kwargs.get('id'))
        currentPos = GetPositionViewset().GetCurrentPositionDocumentInstance(request)

        if not request.user.id in [instance.desc['approvers']['pos_vahede_darkhat']['userID'],
                                   instance.desc['approvers']['pos_modire_vahede_darkhat']['userID'],
                                   ]:
            return Response({"message": "شما مجوز این حذف را ندارید"},
                            status=status.HTTP_400_BAD_REQUEST)

        if instance.desc['approvers'].get('pos_masoole_edari', {}).get('approved', False) == True or instance.desc[
            'approvers'].get('pos_modire_mali', {}).get('approved', False) == True:
            return Response({"message": "شما مجوز حذف اضافه کاری های تایید شده را ندارید"},
                            status=status.HTTP_400_BAD_REQUEST)
        if not currentPos.userID in [
            instance.desc['approvers']['pos_vahede_darkhat']['userID'],
            instance.desc['approvers']['pos_modire_vahede_darkhat']['userID']
        ]:
            return Response({"message": "شما مجوز این حذف را ندارید"},
                            status=status.HTTP_400_BAD_REQUEST)

        instance.delete()
        return Response({"ok": "ok"})

    @detail_route(methods=["post"])
    def savePers(self, request, *args, **kwargs):
        instance = self.queryset.get(id=kwargs.get('id'))
        currentPos = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        posIns = PositionDocumentLessDataSerializer(instance=currentPos).data
        desc = request.data['ez'].get('desc', {})
        if (instance.desc['approvers']['pos_modire_mali'].get('approved', False) == True) or (
                instance.desc['approvers']['pos_masoole_edari'].get('approved', False) == True):
            return Response({"message": "پس از امضا نهایی نمی توان ویرایش نمود"},
                            status=status.HTTP_400_BAD_REQUEST)
        prev_pers = query(instance.desc['pers']).where(lambda x: x['userID'] == request.data['per']['userID']).first()
        new_pers = request.data.get('per')

        changes = instance.desc.get('changes', [])
        changes.append({
            'prev': dict(prev_pers),
            'changeto': dict(new_pers),
            'changer': dict(posIns),
            'dateOfPost': datetime.now()

        })
        desc['changes'] = changes

        # ser = self.serializer_class(instance=instance, data={"desc.changes": desc['changes']}, partial=True)
        ser = self.serializer_class(instance=instance, data={"desc": desc}, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    @detail_route(methods=["post"])
    def sharheEghdam(self, request, *args, **kwargs):
        instance = self.queryset.get(id=kwargs.get('id'))
        currentPos = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        desc = request.data.get('desc', {})
        if request.data.get('Sharh') is None:
            return Response({"message": "شرح را وارد نمایید"}, status=status.HTTP_400_BAD_REQUEST)

        if request.data.get('Sharh') == "":
            return Response({"message": "شرح را وارد نمایید"}, status=status.HTTP_400_BAD_REQUEST)

        if desc["approvers"]["pos_vahede_darkhat_after_sign"].get("approved", False):
            return Response({"message": "امکان ثبت شرح پس از امضای سوم وجود ندارد"}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.id != currentPos.userID:
            return Response({"message": "فقط صادر کننده می تواند شرح را وارد نماید"},
                            status=status.HTTP_400_BAD_REQUEST)
        desc["dateOfSharh"] = datetime.now()
        ser = self.serializer_class(instance=instance, data={'desc': desc, 'Sharh': request.data.get('Sharh')},
                                    partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    @detail_route(methods=["get"])
    def writeToKaraweb(self, personnel_list, shamsiDate, mizan):
        hzview = HZViewSet()
        header = hzview.makeheader()
        url = "OverWork/GroupSubmission"
        header['Referer'] = "http://{}:{}/{}".format(hzview.hz_host, str(hzview.hz_port), url)
        header['Origin'] = "http://{}:{}".format(hzview.hz_host, str(hzview.hz_port))
        header["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        header["Cookie"] = header["Cookie"] + '; SectionsSelectableSearchCookieName=[]'
        # header["Cookie"] = ''
        myform = {
            '__RequestVerificationToken': header['__RequestVerificationToken'],
            'command': 'submit',
            # 'SelectedEmployeesEmpNoInJsonFormat': '[1008, 1012]',
            'SelectedEmployeesEmpNoInJsonFormat': '[' + personnel_list + ']',
            'SelectedEmployeesFiltering': '',
            # 'SubmitFromDateFormatted': '1399/09/11',
            # 'SubmitToDateFormatted': '1399/09/11',
            'SubmitFromDateFormatted': shamsiDate,
            'SubmitToDateFormatted': shamsiDate,
            # 'OverTimeFormatted': '02:00',
            'OverTimeFormatted': mizan,
            # 'DeleteFromDateFormatted': '1399/10/11',
            # 'DeleteToDateFormatted': '1399/10/11',
            'DeleteFromDateFormatted': shamsiDate,
            'DeleteToDateFormatted': shamsiDate,
            'X-Requested-With': 'XMLHttpRequest'}
        # del header['__RequestVerificationToken']

        h = Http()

        resp, content = h.request("http://{}:{}/{}".format(hzview.hz_host, str(hzview.hz_port), url), "GET",
                                  headers=header)
        content = bs4.BeautifulSoup(content, 'html.parser')
        myform['__RequestVerificationToken'] = content.find('input', {'name': '__RequestVerificationToken'})['value']
        resp, content = h.request("http://{}:{}/{}".format(hzview.hz_host, str(hzview.hz_port), url), "POST",
                                  urlencode(myform),
                                  headers=header)
        return content.decode()

    @detail_route(methods=["post"])
    def saveApprove(self, request, *args, **kwargs):
        instance = self.queryset.get(id=kwargs.get('id'))
        typeOfApprove = request.data.get('typeOfApprove')
        keyname = {}
        keyname['1'] = 'pos_vahede_darkhat'
        keyname['2'] = 'pos_modire_vahede_darkhat'
        keyname['3'] = 'pos_vahede_darkhat_after_sign'
        keyname['4'] = 'pos_modire_vahede_darkhat_after_sign'
        keyname['5'] = 'pos_modire_mali'
        keyname['6'] = 'pos_masoole_edari'

        currentApprovers = instance.desc.get('approvers', {}).get(keyname[str(typeOfApprove)], {})

        if currentApprovers is None:
            return Response({"message": "current key is invalid"}, status=status.HTTP_400_BAD_REQUEST)

        if currentApprovers['userID'] != request.user.id:
            return Response({"message": "شما مجوز این تایید را ندارید"}, status=status.HTTP_400_BAD_REQUEST)

        desc = instance.desc
        if desc["approvers"][keyname[str(typeOfApprove)]].get('approved') != None:
            return Response({"message": "شما قبلا امضا زده اید"}, status=status.HTTP_400_BAD_REQUEST)

        if typeOfApprove == 2:
            if not desc["approvers"]['pos_vahede_darkhat'].get('approved', False):
                return Response({"message": "لطفا ترتیب امضا را رعایت کنید"}, status=status.HTTP_400_BAD_REQUEST)

        if typeOfApprove == 3:
            if not desc["approvers"]['pos_modire_vahede_darkhat'].get('approved', False):
                return Response({"message": "لطفا ترتیب امضا را رعایت کنید"}, status=status.HTTP_400_BAD_REQUEST)

        if typeOfApprove == 4:
            if not desc["approvers"]['pos_vahede_darkhat_after_sign'].get('approved', False):
                return Response({"message": "لطفا ترتیب امضا را رعایت کنید"}, status=status.HTTP_400_BAD_REQUEST)

        if typeOfApprove == 5:
            if not desc["approvers"]['pos_modire_vahede_darkhat_after_sign'].get('approved', False):
                return Response({"message": "لطفا ترتیب امضا را رعایت کنید"}, status=status.HTTP_400_BAD_REQUEST)

        if desc.get("commit", False) == True:
            return Response({"message": "امضای پنجم قبلا توسط مسئول دیگری تایید شده است"},
                            status=status.HTTP_400_BAD_REQUEST)

        desc["approvers"][keyname[str(typeOfApprove)]]['approved'] = True
        desc["approvers"][keyname[str(typeOfApprove)]]['approved_date'] = datetime.now()
        if typeOfApprove in [5, 6]:
            desc["commit"] = True

        ser = self.serializer_class(instance=instance, data={"desc": desc}, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()

        cbs = []
        if desc.get("commit", False) == True:
            for p in instance.desc['pers']:
                res = self.writeToKaraweb(
                    p['personnel_code'],
                    mil_to_sh(instance.tarikheAnjam),
                    '{:02d}:{:02d}'.format(*divmod(p['mizan_daghighe'], 60), 60)

                )
                rss = json.loads(res)
                rss['pers_code'] = p['personnel_code']
                rss['anjam'] = mil_to_sh(instance.tarikheAnjam)
                rss['mizan'] = str(timedelta(minutes=p['mizan_daghighe']))[:-3]

                cbs.append(res)
            desc['commit_result'] = cbs
            ser = self.serializer_class(instance=instance, data={"desc.commit_result": desc['commit_result']},
                                        partial=True)
            ser.is_valid(raise_exception=True)
            ser.save()
        return Response(ser.data)

    @detail_route(methods=["post"])
    def postComment(self, request, *args, **kwargs):
        instance = self.queryset.get(id=kwargs.get('id'))
        current = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        data = request.data
        typeOfApprove = request.data.get('approve')
        keyname = {}
        keyname['1'] = 'pos_vahede_darkhat'
        keyname['2'] = 'pos_modire_vahede_darkhat'
        keyname['3'] = 'pos_vahede_darkhat_after_sign'
        keyname['4'] = 'pos_modire_vahede_darkhat_after_sign'
        keyname['5'] = 'pos_modire_mali'
        keyname['6'] = 'pos_masoole_edari'
        desc = instance.desc
        appr = desc["approvers"][keyname[str(typeOfApprove)]]

        if appr['userID'] != request.user.id:
            return Response({"message": "شما فقط مجاز کامنت گذاری برای خود هستید."},
                            status=status.HTTP_400_BAD_REQUEST)

        if len(desc["approvers"].get(keyname[str(typeOfApprove)], {}).get('comments', [])) == 0:
            desc["approvers"][keyname[str(typeOfApprove)]]['comments'] = []
        desc["approvers"][keyname[str(typeOfApprove)]]['comments'].append({
            'dateOfPost': datetime.now(),
            'comment': data['comment']})
        ser = self.serializer_class(instance=instance, data={"desc": desc}, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)


    def find_all_emza(self, current_position):
        emza_konandeh_ha = current_position.desc.get('taeed', None)
        if emza_konandeh_ha is not None:
            emza_1 = emza_konandeh_ha.get('ezafeh_kari_taeed', {}).get('first', None)
            emza_2 = emza_konandeh_ha.get('ezafeh_kari_taeed', {}).get('second', None)
            emza_3 = emza_konandeh_ha.get('ezafeh_kari_taeed', {}).get('third', None)
            emza_4 = emza_konandeh_ha.get('ezafeh_kari_taeed', {}).get('forth', None)
            user1 = MyUser.objects.filter(personnel_code=emza_1).order_by("-id").first() if emza_1 else None
            user2 = MyUser.objects.filter(personnel_code=emza_2).order_by("-id").first() if emza_2 else None
            user3 = MyUser.objects.filter(personnel_code=emza_3).order_by("-id").first() if emza_3 else None
            user4 = MyUser.objects.filter(personnel_code=emza_4).order_by("-id").first() if emza_4 else None
            user1 = user1.id if user1 else None
            user2 = user2.id if user2 else None
            user3 = user3.id if user3 else None
            user4 = user4.id if user4 else None
            pos1 = PositionsDocument.objects.filter(companyID=700, userID=user1).order_by(
                "-id").first() if user1 else None
            pos2 = PositionsDocument.objects.filter(companyID=700, userID=user2).order_by(
                "-id").first() if user2 else None
            pos3 = PositionsDocument.objects.filter(companyID=700, userID=user3).order_by(
                "-id").first() if user3 else None
            pos4 = PositionsDocument.objects.filter(companyID=700, userID=user4).order_by(
                "-id").first() if user4 else None
            emza_konandeh_ha = []
            if pos1: emza_konandeh_ha.append(PositionDocumentLessDataSerializer(instance=pos1).data)
            if pos2: emza_konandeh_ha.append(PositionDocumentLessDataSerializer(instance=pos2).data)
            if pos3: emza_konandeh_ha.append(PositionDocumentLessDataSerializer(instance=pos3).data)
            if pos4: emza_konandeh_ha.append(PositionDocumentLessDataSerializer(instance=pos4).data)
            return emza_konandeh_ha


    @list_route(methods=["post"])
    def start(self, request, *args, **kwargs):
        dt = request.data
        dt["positionID"] = GetPositionViewset().GetCurrentPositionDocumentInstance(request).positionID
        dt["dateOfPost"] = datetime.now()
        dt["tarikheAnjam"] = datetime.strptime(sh_to_mil(request.data['tarikheAnjam']), "%Y/%m/%d") if request.data.get(
            'tarikheAnjam') else datetime.now()

        if dt["tarikheAnjam"] < datetime.now() - timedelta(days=4):
            return Response({"message": "اضافه کار ثبتی می بایست برای امروز یا بعد از آن باشد"},
                            status=status.HTTP_400_BAD_REQUEST)

        lalala = []
        total_minutes = 0
        for p in request.data['desc']['pers']:
            if p.get('check', False) == True:
                az = datetime.strptime(p['az'], '%H:%M').time()
                ta = datetime.strptime(p['ta'], '%H:%M').time()
                enter_delta = timedelta(hours=az.hour, minutes=az.minute, seconds=az.second)
                exit_delta = timedelta(hours=ta.hour, minutes=ta.minute, seconds=ta.second)
                difference_delta = exit_delta - enter_delta
                p['mizan_daghighe'] = int(difference_delta.seconds / 60)
                total_minutes += p['mizan_daghighe']
                lalala.append(p)

                if az >= ta:
                    return Response({"message": "زمان اضافه کار را بدرستی وارد کنید"},
                                    status=status.HTTP_400_BAD_REQUEST)

        request.data['desc']['pers'] = lalala
        request.data['desc']['total_daghigheh'] = total_minutes

        current_approver = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        chartInstance = Chart.objects.get(id=current_approver.chartID)

        # chart 15 is modir
        recursive_limit = 0

        def find_modir(currentChart, recursive_limit):
            recursive_limit += 1
            if recursive_limit == 20:
                return currentChart
            topid = Chart.objects.filter(id=currentChart.top_id)
            if currentChart.rank == 15:
                return currentChart
            if topid.first():
                if topid.first().rank == 15:
                    return topid.first()
            if currentChart.rank != 15 and currentChart.rank != 16 :
                find_modir(topid.first(), recursive_limit)
            return currentChart

        # modiresh = find_modir(chartInstance, recursive_limit)

        modiresh_emza_konandeh_ha = self.find_all_emza(current_approver)
        if len(modiresh_emza_konandeh_ha) == 0:
            raise APIException('لطفا نفری را برای تایید اضافه کاری این مشخص نمایید - این فرآیند توسط ادادری انجام می شود')


        modire_mali = Chart.objects.get(id=3503)
        masoole_edari = Chart.objects.get(id=3504)
        # get positions
        pos_modiresh = PositionsDocument.objects.filter(chartID=modiresh_emza_konandeh_ha[0]['chartID'], userID__ne=None).order_by("-id").first()
        pos_modire_mali = PositionsDocument.objects.filter(chartID=modire_mali.id, userID__ne=None).order_by(
            "-id").first()
        pos_masoole_edari = PositionsDocument.objects.filter(chartID=masoole_edari.id, userID__ne=None).order_by(
            "-id").first()

        pos_current = PositionDocumentLessDataSerializer(instance=current_approver).data
        pos_modiresh = PositionDocumentLessDataSerializer(instance=pos_modiresh).data
        pos_modire_mali = PositionDocumentLessDataSerializer(instance=pos_modire_mali).data
        pos_masoole_edari = PositionDocumentLessDataSerializer(instance=pos_masoole_edari).data

        dt["desc"] = request.data["desc"]
        dt["desc"]["approvers"] = {
            'pos_vahede_darkhat': pos_current,
            'pos_modire_vahede_darkhat': pos_modiresh,
            'pos_vahede_darkhat_after_sign': pos_current,
            'pos_modire_vahede_darkhat_after_sign': pos_modiresh,
            'pos_modire_mali': pos_modire_mali,
            'pos_masoole_edari': pos_masoole_edari,
        }
        is_entered_before = self.queryset.filter(
            positionID=dt["desc"]["approvers"]['pos_vahede_darkhat']["positionID"],
            tarikheAnjam=dt["tarikheAnjam"]
        ).count() > 0
        if is_entered_before:
            return Response({"message": "برای یک روز فقط میتوان یک اضافه کار ثبت کرد"},
                            status=status.HTTP_400_BAD_REQUEST)

        dt["typeOf"] = 2
        if request.data.get("id"):
            instance = self.queryset.get(id=request.data.get("id"))
            del request.data['id']
            ser = self.serializer_class(instance=instance, data=dt, partial=True)
            ser.is_valid(raise_exception=True)
            ser = ser.save()
            ser = self.serializer_class(instance=ser).data
            result = Response(ser)
        else:
            ser = self.serializer_class(data=dt)
            ser.is_valid(raise_exception=True)
            ser = ser.save()
            ser = self.serializer_class(instance=ser).data
            result = Response(ser)

        return result
