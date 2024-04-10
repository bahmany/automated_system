import base64
import json
import re
import uuid
from datetime import datetime
from io import BytesIO
from urllib.parse import urlencode

import openpyxl

import bs4
from asq.initiators import query
from django.shortcuts import render_to_response
from django.template import RequestContext
from httplib2 import Http
from mongoengine import Q
from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.CompaniesManagment.Charts.models import Chart
from amspApp.CompaniesManagment.Connections.models import ConnectionPools, Connections
from amspApp.CompaniesManagment.Connections.viewes.ConnectionsViews import ConnectionsViewSet
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.Positions.serializers.PositionSerializer import PositionDocumentLessDataSerializer
from amspApp.Infrustructures.Classes.DateConvertors import getCurrentYearShamsi, getCurrentMonthShamsi, mil_to_sh, \
    is_valid_shamsi_date
from amspApp.Infrustructures.Classes.convert_sqlresult_to_validstr import convert_sqlresultstr_to_valid_str, \
    convert_sqlresultstr_to_valid_numbers
from amspApp.Edari.Morekhasi.models import MorekhasiSaati
from amspApp.Edari.Morekhasi.serializers.MorekhasiSaatieSerializers import MorekhasiSaatieSerializers
from amspApp.Notifications.models import Notifications
from amspApp._Share.ListPagination import DataTableForNewDatables_net
from amspApp.amspUser.models import MyUser
from amspApp.Edari.hz.views.HZViewSet import HZViewSet
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class MorekhasiSaatiViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = MorekhasiSaati.objects.all().order_by('-id')
    serializer_class = MorekhasiSaatieSerializers
    pagination_class = DataTableForNewDatables_net

    dtcols = [
        {'type': "string", 'data': 'status', 'title': 'وضعیت'},
        {'type': "string", 'data': 'exp.pos_vahede_darkhat.profileName', 'title': 'متقاضی'},
        {'type': "string", 'data': 'exp.dateofmorekhasi', 'title': 'تاریخ'},
        {'type': "string", 'data': 'exp.az', 'title': 'از'},
        {'type': "string", 'data': 'exp.taa', 'title': 'تا'},
        {'type': "string", 'data': 'exp.mizan', 'title': 'میزان - دقیقه'},

    ]

    pagination_class.dtcols = dtcols

    @list_route(methods=["get"])
    def getDatatableCols(self, request, *args, **kwargs):
        return Response(self.dtcols)

    def retrieve(self, request, *args, **kwargs):
        result = super(MorekhasiSaatiViewSet, self).retrieve(request, *args, **kwargs)
        q1 = Q(userID=request.user.id)
        q2 = Q(extra__id=result.data['id'])
        qq = q1 & q2
        Notifications.objects.filter(qq).delete()
        return result

    def get_queryset(self):
        info = self.get_personnel_info(self.request, *{}, **{})

        q1 = Q(creator_position=GetPositionViewset().GetCurrentPositionDocumentInstance(self.request).positionID)
        q2 = Q(exp__pos_vahede_dakhat__userID=self.request.user.id)
        q3 = Q(exp__pos_modire_vahede_darkhat__userID=self.request.user.id)
        q4 = Q(exp__pos_modire_mali__userID=self.request.user.id)
        q5 = Q(exp__pos_masoole_edari__userID=self.request.user.id)
        q996 = Q(exp__pos_emaza_konandeha__userID=self.request.user.id)
        q6 = q1 | q2 | q3 | q4 | q5 | q996

        if info.data['exp']['pos_modire_mali']['userID'] == self.request.user.id:
            q1 = Q(exp__pos_vahede_darkhat__is_signed=True)
            q2 = Q(exp__pos_modire_vahede_darkhat__is_signed=True)
            q3 = Q(exp__pos_modire_mali__is_signed__ne=True)
            q4 = Q(exp__pos_masoole_edari__is_signed__ne=True)
            q5 = Q(exp__pos_modire_vahede_darkhat__userID=self.request.user.id)

            q6 = q1 & q2 & q3 & q4 | q5

        if info.data['exp']['pos_masoole_edari']['userID'] == self.request.user.id:
            q1 = Q(exp__pos_vahede_darkhat__is_signed=True)
            q2 = Q(exp__pos_modire_vahede_darkhat__is_signed=True)
            q3 = Q(exp__pos_modire_mali__is_signed__ne=True)
            q4 = Q(exp__pos_masoole_edari__is_signed__ne=True)
            q5 = Q(exp__pos_modire_vahede_darkhat__userID=self.request.user.id)
            q6 = q1 & q2 & q3 & q4 | q5

        self.queryset = self.queryset.filter(q6)
        result = super(MorekhasiSaatiViewSet, self).get_queryset()
        return result

    def template_base(self, request):
        return render_to_response(
            'Edari/Morekhasi/Saati/base.html',
            {},
            context_instance=RequestContext(request))

    def template_add(self, request):

        checker = []

        # morekhasi saati checker
        posInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        msaati = posInstance.desc.get('taeed', {}).get('morekhasi_saati_taeed', {}).get('first', False)
        if msaati == False or msaati == '' or msaati == None:
            checker.append({
                'msgtype': 1,
                'msg': 'شما نمی توانید از مرخصی ساعتی استفاده کنید - هنوز شخصی بعنوان امضا کننده مرخصی ساعتی برای مشخص نشده است. لطفا با واحد اداری تماس بگیرید.'
            })

        has_check = len(checker) > 0
        return render_to_response(
            'Edari/Morekhasi/Saati/add.html',
            {'checker': checker, 'has_check': has_check},
            context_instance=RequestContext(request))

    def template_list(self, request):
        return render_to_response(
            'Edari/Morekhasi/Saati/list.html',
            {},
            context_instance=RequestContext(request))

    def template_MyMorekhasi(self, request):
        return render_to_response(
            'Edari/Morekhasi/Saati/my.html',
            {},
            context_instance=RequestContext(request))

    def template_MorekhasisaatiEzamat(self, request):
        if request.user.groups.filter(name="group_entezamaat").count() == 0:
            return render_to_response('Financial/cog/noaccess.html', {}, context_instance=RequestContext(request))
        return render_to_response(
            'Edari/Morekhasi/Saati/entezamat.html',
            {},
            context_instance=RequestContext(request))

    def template_MorekhasisaatiEdari(self, request):
        if request.user.groups.filter(name="group_edari").count() == 0:
            return render_to_response('Financial/cog/noaccess.html', {}, context_instance=RequestContext(request))

        return render_to_response(
            'Edari/Morekhasi/Saati/edari.html',
            {},
            context_instance=RequestContext(request))

    def find_all_emza(self, current_position):
        emza_konandeh_ha = current_position.desc.get('taeed', None)
        if emza_konandeh_ha is not None:
            emza_1 = emza_konandeh_ha.get('morekhasi_saati_taeed', {}).get('first', None)
            emza_2 = emza_konandeh_ha.get('morekhasi_saati_taeed', {}).get('second', None)
            emza_3 = emza_konandeh_ha.get('morekhasi_saati_taeed', {}).get('third', None)
            emza_4 = emza_konandeh_ha.get('morekhasi_saati_taeed', {}).get('forth', None)
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

    @list_route(methods=['get'])
    def get_personnel_info(self, request, *args, **kwargs):
        typeofrequest = request.query_params.get('q')
        current_approver = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        chartInstance = Chart.objects.get(id=current_approver.chartID)
        # chart 15 is modir
        recursive_limit = 0

        def find_modir(currentChart, recursive_limit):
            recursive_limit += 1
            if recursive_limit == 120:
                return currentChart
            if currentChart.top_id == None:
                return currentChart
            topid = Chart.objects.filter(id=currentChart.top_id)
            if currentChart.rank == 15:
                return currentChart
            if topid.first():
                if topid.first().rank == 15:
                    return topid.first()
            if currentChart.rank != 15:
                currentChart = find_modir(topid.first(), recursive_limit)
            return currentChart

        # modiresh = find_modir(chartInstance, recursive_limit)
        modiresh = chartInstance.top

        emza_konandeh_ha = self.find_all_emza(current_approver)

        modire_mali = Chart.objects.get(id=3503)
        masoole_edari = Chart.objects.get(id=3504)
        # get positions
        pos_modiresh = PositionsDocument.objects.filter(chartID=modiresh.id, userID__ne=None).order_by("-id").first()
        pos_modire_mali = PositionsDocument.objects.filter(chartID=modire_mali.id, userID__ne=None).order_by(
            "-id").first()
        pos_masoole_edari = PositionsDocument.objects.filter(chartID=masoole_edari.id, userID__ne=None).order_by(
            "-id").first()

        pos_current = PositionDocumentLessDataSerializer(instance=current_approver).data
        pos_modiresh = PositionDocumentLessDataSerializer(instance=pos_modiresh).data
        pos_modire_mali = PositionDocumentLessDataSerializer(instance=pos_modire_mali).data
        pos_masoole_edari = PositionDocumentLessDataSerializer(instance=pos_masoole_edari).data

        result = {
            'pos_vahede_darkhat': pos_current,
            'pos_modire_vahede_darkhat': pos_modiresh,
            'pos_vahede_darkhat_after_sign': pos_current,
            'pos_modire_vahede_darkhat_after_sign': pos_modiresh,
            'pos_emaza_konandeha': emza_konandeh_ha,
            'pos_modire_mali': pos_modire_mali,
            'pos_masoole_edari': pos_masoole_edari,
        }
        result = {
            'dateOfPost': datetime.now(),
            'creator_position': GetPositionViewset().GetCurrentPositionDocumentInstance(request).positionID,
            'exp': result
        }

        return Response(result)

    @list_route(methods=['post'])
    def get_personnel_by_code(self, request, *args, **kwargs):
        if len(request.data['personnel_code']) > 12:
            return Response({"message": "لطفا کد معتبری را وارد کنید"},
                            status=status.HTTP_400_BAD_REQUEST)
        userInstance = MyUser.objects.filter(personnel_code=request.data['personnel_code']).first()
        if userInstance == None:
            return Response({"message": "کد وارد شده یافت نشد"},
                            status=status.HTTP_400_BAD_REQUEST)
        request.user = userInstance
        result = self.get_personnel_info(request, *args, **kwargs)
        result.data['creator_position'] = GetPositionViewset().GetCurrentPositionDocumentInstance(request).positionID
        return result

    @list_route(methods=['get'])
    def get_mandeh_morekhasi_current_year(self, request, *args, **kwargs):
        request.query_params._mutable = True

        request.query_params['q'] = request.user.personnel_code
        request.query_params['d'] = 1
        r1 = self.get_mandeh_morekhasi(request, *args, **kwargs)

        request.query_params['d'] = 2
        r2 = self.get_mandeh_morekhasi(request, *args, **kwargs)

        request.query_params['d'] = 3
        r3 = self.get_mandeh_morekhasi(request, *args, **kwargs)

        request.query_params['d'] = 4
        r4 = self.get_mandeh_morekhasi(request, *args, **kwargs)

        request.query_params['d'] = 5
        r5 = self.get_mandeh_morekhasi(request, *args, **kwargs)

        request.query_params['d'] = 6
        r6 = self.get_mandeh_morekhasi(request, *args, **kwargs)

        request.query_params['d'] = 7
        r7 = self.get_mandeh_morekhasi(request, *args, **kwargs)

        request.query_params['d'] = 8
        r8 = self.get_mandeh_morekhasi(request, *args, **kwargs)

        request.query_params['d'] = 9
        r9 = self.get_mandeh_morekhasi(request, *args, **kwargs)

        request.query_params['d'] = 10
        r10 = self.get_mandeh_morekhasi(request, *args, **kwargs)

        request.query_params['d'] = 11
        r11 = self.get_mandeh_morekhasi(request, *args, **kwargs)

        request.query_params['d'] = 12
        r12 = self.get_mandeh_morekhasi(request, *args, **kwargs)

        result = [
            r1.data,
            r2.data,
            r3.data,
            r4.data,
            r5.data,
            r6.data,
            r7.data,
            r8.data,
            r9.data,
            r10.data,
            r11.data,
            r12.data
        ]

        return Response(result)

    @list_route(methods=['get'])
    def get_mandeh_morekhasi(self, request, *args, **kwargs):
        personnel_code = request.query_params.get('q')
        period = {}
        current_year = getCurrentYearShamsi()
        period[1] = [str(int(current_year) - 1) + "/12/26", str(current_year) + "/01/25"]
        period[2] = [str(current_year) + "/01/26", str(current_year) + "/02/25"]
        period[3] = [str(current_year) + "/02/26", str(current_year) + "/03/25"]
        period[4] = [str(current_year) + "/03/26", str(current_year) + "/04/25"]
        period[5] = [str(current_year) + "/04/26", str(current_year) + "/05/25"]
        period[6] = [str(current_year) + "/05/26", str(current_year) + "/06/25"]
        period[7] = [str(current_year) + "/06/26", str(current_year) + "/07/25"]
        period[8] = [str(current_year) + "/07/26", str(current_year) + "/08/25"]
        period[9] = [str(current_year) + "/08/26", str(current_year) + "/09/25"]
        period[10] = [str(current_year) + "/09/26", str(current_year) + "/10/25"]
        period[11] = [str(current_year) + "/10/26", str(current_year) + "/11/25"]
        period[12] = [str(current_year) + "/11/26", str(current_year) + "/12/25"]

        current_month = getCurrentMonthShamsi()

        if request.query_params.get('d'):
            current_month = request.query_params.get('d')

        hzview = HZViewSet()
        header = hzview.makeheader()
        url = "KaraReports/KarkardSummary"
        header['Referer'] = "http://{}:{}/{}".format(hzview.hz_host, str(hzview.hz_port), url)
        header['Origin'] = "http://{}:{}".format(hzview.hz_host, str(hzview.hz_port))
        header[
            'Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        header["Content-Type"] = "application/x-www-form-urlencoded"
        header["Cookie"] = header[
                               "Cookie"] + '; SectionsSelectableSearchCookieName=[]; mormamdailymormam_MdsGridView=mormamdailymormam_MdsGridView={%22PageNumber%22:1%2C%22FilteringString%22:%22%22%2C%22SortingString%22:%22%22%2C%22SelectedRowsIds%22:[' + str(
            request.user.personnel_code) + ']}; SortingAndSeparation1CookieName={%22SelectedSortItemId%22:0%2C%22SelectedSeparationItemId%22:0%2C%22SelectedSortDirection%22:1%2C%22PrintReportTitleOnlyOnce%22:false%2C%22PrintNationalCode%22:false%2C%22IsReportContinuous%22:false}; SectionsSelectableSearchCookieName=[]; MonthSelector4CookieName={%22MonthSelector4StartDateFormatted%22:%22%DB%B1%DB%B3%DB%B9%DB%B2/%DB%B0%DB%B1/%DB%B0%DB%B1%22%2C%22MonthSelector4EndDateFormatted%22:%22%DB%B1%DB%B4%DB%B0%DB%B0/%DB%B0%DB%B6/%DB%B2%DB%B0%22}; '
        header["Cache-Control"] = "max-age=0"
        myform = {
            '__RequestVerificationToken': header['__RequestVerificationToken'],
            'command': 'ایجاد جدول اکسل',
            'StartDate': period[int(current_month)][0],
            'EndDate': period[int(current_month)][1],
            'Year': int(current_year),
            'Month': int(current_month),
            'GroupById': 0,
            'SortItemId': 0,
            'SortDirectionId': 2,
            'IsReportContinuous': False,
            'SelectedEmployeesFiltering': '',
            'SelectedReportItems1InJsonFormat': [17],
            'SelectedEmployeesEmpNoInJsonFormat': [int(personnel_code)],
            'MonthSelector1Month': int(current_month),
            'MonthSelector1Year': int(current_year),
            'MonthSelector1StartDateFormatted': period[int(current_month)][0],
            'MonthSelector1EndDateFormatted': period[int(current_month)][1],
            'SortingAndSeparation1SelectedSeparationItemId': 0,
            'SortingAndSeparation1SelectedSortItemId': 0,
            'SortingAndSeparation1SelectedSortDirection': 0,
        }

        h = Http()
        resp, content = h.request(
            "http://{}:{}/{}".format(hzview.hz_host, str(hzview.hz_port), 'KaraReports/KarkardSummary'), "GET",
            headers=header)
        content = bs4.BeautifulSoup(content, 'html.parser')
        myform['__RequestVerificationToken'] = content.find('input', {'name': '__RequestVerificationToken'})['value']
        resp, content = h.request("http://{}:{}/{}".format(hzview.hz_host, str(hzview.hz_port), url), "POST",
                                  urlencode(myform),
                                  headers=header)

        p = BytesIO(content)
        workbook = openpyxl.load_workbook(p)
        sheet_obj = workbook.active

        return Response({
            'result': str(sheet_obj['H2'].value),
            'from': period[int(current_month)][0],
            'to': period[int(current_month)][1],

        })

    @list_route(methods=['get'])
    def get_mandeh_morekhasi_koli(self, request, *args, **kwargs):

        # ------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------
        # first GET for getting validators
        hzview = HZViewSet()
        header = hzview.makeheader()
        url = "KaraReports/RemainKardex"
        header['Referer'] = "http://{}:{}/{}".format(hzview.hz_host, str(hzview.hz_port), url)
        header['Origin'] = "http://{}:{}".format(hzview.hz_host, str(hzview.hz_port))
        header[
            'Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        header["Content-Type"] = "application/x-www-form-urlencoded"
        # "Cookie"] + '; SectionsSelectableSearchCookieName=[]; mormamdailymormam_MdsGridView=mormamdailymormam_MdsGridView={%22PageNumber%22:1%2C%22FilteringString%22:%22%22%2C%22SortingString%22:%22%22%2C%22SelectedRowsIds%22:[%22456453%22]}; SortingAndSeparation1CookieName={%22SelectedSortItemId%22:0%2C%22SelectedSeparationItemId%22:0%2C%22SelectedSortDirection%22:1%2C%22PrintReportTitleOnlyOnce%22:false%2C%22PrintNationalCode%22:false%2C%22IsReportContinuous%22:false}; SectionsSelectableSearchCookieName=[]; MonthSelector4CookieName={%22MonthSelector4StartDateFormatted%22:%22%DB%B1%DB%B3%DB%B9%DB%B2/%DB%B0%DB%B1/%DB%B0%DB%B1%22%2C%22MonthSelector4EndDateFormatted%22:%22%DB%B1%DB%B4%DB%B0%DB%B0/%DB%B0%DB%B6/%DB%B2%DB%B0%22}; '
        header["Cache-Control"] = "max-age=0"
        header["Upgrade-Insecure-Requests"] = '1'
        h = Http()
        first_resp, first_content = h.request(
            "http://{}:{}/{}".format(hzview.hz_host, str(hzview.hz_port), url),
            "GET",
            headers=header)
        # ------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------
        url = "KaraReports/RemainKardex"
        bs4__content = bs4.BeautifulSoup(first_content, 'html.parser')
        myform = {}
        myform['__RequestVerificationToken'] = bs4__content.find('input', {'name': '__RequestVerificationToken'})[
            'value']
        myform = {
            '__RequestVerificationToken': myform['__RequestVerificationToken'],
            'DateFormatted': mil_to_sh(datetime.now()),
            'MinTimeFormatted': '-999:00',
            'MaxTimeFormatted': '9999:00',
            'command': ' مشاهده',
            'GroupById': 0,
            'SortItemId': 0,
            'IsReportContinuous': False,
            'SelectedEmployeesFiltering': '',
            'SelectedReportItems1InJsonFormat': [17],
            'SelectedEmployeesEmpNoInJsonFormat': [int(request.user.personnel_code)],
            'SortingAndSeparation1SelectedSeparationItemId': 0,
            'SortingAndSeparation1SelectedSortItemId': 0,
            'SortingAndSeparation1SelectedSortDirection': 1,
            'SortDirectionId: 1': 1,
        }

        ppp = '; SortingAndSeparation1CookieName={%22SelectedSortItemId%22:0%2C%22SelectedSeparationItemId%22:0%2C%22SelectedSortDirection%22:1%2C%22PrintReportTitleOnlyOnce%22:false%2C%22PrintNationalCode%22:false%2C%22IsReportContinuous%22:false}; SectionsSelectableSearchCookieName=[]; SearchSelectableEmployees_MdGridView={%22PageNumber%22:1%2C%22FilteringString%22:%22%22%2C%22SortingString%22:%22%22%2C%22SelectedRowsIds%22:[' + str(
            request.user.personnel_code) + ']};'
        header['Cookie'] = header['Cookie'] + "; " + ppp
        # header['__RequestVerificationToken'] = myform['__RequestVerificationToken']

        second_h = Http()
        second_resp, second_content = h.request(
            "http://{}:{}/{}".format(hzview.hz_host, str(hzview.hz_port), url), "POST",
            body=urlencode(myform),
            headers=header)

        bs4_second_content = bs4.BeautifulSoup(second_content, 'html.parser')
        bs4___RequestVerificationToken_content = \
            bs4_second_content.find('input', {'name': '__RequestVerificationToken'})['value']
        # ------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------

        # myform['__RequestVerificationToken'] = content.find('input', {'name': '__RequestVerificationToken'})['value']
        myform = {}
        header['Cookie'] = re.sub(r"\_RequestVerificationToken.*?\; ", "", header['Cookie']).replace("; ;", " ;")
        header['Cookie'] = header['Cookie'] + " RequestVerificationToken=" + bs4___RequestVerificationToken_content
        myform['mvcviewer_action'] = 'Report'
        reportGUID = str(uuid.uuid4()).replace('-', '')
        myform[
            'mvcviewer_parameters'] = '{"viewerId":"MvcViewer","routes":{"action":"RemainKardex","controller":"KaraReports"},"formValues":{},"clientGuid":"' + reportGUID + '","reportGuid":null,"paramsGuid":null,"drillDownGuid":null,"serverCacheMode":"ObjectCache","serverCacheTimeout":20,"serverCacheItemPriority":"Default","pageNumber":0,"zoom":100,"viewMode":"OnePage","showBookmarks":true,"openLinksTarget":"_blank","chartRenderType":"AnimatedVector","drillDownParameters":[],"editableParameters":null}'
        myform['mvcviewer_parameters'] = base64.encodebytes(myform['mvcviewer_parameters'].encode())

        resp, content = h.request(
            "http://{}:{}/{}".format(hzview.hz_host, str(hzview.hz_port), 'KaraReports/RemainKardexStimulsoftReport'),
            "POST",
            body=urlencode(myform),
            headers=header)

        cc = json.loads(content.decode().replace("<table", "<table class='table table-bordered table-striped mini' "))
        return Response(cc)

    @list_route(methods=['get'])
    def get_mandeh_report_detail(self, request, *args, **kwargs):

        # ------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------
        # first GET for getting validators
        hzview = HZViewSet()
        header = hzview.makeheader()
        url = "KaraReports/DailyVacationMission"
        header['Referer'] = "http://{}:{}/{}".format(hzview.hz_host, str(hzview.hz_port), url)
        header['Origin'] = "http://{}:{}".format(hzview.hz_host, str(hzview.hz_port))
        header[
            'Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        header["Content-Type"] = "application/x-www-form-urlencoded"
        # "Cookie"] + '; SectionsSelectableSearchCookieName=[]; mormamdailymormam_MdsGridView=mormamdailymormam_MdsGridView={%22PageNumber%22:1%2C%22FilteringString%22:%22%22%2C%22SortingString%22:%22%22%2C%22SelectedRowsIds%22:[%22456453%22]}; SortingAndSeparation1CookieName={%22SelectedSortItemId%22:0%2C%22SelectedSeparationItemId%22:0%2C%22SelectedSortDirection%22:1%2C%22PrintReportTitleOnlyOnce%22:false%2C%22PrintNationalCode%22:false%2C%22IsReportContinuous%22:false}; SectionsSelectableSearchCookieName=[]; MonthSelector4CookieName={%22MonthSelector4StartDateFormatted%22:%22%DB%B1%DB%B3%DB%B9%DB%B2/%DB%B0%DB%B1/%DB%B0%DB%B1%22%2C%22MonthSelector4EndDateFormatted%22:%22%DB%B1%DB%B4%DB%B0%DB%B0/%DB%B0%DB%B6/%DB%B2%DB%B0%22}; '
        header["Cache-Control"] = "max-age=0"
        header["Upgrade-Insecure-Requests"] = '1'
        h = Http()
        first_resp, first_content = h.request(
            "http://{}:{}/{}".format(hzview.hz_host, str(hzview.hz_port), url),
            "GET",
            headers=header)
        # ------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------
        url = "KaraReports/DailyVacationMission"
        bs4__content = bs4.BeautifulSoup(first_content, 'html.parser')
        myform = {}
        myform['__RequestVerificationToken'] = bs4__content.find('input', {'name': '__RequestVerificationToken'})[
            'value']

        myform = {
            '__RequestVerificationToken': myform['__RequestVerificationToken'],
            'SelectedCardNos1InJsonFormat': [54, 69, 64, 57, 60, 65, 58, 59, 61],
            'SelectedEmployeesEmpNoInJsonFormat': [int(request.user.personnel_code)],
            'SelectedEmployeesFiltering': '',
            'StartDate': getCurrentYearShamsi() + '/01/01',
            'EndDate': mil_to_sh(datetime.now()),
            'Month': -1,
            'Year': int(getCurrentYearShamsi()),
            'GroupById': 0,
            'SortItemId': 0,
            'SortDirectionId': 1,
            'IsReportContinuous': False,
            'MonthSelector1Month': -1,
            'MonthSelector1StartDateFormatted': getCurrentYearShamsi() + '/ 01 / 01',
            'MonthSelector1EndDateFormatted': mil_to_sh(datetime.now()),
            'SortingAndSeparation1SelectedSeparationItemId': 0,
            'SortingAndSeparation1SelectedSortItemId': 0,
            'SortingAndSeparation1SelectedSortDirection': 1,
            'command': 'مشاهده'}

        second_resp, second_content = h.request(
            "http://{}:{}/{}".format(hzview.hz_host, str(hzview.hz_port), url), "POST",
            body=urlencode(myform),
            headers=header)

        bs4_second_content = bs4.BeautifulSoup(second_content, 'html.parser')
        bs4___RequestVerificationToken_content = \
            bs4_second_content.find('input', {'name': '__RequestVerificationToken'})['value']
        # ------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------
        # ------------------------------------------------------------------------------------

        # myform['__RequestVerificationToken'] = content.find('input', {'name': '__RequestVerificationToken'})['value']
        myform = {}
        header['Cookie'] = re.sub(r"\_RequestVerificationToken.*?\; ", "", header['Cookie']).replace("; ;", " ;")
        header['Cookie'] = header['Cookie'] + " RequestVerificationToken=" + bs4___RequestVerificationToken_content
        myform['mvcviewer_action'] = 'Report'
        reportGUID = str(uuid.uuid4()).replace('-', '')
        myform[
            'mvcviewer_parameters'] = '{"viewerId":"MvcViewer","routes":{"action":"KaraReports","controller":"DailyVacationMission"},"formValues":{},"clientGuid":"' + reportGUID + '","reportGuid":null,"paramsGuid":null,"drillDownGuid":null,"serverCacheMode":"ObjectCache","serverCacheTimeout":20,"serverCacheItemPriority":"Default","pageNumber":0,"zoom":100,"viewMode":"OnePage","showBookmarks":true,"openLinksTarget":"_blank","chartRenderType":"AnimatedVector","drillDownParameters":[],"editableParameters":null}'
        myform['mvcviewer_parameters'] = base64.encodebytes(myform['mvcviewer_parameters'].encode())

        resp, content = h.request(
            "http://{}:{}/{}".format(hzview.hz_host, str(hzview.hz_port),
                                     'KaraReports/DailyVacationMissionStimulsoftReport'),
            "POST",
            body=urlencode(myform),
            headers=header)

        cc = json.loads(content.decode().replace("<table", "<table class='table table-bordered table-striped mini' "))
        return Response(cc)

    @list_route(methods=['post'])
    def confirm(self, request, *args, **kwargs):
        current_pos = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        if request.data.get('exp').get('confirm_type') == 1:
            requester_pos = PositionsDocument.objects.get(
                positionID=request.data['exp']['pos_vahede_darkhat']['positionID'])
            emza = self.find_all_emza(requester_pos)
            morekhasi_item = request.data
            if morekhasi_item['exp']['pos_vahede_darkhat'].get('is_signed') == True:
                return Response({"message": "از قبل این مرخصی امضا شده است"},
                                status=status.HTTP_400_BAD_REQUEST)
            # morekhasi_item['exp']['pos_vahede_darkhat'] = self.get_personnel_info(request, *args, **kwargs).data['exp'][
            #     'pos_vahede_darkhat']

            if datetime.strptime(request.data.get('exp')['az'], '%H:%M').time() >= datetime.strptime(
                    request.data.get('exp')['taa'], '%H:%M').time():
                return Response({"message": "در ورود ساعات مرخصی دقت نمایید"},
                                status=status.HTTP_400_BAD_REQUEST)

            morekhasi_item['exp']['pos_vahede_darkhat']['is_signed'] = True
            morekhasi_item['exp']['pos_emaza_konandeha'] = emza
            morekhasi_item['exp']['pos_vahede_darkhat'][
                'position_id'] = requester_pos.positionID
            morekhasi_item['exp']['pos_vahede_darkhat']['date_of_signed'] = datetime.now()

            if morekhasi_item['exp']['pos_modire_vahede_darkhat']['positionID'] is None or \
                    morekhasi_item['exp']['pos_modire_vahede_darkhat_after_sign']['positionID'] is None:
                top_chart = Chart.objects.get(id = morekhasi_item['exp']['pos_vahede_darkhat']['chartID'])
                modiresh_position = PositionsDocument.objects.filter(chartID = top_chart.top.id, userID__ne = None).first()
                if modiresh_position:
                    modiresh_position = PositionDocumentLessDataSerializer(instance=modiresh_position).data
                    morekhasi_item['exp']['pos_modire_vahede_darkhat'] = modiresh_position
                    morekhasi_item['exp']['pos_modire_vahede_darkhat_after_sign'] = modiresh_position

            dt = dict(
                dateOfPost=datetime.now(),
                creator_position=current_pos.positionID,
                exp=morekhasi_item['exp']
            )
            ser = MorekhasiSaatieSerializers(data=dt)
            ser.is_valid(raise_exception=True)
            ser.save()
            return Response(ser.data)

        morekhasi_item = request.data

        if request.data.get('exp').get('confirm_type') == 2:
            instance = MorekhasiSaati.objects.get(id=request.data.get('id'))
            insd = MorekhasiSaatieSerializers(instance=instance).data
            if instance.exp['pos_modire_vahede_darkhat'].get('is_signed') == True:
                return Response({"message": "از قبل این مرخصی امضا شده است"},
                                status=status.HTTP_400_BAD_REQUEST)
            allow_to_sign = False
            who_signed = None
            if instance.exp['pos_modire_vahede_darkhat'].get('positionID') == current_pos.positionID:
                allow_to_sign = True
                who_signed = instance.exp['pos_modire_vahede_darkhat']
            for i in instance.exp['pos_emaza_konandeha']:
                if i['positionID'] == current_pos.positionID:
                    allow_to_sign = True
                    who_signed = i

            if allow_to_sign == False:
                return Response({"message": "شما مجاز به این امضا نیستید"},
                                status=status.HTTP_400_BAD_REQUEST)
            insd['exp']['pos_modire_vahede_darkhat'] = who_signed
            insd['exp']['pos_modire_vahede_darkhat']['is_signed'] = True
            insd['exp']['pos_modire_vahede_darkhat']['position_id'] = current_pos.positionID
            insd['exp']['pos_modire_vahede_darkhat']['date_of_signed'] = datetime.now()
            instance.update(exp={})
            ser = MorekhasiSaatieSerializers(data={'exp': insd['exp']},
                                             instance=MorekhasiSaati.objects.get(id=request.data.get('id')),
                                             partial=True, )
            ser.is_valid(raise_exception=True)
            ser.save()
            return Response(ser.data)

        if request.data.get('exp').get('confirm_type') == 99:
            instance = MorekhasiSaati.objects.get(id=request.data.get('id'))
            insd = MorekhasiSaatieSerializers(instance=instance).data
            if instance.exp['pos_modire_vahede_darkhat'].get('is_signed') == True:
                return Response({"message": "از قبل این مرخصی امضا شده است"},
                                status=status.HTTP_400_BAD_REQUEST)
            allow_to_sign = False
            who_signed = None
            if instance.exp['pos_modire_vahede_darkhat'].get('positionID') == current_pos.positionID:
                allow_to_sign = True
                who_signed = instance.exp['pos_modire_vahede_darkhat']
            for i in instance.exp['pos_emaza_konandeha']:
                if i['positionID'] == current_pos.positionID:
                    allow_to_sign = True
                    who_signed = i

            if allow_to_sign == False:
                return Response({"message": "شما مجاز به این امضا نیستید"},
                                status=status.HTTP_400_BAD_REQUEST)
            insd['exp']['pos_modire_vahede_darkhat'] = who_signed
            insd['exp']['pos_modire_vahede_darkhat']['is_signed'] = False
            insd['exp']['pos_modire_vahede_darkhat']['is_disagree'] = True
            insd['exp']['pos_modire_vahede_darkhat']['position_id'] = current_pos.positionID
            insd['exp']['pos_modire_vahede_darkhat']['date_of_signed'] = datetime.now()
            instance.update(exp={})
            ser = MorekhasiSaatieSerializers(data={'exp': insd['exp']},
                                             instance=MorekhasiSaati.objects.get(id=request.data.get('id')),
                                             partial=True, )
            ser.is_valid(raise_exception=True)
            ser.save()
            return Response(ser.data)

        if request.data.get('exp').get('confirm_type') == 3:
            instance = MorekhasiSaati.objects.get(id=request.data.get('id'))

            if instance.exp['pos_masoole_edari'].get('is_signed') == True:
                return Response({"message": "از قبل این مرخصی امضا شده است"},
                                status=status.HTTP_400_BAD_REQUEST)

            if instance.exp['pos_modire_mali'].get('is_signed') == True:
                return Response({"message": "از قبل این مرخصی امضا شده است"},
                                status=status.HTTP_400_BAD_REQUEST)

            if not current_pos.positionID in [
                instance.exp['pos_modire_mali'].get('positionID'),
                instance.exp['pos_masoole_edari'].get('positionID'), ]:
                return Response({"message": "شما مجاز به این امضا نیستید"},
                                status=status.HTTP_400_BAD_REQUEST)

            if instance.exp['pos_modire_mali'].get('positionID') == current_pos.positionID:
                morekhasi_item['exp']['pos_modire_mali']['is_signed'] = True
                morekhasi_item['exp']['pos_modire_mali'][
                    'position_id'] = GetPositionViewset().GetCurrentPositionDocumentInstance(request).positionID
                morekhasi_item['exp']['pos_modire_mali']['date_of_signed'] = datetime.now()
                ser = MorekhasiSaatieSerializers(data={'exp': morekhasi_item['exp']}, instance=instance, partial=True)
                ser.is_valid(raise_exception=True)
                ser.save()
                return Response(ser.data)
            if instance.exp['pos_masoole_edari'].get('positionID') == current_pos.positionID:
                morekhasi_item['exp']['pos_masoole_edari']['is_signed'] = True
                morekhasi_item['exp']['pos_masoole_edari'][
                    'position_id'] = GetPositionViewset().GetCurrentPositionDocumentInstance(request).positionID
                morekhasi_item['exp']['pos_masoole_edari']['date_of_signed'] = datetime.now()
                ser = MorekhasiSaatieSerializers(data={'exp': morekhasi_item['exp']}, instance=instance, partial=True)
                ser.is_valid(raise_exception=True)
                ser.save()
                return Response(ser.data)

    def list(self, request, *args, **kwargs):
        result = super(MorekhasiSaatiViewSet, self).list(request, *args, **kwargs)
        for r in result.data['data']:

            r['status'] = ''
            if r['exp'].get('pos_vahede_darkhat', {}).get('is_signed', None):
                r['status'] = 'منتظر امضای متقاضی'
            if r['exp'].get('pos_vahede_darkhat', {}).get('is_signed') == True:
                r['status'] = 'منتظر امضای مدیر متقاضی'
            if r['exp'].get('pos_modire_vahede_darkhat', {}).get('is_signed') == True:
                r['status'] = 'منتظر امضای مدیر یا مسئول ادرای' + '(موافق شده)'
            if r['exp'].get('pos_modire_mali', {}).get('is_signed') == True:
                r['status'] = 'تایید شده'
            if r['exp'].get('pos_masoole_edari', {}).get('is_signed') == True:
                r['status'] = 'تایید شده'
            if r['exp'].get('pos_modire_vahede_darkhat', {}).get('is_disagree') == True:
                r['status'] = 'رد شده'
            if r['exp'].get('mizan', None) == None:
                r['exp']['mizan'] = ''
            if r['exp'].get('dateofmorekhasi', None) == None:
                r['exp']['dateofmorekhasi'] = ''
            if r['exp'].get('az', None) == None:
                r['exp']['az'] = ''
            if r['exp'].get('taa', None) == None:
                r['exp']['taa'] = ''

        return result

    @list_route(methods=['post'])
    def post_entezamat(self, request, *args, **kwargs):
        dt = request.data
        instance = self.queryset.get(id=dt['id'])
        pid = GetPositionViewset().GetCurrentPositionDocumentInstance(request)

        exp = instance.exp
        if dt['typeof'] == 1:
            exp['exit_confirm'] = True
            exp['exit_confirm_date'] = datetime.now()
            exp['exit_confirm_positionID'] = pid.positionID

        if dt['typeof'] == 2:
            exp['comeback_confirm'] = True
            exp['comeback_confirm_date'] = datetime.now()
            exp['comeback_confirm_positionID'] = pid.positionID

        sr = self.serializer_class(instance=instance, data={'exp': exp}, partial=True)
        sr.is_valid(raise_exception=True)
        sr.save()
        return Response(sr.data)

    @list_route(methods=['get'])
    def get_entezamat(self, request, *args, **kwargs):
        dt = request.query_params.get('dt', None)
        if dt == '':
            dt = mil_to_sh(datetime.now())
        if not is_valid_shamsi_date(dt):
            return Response({"message": "تاریخ را به درستی وارد کنید"},
                            status=status.HTTP_400_BAD_REQUEST)
        q1 = Q(exp__dateofmorekhasi=dt)
        q2 = Q(exp__pos_modire_vahede_darkhat__is_signed=True)
        q3 = q1 & q2
        result = MorekhasiSaati.objects
        result = result.filter(q3)
        result = self.serializer_class(instance=result, many=True).data
        return Response(result)

    @list_route(methods=['get'])
    def get_edari(self, request, *args, **kwargs):
        dt = request.query_params.get('dt', None)
        if dt == '':
            dt = mil_to_sh(datetime.now())
        if dt == 'undefined':
            dt = mil_to_sh(datetime.now())
        if not is_valid_shamsi_date(dt):
            return Response({"message": "تاریخ را به درستی وارد کنید"},
                            status=status.HTTP_400_BAD_REQUEST)
        q1 = Q(exp__dateofmorekhasi=dt)
        q2 = Q(exp__pos_modire_vahede_darkhat__is_signed=True)
        q3 = q1 & q2
        result = MorekhasiSaati.objects
        result = result.filter(q3)
        result = self.serializer_class(instance=result, many=True).data

        connection = Connections.objects.get(databaseName="Kara")
        connection = ConnectionsViewSet().getConnection(connection)
        pool = ConnectionPools.objects.get(name="GetTaradod")
        for r in result:
            sql = pool.sqls[0]["code"]
            sql = sql.replace("<:codepersonnel:>", r['exp'].get('pos_vahede_darkhat', {}).get('personnel_code', '-1'))
            sql = sql.replace("<:date:>", dt.replace('/', ''))
            connection.execute(sql)
            sql_res = connection.fetchall()
            sql_res = convert_sqlresultstr_to_valid_str(sql_res)
            sql_res = convert_sqlresultstr_to_valid_numbers(sql_res)
            r['exp']['pos_vahede_darkhat']['karaweb_times'] = sql_res

        return Response(result)

    @list_route(methods=['get'])
    def make_change(self, request, *args, **kwargs):
        dt = request.query_params
        instance = self.queryset.get(id=dt['ins'])
        pid = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        connection = Connections.objects.get(databaseName="Kara")
        connection = ConnectionsViewSet().getConnectionAutoCommit(connection)
        pool = ConnectionPools.objects.get(name="UpdateTaradod")
        sql = pool.sqls[0]["code"]
        sql = sql.replace("<:idOfData:>", dt['dt'])
        sql = sql.replace("<:idOfStatus:>", '17')
        connection.execute(sql)
        connection.close()

        exp = instance.exp
        if exp.get('karaweb_approves', None) is None:
            exp['karaweb_approves'] = []
        ccc = []
        found = False

        new_res = query(exp['karaweb_approves']).where(lambda x: x['id'] != int(dt['dt'])).to_list()
        new_res.append({
            'id': int(dt['dt']),
            'positionID': pid.positionID,
            'dateofpost': datetime.now()
        })
        exp['karaweb_approves'] = new_res
        ser = self.serializer_class(instance=instance, data={'exp': exp}, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    @list_route(methods=['get'])
    def make_unchange(self, request, *args, **kwargs):
        dt = request.query_params
        instance = self.queryset.get(id=dt['ins'])
        pid = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        connection = Connections.objects.get(databaseName="Kara")
        connection = ConnectionsViewSet().getConnectionAutoCommit(connection)
        pool = ConnectionPools.objects.get(name="UpdateTaradod")
        sql = pool.sqls[0]["code"]
        sql = sql.replace("<:idOfData:>", dt['dt'])
        sql = sql.replace("<:idOfStatus:>", '0')
        connection.execute(sql)
        connection.close()

        exp = instance.exp
        if exp.get('karaweb_approves', None) is None:
            exp['karaweb_approves'] = []
        ccc = []
        found = False

        new_res = query(exp['karaweb_approves']).where(lambda x: x['id'] != int(dt['dt'])).to_list()
        new_res.append({
            'id': int(dt['dt']),
            'positionID': pid.positionID,
            'dateofpost': datetime.now()
        })
        exp['karaweb_approves'] = new_res
        final = []
        for d in exp['karaweb_approves']:
            if int(d['id']) != int(dt['dt']):
                final.append(d)
        exp['karaweb_approves'] = final
        ser = self.serializer_class(instance=instance, data={'exp': exp}, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)
