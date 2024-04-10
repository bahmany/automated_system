from dateutil import parser

from datetime import datetime
from itertools import chain

import bs4
from asq.initiators import query
from django.contrib.auth.models import Group
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.CompaniesManagment.Connections.models import ConnectionPools, Connections
from amspApp.CompaniesManagment.Connections.viewes.ConnectionsViews import ConnectionsViewSet
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh_with_time, mil_to_sh, sh_to_mil, get_date_str
from amspApp.Letter.views.LetterView import LetterViewSet
from amspApp.MyProfile.models import Profile
from amspApp.MyProfile.serializers.ProfileSerializer import ProfileSerializer
from amspApp.Notifications.models import Notifications
from amspApp.Notifications.serializers.NotificationSerializer import NotificationsSerializer
from amspApp.Notifications.views.NotificationView import NotificationViewSet
from amspApp.Sales.models import HavalehForooshConv, HavalehForooshSigns, \
    HavalehForooshApprove, HamkaranHavaleForoosh, HamkaranHavaleForooshOrderApprove, HamkaranSalesCustomerProfile, \
    HamkaranCustomerAddress, HavalehForooshs, lastHavalehForooshID
from amspApp.Sales.serializers.CustomerProfileSerializer import HamkaranSalesCustomerProfileSerializer, \
    HamkaranCustomerAddressSerializer
from amspApp.Sales.serializers.HavalehForooshSerializer import HavalehForooshSerializer, HavalehForooshConvSerializer, \
    HavalehForooshSignSerializer, HavalehForooshApproveSerializer
from amspApp.Sales.views.endOfHavaleRecieversDict import recs, newLetter, nahieh_1_tolid, nahieh_2_tolid, \
    nahieh_1_foroosh, nahieh_2_foroosh
from amspApp._Share.ListPagination import DetailsPagination
from amspApp.amspUser.models import MyUser
from amspApp.amspUser.views.UserView import UserViewSet
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset
from amspApp.tasks import sendSMS


class HavalehForooshViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = HamkaranHavaleForoosh.objects.all()
    serializer_class = HavalehForooshSerializer
    pagination_class = DetailsPagination

    """
    permitted group for coming to exitis :
    group_havalehforoosh_permited_to_view

    qrcode signature format :
    type = qrexit_
    qrexit_ + exit_id + _ + positionID

    steps:
     group_havalehforoosh_start
     group_havalehforoosh_permited_to_view_1
     group_havalehforoosh_permited_to_view_2
     group_havalehforoosh_permited_to_view_3
     group_havalehforoosh_permited_to_view_4
     group_havalehforoosh_permited_to_view_5
     group_havalehforoosh_end
     
    """

    def list(self, request, *args, **kwargs):

        result = super(HavalehForooshViewSet, self).list(request, args, kwargs)
        return result

    @detail_route(methods=["GET"])
    def nextRecord(self, request, *args, **kwargs):
        id = kwargs.get("id")
        fff = HamkaranHavaleForoosh.objects.filter(id__gt=id).order_by("id").first()
        if not fff:
            return Response({"id": ""})
        return Response({'id': str(fff.id)})

    @detail_route(methods=["GET"])
    def prevRecord(self, request, *args, **kwargs):
        id = kwargs.get("id")
        fff = HamkaranHavaleForoosh.objects.filter(id__lt=id).order_by("-id").first()
        if not fff:
            return Response({"id": ""})
        return Response({'id': str(fff.id)})

    def getVaziat(self, step):

        if step == 1:
            return "منتظر امضای حسابداری فروش"
        if step == 2:
            return "منتظر امضای مدیر بازرگانی"
        if step == 3:
            return "منتظر تایید تولید مدیر مالی"
        if step == 4:
            return "منتظر تایید تولید مدیر عامل"
        if step == 5:
            return "منتظر تایید خروج مدیر عامل و مالی"
        if step == 6:
            return "منتظر تایید خروج مدیر عامل"
        if step == 7:
            return "دارای تاییده خروج"

    @list_route(methods=["GET"])
    def getAggr(self, request, *args, **kwargs):

        if request.user.groups.filter(name="group_havalehforoosh_permited_to_view").count() == 0:
            return Response({})
        havals = []
        if request.query_params.get('archive'):
            if request.query_params.get('archive') == "true":
                havals = []
                pass
            else:
                havals = [
                    x.havalehForooshLink for x in HamkaranHavaleForooshOrderApprove.objects.filter(
                        item__closed=None,
                        dateOfPost__gte=datetime.strptime(sh_to_mil("1400/01/01"), "%Y/%m/%d")
                    )
                ]
        else:
            havals = [x.havalehForooshLink for x in HamkaranHavaleForooshOrderApprove.objects.filter(item__closed=None,
                                                                                                     dateOfPost__gte=datetime.strptime(
                                                                                                         sh_to_mil(
                                                                                                             "1400/01/01"),
                                                                                                         "%Y/%m/%d"))]

        # except:
        #     pass
        page_size = int(request.query_params.get("page_size", "20"))
        page = int(request.query_params.get("page", "1"))
        search = ""
        search = request.query_params.get("search", "")
        searchDict = {}
        if search != "":
            searchDict["$or"] = [
                {"customerName": {"$regex": search}},
                {"tarikheSodoor": {"$regex": search}},

            ]
            if search.isdigit():
                searchDict["$or"].append(
                    {"mizanAvaliehSefaresh": int(search)},
                )

                searchDict["$or"].append(
                    {"Number": int(search)},
                )

        if len(havals) > 0:
            searchDict["$and"] = [
                {"_id": {"$in": query(havals).select(lambda x: x.id).distinct().to_list()}},
                {'vaziat': {'$nin': [3,4,5,6]}}  # این خط منجر به حذف منتظر مدیرعامل می شود
            ]
            if request.query_params.get('archive','') == "true":   # در صورتی که تیک آرشیو زده شود تمامی آیتم ها نماتیش داده می شود
                searchDict["$and"] = [searchDict["$and"][0]]

        counter = list(HamkaranHavaleForoosh.objects.aggregate(
            {"$match": searchDict}, {"$count": "countOf"}))
        if len(counter) == 0:
            return Response({})
        totalCount = counter[0]["countOf"]
        data = HamkaranHavaleForoosh.objects.aggregate(
            {"$match": searchDict},
            {"$sort": {"ID": -1}},
            {"$limit": ((page - 1) * page_size) + page_size},
            {"$skip": (page - 1) * page_size})

        data = list(data)
        for d in data:
            d['mizanAvaliehSefaresh'] = query(
                HamkaranHavaleForooshOrderApprove.objects.filter(havalehForooshLink=d['_id'])[0].item['items']).sum(
                lambda x: x['OrderItemQuantity'])
            allApprove = [x['id'] for x in
                          HamkaranHavaleForooshOrderApprove.objects.filter(havalehForooshLink=d['_id'])]
            lastSigns = list(
                HavalehForooshSigns.objects.filter(HavalehForooshApproveLink__in=allApprove).order_by("-whichStep"))
            if len(lastSigns) == 0:
                d['vaziatInt'] = 1
                d['vaziat'] = "منتظر امضای صادر کننده"
            else:

                # if lastSigns[0].whichStep == 5:
                #     d['vaziatInt'] = 5
                #     d['vaziat'] = "تایید شده"
                # else:
                d['vaziat_id'] = d['vaziat']
                d['vaziat'] = self.getVaziat(lastSigns[0].whichStep)

        # for d in data :
        #     signCount = HavalehForooshSigns.objects.filter(HavalehForooshApproveLink = d['_id']).count()
        #     d['signCount'] = signCount
        #     commentCount = HavalehForooshConv.objects.filter(HavalehForooshApproveLink = d['_id']).count()
        #     d['commentCount'] = commentCount
        #
        #     d['vaziat'] = self.getVaziat(d)

        result = {
            "next": "/api/v1/havakehForoosh/getAggr/?page_size=%d&page=%d&search=%s" % (page_size, page + 1, search),
            "prev": "/api/v1/havakehForoosh/getAggr/?page_size=%d&page=%d&search=%s" % (
                page_size, page - 1, search) if page - 1 > 0 else None,
            "first": "/api/v1/havakehForoosh/getAggr/?page_size=%d&page=%d&search=%s" % (page_size, 1, search),
            "last": "/api/v1/havakehForoosh/getAggr/?page_size=%d&page=%d&search=%s" % (
                page_size, int(totalCount / page_size) if totalCount > page_size else 1, search),
            "count": totalCount,
            "results": list(data)
        }

        return Response(result)

    @list_route(methods=["GET"])
    def getAggrForInbox(self,  request, *args, **kwargs):

        result = NotificationViewSet().get_all_unsings_foroosh(request, *args, **kwargs)
        list_of_ids = query(result).select(lambda x:x['id']).to_list()


        searchDict = {
            "_id":{"$in":list_of_ids}
        }
        # totalCount = counter[0]["countOf"]
        data = HamkaranHavaleForoosh.objects.aggregate(
            {"$match": searchDict},
            {"$sort": {"ID": -1}},)


        data = self.serializer_class(
            HamkaranHavaleForoosh.objects.filter(id__in=list_of_ids).order_by('-id'), many=True).data
        for d in data:
            d['_id'] = d['id']
            d['mizanAvaliehSefaresh'] = query(
                HamkaranHavaleForooshOrderApprove.objects.filter(havalehForooshLink=d['_id'])[0].item['items']).sum(
                lambda x: x['OrderItemQuantity'])
            allApprove = [x['id'] for x in
                          HamkaranHavaleForooshOrderApprove.objects.filter(havalehForooshLink=d['_id'])]
            lastSigns = list(
                HavalehForooshSigns.objects.filter(HavalehForooshApproveLink__in=allApprove).order_by("-whichStep"))
            if len(lastSigns) == 0:
                d['vaziatInt'] = 1
                d['vaziat'] = "منتظر امضای صادر کننده"
            else:

                d['vaziat_id'] = d['vaziat']
                d['vaziat'] = self.getVaziat(lastSigns[0].whichStep)


        result = {
            "next": None,
            "prev": None,
            "first": None,
            "last": None,
            "count": 0,
            "results": data
        }

        return Response(result)

    @detail_route(methods=["GET"])
    def getDetails(self, request, *args, **kwargs):
        id = kwargs["id"]
        instance = self.queryset.get(id=id)
        # check if user is from tolid department

        ApprovesIns = HamkaranHavaleForooshOrderApprove.objects.filter(havalehForooshLink=id).order_by("id")
        ApprovesIns = HavalehForooshApproveSerializer(instance=ApprovesIns, many=True).data

        for a in ApprovesIns:
            signsIns = HavalehForooshSigns.objects.filter(HavalehForooshApproveLink=a['id'])
            signsIns = HavalehForooshSignSerializer(instance=signsIns, many=True).data
            a['signs'] = signsIns
            for aa in a['signs']:
                ins = PositionsDocument.objects.filter(positionID=aa['positionID']).first()
                if ins:
                    aa['positionName'] = ins['profileName']
                    aa['positionchartName'] = ins['chartName']
            # detecting duplicated signs
            if len(a['signs']) > 0:
                dup_signs = query(a['signs']).group_by(lambda x: x['HavalehForooshApproveLink'],
                                                       result_selector=lambda key, group: {
                                                           'key': key,
                                                           'group': query(group).group_by(lambda x: x['whichStep'],
                                                                                          result_selector=lambda key,
                                                                                                                 xgroup: {
                                                                                              'whiscStep': key,
                                                                                              'firstOf': xgroup.first()}
                                                                                          ).to_list()
                                                       }
                                                       ).to_list()
                a['signs'] = [x['firstOf'] for x in dup_signs[0]['group']]

            inss = HavalehForooshConv.objects.filter(HavalehForooshApproveLink=a['id']).order_by("id")
            inss = HavalehForooshConvSerializer(instance=inss, many=True).data
            for c in inss:
                ps = PositionsDocument.objects.filter(positionID=c['positionID'])
                if len(ps) > 0:
                    ps = ps[0]
                    c["positionName"] = ps.profileName
                    c["positionSemat"] = ps.chartName
                    c["avatar"] = ps.avatar.replace("thmum50CC", "thmum100")
                else:
                    c["positionName"] = "حذف شده"
                    c["positionSemat"] = "حذف شده"
                    c["avatar"] = "/static/images/avatar_empty.jpg"
            a['convs'] = inss

        c = 1
        for a in ApprovesIns:
            if c != 1:
                posiData = self.getPositionDocByPosID(a['positionID'])
                a['positionName'] = posiData['positionName']
                a['positionchartName'] = posiData['positionchartName']
                a['positionAvatar'] = posiData['positionavatar'].replace("thmum50CC", "thmum100")

            customerNumber = str(a['havalehForooshLink']['exp']['CustomerCode'])
            customerInstance = HamkaranSalesCustomerProfile.objects.get(exp__Number=str(customerNumber))

            customerAddress = HamkaranCustomerAddress.objects.filter(exp__CustomerRef=customerInstance.CustomerID)
            customerSerializer = HamkaranSalesCustomerProfileSerializer(instance=customerInstance).data
            customerAddressSerializer = HamkaranCustomerAddressSerializer(instance=customerAddress, many=True).data
            a['customerInfo'] = customerSerializer
            a['customerAddresses'] = customerAddressSerializer

        Notifications.objects.filter(
            userID=request.user.id,
            extra__dbid=id
        ).delete()

        def seeer():
            return {
                'dep': '',
                'signer_name': '',
                'comment': '',
                'signer_chart': '',
                'signer_sh_date': '',
                'tolid_bela_maneh': False,

            }

        dt = {}
        dt['s1'] = seeer()
        dt['s2'] = seeer()
        dt['s3'] = seeer()
        dt['s4'] = seeer()
        dt['s5'] = seeer()
        dt['s1']['dep'] = 'صادرکننده'
        dt['s2']['dep'] = 'حسابداری فروش'
        dt['s3']['dep'] = 'رییس فروش'
        dt['s4']['dep'] = 'مالی'
        dt['s5']['dep'] = 'مدیرعامل'
        signs = ApprovesIns[0]['signs']

        s_1 = query(signs).where(lambda x: x['whichStep'] == 1).to_list()
        if len(s_1) > 0:
            dt['s1']['signer_name'] = s_1[0]['positionName']
            dt['s1']['signer_chart'] = s_1[0]['positionchartName']
            s_1[0]['dateOfPost'] = s_1[0]['dateOfPost']+".0001" if s_1[0]['dateOfPost'].find('.')==-1 else s_1[0]['dateOfPost']
            dt['s1']['signer_sh_date'] = get_date_str(
                datetime.strptime(s_1[0]['dateOfPost'].replace("T", " "), "%Y-%m-%d %H:%M:%S.%f"))
            dt['s1']['comment'] = s_1[0]['comment']
            dt['s1']['tolid_bela_maneh'] = False

        s_2 = query(signs).where(lambda x: x['whichStep'] == 2).to_list()
        if len(s_2) > 0:
            dt['s2']['signer_name'] = s_2[0]['positionName']
            dt['s2']['signer_chart'] = s_2[0]['positionchartName']
            s_2[0]['dateOfPost'] = s_2[0]['dateOfPost']+".0001" if s_2[0]['dateOfPost'].find('.')==-1 else s_2[0]['dateOfPost']

            dt['s2']['signer_sh_date'] = get_date_str(
                datetime.strptime(s_2[0]['dateOfPost'].replace("T", " "), "%Y-%m-%d %H:%M:%S.%f"))
            dt['s2']['comment'] = s_2[0]['comment']
            dt['s2']['tolid_bela_maneh'] = False

        s_3 = query(signs).where(lambda x: x['whichStep'] == 3).to_list()
        if len(s_3) > 0:
            dt['s3']['signer_name'] = s_3[0]['positionName']
            dt['s3']['signer_chart'] = s_3[0]['positionchartName']
            s_3[0]['dateOfPost'] = s_3[0]['dateOfPost']+".0001" if s_3[0]['dateOfPost'].find('.')==-1 else s_3[0]['dateOfPost']

            dt['s3']['signer_sh_date'] = get_date_str(
                datetime.strptime(s_3[0]['dateOfPost'].replace("T", " "), "%Y-%m-%d %H:%M:%S.%f"))
            dt['s3']['comment'] = s_3[0]['comment']
            dt['s3']['tolid_bela_maneh'] = False

        s_4 = query(signs).where(lambda x: x['whichStep'] == 4).to_list()
        if len(s_4) > 0:
            dt['s4']['signer_name'] = s_4[0]['positionName']
            dt['s4']['signer_chart'] = s_4[0]['positionchartName']
            s_4[0]['dateOfPost'] = s_4[0]['dateOfPost']+".0001" if s_4[0]['dateOfPost'].find('.')==-1 else s_4[0]['dateOfPost']

            dt['s4']['signer_sh_date'] = get_date_str(
                datetime.strptime(s_4[0]['dateOfPost'].replace("T", " "), "%Y-%m-%d %H:%M:%S.%f"))
            dt['s4']['comment'] = s_4[0]['comment']
            dt['s4']['tolid_bela_maneh'] = False
            dt['s4']['has_exit_confirm'] = False
            dt['s4']['has_exit_confirm_date'] = ""
            dt['s4']['has_exit_confirm_comment'] = ""
            s4_approve_exit = query(signs).where(lambda x: x['whichStep'] == 6).to_list()
            if (len(s4_approve_exit)) > 0:
                dt['s4']['has_exit_confirm'] = True
                s4_approve_exit[0]['dateOfPost'] = s4_approve_exit[0]['dateOfPost'] + ".0001" if s4_approve_exit[0]['dateOfPost'].find('.') == -1 else s4_approve_exit[0]['dateOfPost']
                dt['s4']['has_exit_confirm_date'] = get_date_str(
                    datetime.strptime(s4_approve_exit[0]['dateOfPost'].replace("T", " "), "%Y-%m-%d %H:%M:%S.%f"))
                dt['s4']['has_exit_confirm_comment'] = s4_approve_exit[0]['comment']

        s_5 = query(signs).where(lambda x: x['whichStep'] == 5).to_list()
        if len(s_5) > 0:
            dt['s5']['signer_name'] = s_5[0]['positionName']
            dt['s5']['signer_chart'] = s_5[0]['positionchartName']
            s_5[0]['dateOfPost'] = s_5[0]['dateOfPost']+".0001" if s_5[0]['dateOfPost'].find('.')==-1 else s_5[0]['dateOfPost']

            dt['s5']['signer_sh_date'] = get_date_str(
                datetime.strptime(s_5[0]['dateOfPost'].replace("T", " "), "%Y-%m-%d %H:%M:%S.%f"))
            dt['s5']['comment'] = s_5[0]['comment']
            dt['s5']['tolid_bela_maneh'] = False
            dt['s5']['has_exit_confirm'] = False
            dt['s5']['has_exit_confirm_date'] = ""
            dt['s5']['has_exit_confirm_comment'] = ""
            s4_approve_exit = query(signs).where(lambda x: x['whichStep'] == 6).to_list()
            if (len(s4_approve_exit)) > 0:
                dt['s5']['has_exit_confirm'] = True
                dt['s5']['has_exit_confirm_date'] = get_date_str(
                    datetime.strptime(s4_approve_exit[0]['dateOfPost'].replace("T", " "), "%Y-%m-%d %H:%M:%S.%f"))
                dt['s5']['has_exit_confirm_comment'] = s4_approve_exit[0]['comment']
        ApprovesIns[0]['sign_for_mobile'] = dt
        return Response(ApprovesIns)

    @list_route(methods=["GET"])
    def getDetailsApprove(self, request, *args, **kwargs):
        appriveID = request.query_params.get("ai")
        stepID = request.query_params.get("s")
        ApprovesIns = HavalehForooshApprove.objects.get(id=appriveID)
        ApprovesIns = HavalehForooshApproveSerializer(instance=ApprovesIns).data

        signsIns = HavalehForooshSigns.objects.filter(HavalehForooshApproveLink=ApprovesIns['id'])
        signsIns = HavalehForooshSignSerializer(instance=signsIns, many=True).data
        ApprovesIns['signs'] = signsIns
        for aa in ApprovesIns['signs']:
            ins = PositionsDocument.objects.filter(positionID=aa['positionID']).first()
            if ins:
                aa['positionName'] = ins['profileName']
                aa['positionchartName'] = ins['chartName']

        return Response(ApprovesIns)

    def isHavalehFinished(self, approve):
        havalehForooshes = HavalehForooshApprove.objects.filter(
            havalehForooshLink=approve['havalehForooshLink']).order_by("id")
        havalehForooshes = HavalehForooshApproveSerializer(instance=havalehForooshes, many=True).data
        otherDts = []
        for a in havalehForooshes[0]['item']['items']:
            a['AQty'] = 0
        for a in havalehForooshes:
            otherDts += a['item']['items']

        firstDts = query(havalehForooshes[0]['item']['items']).group_by(
            lambda x: x['PartCode'], result_selector=lambda key, group: {'PartCode': key, 'sumOfQty': query(group).sum(
                lambda x: x['Qty'])}).to_list()

        otherDts = query(otherDts).group_by(
            lambda x: x['PartCode'], result_selector=lambda key, group: {'PartCode': key, 'sumOfAQty': query(group).sum(
                lambda x: x['AQty'])}).to_list()
        aa = approve['item']['items']
        thisDts = query(aa).group_by(
            lambda x: x['PartCode'], result_selector=lambda key, group: {'PartCode': key, 'sumOfAQty': query(group).sum(
                lambda x: x['AQty'])}).to_list()
        remains = []
        for f in firstDts:
            sumOf = query(otherDts).where(lambda x: x['PartCode'] == f['PartCode']).sum(lambda x: x['sumOfAQty'])
            if (f['sumOfQty'] - sumOf) > 0:
                sumOfNew = query(thisDts).where(lambda x: x['PartCode'] == f['PartCode']).sum(lambda x: x['sumOfAQty'])
                if ((f['sumOfQty'] - sumOf) - sumOfNew) > 0:
                    remains.append({
                        'PartCode': f['PartCode'],
                        'remain_amount': (f['sumOfQty'] - sumOf) - sumOfNew
                    })

        return dict(
            result=len(remains) == 0,
            details=remains
        )

    def getFirstInstance(self, approveID):
        ApprovesIns = HavalehForooshApprove.objects.get(id=approveID)
        ApprovesInses = HavalehForooshApprove.objects.filter(
            havalehForooshLink=ApprovesIns.havalehForooshLink).order_by("id").first()
        return ApprovesInses

    def getFirstItemByApproveID(self, approveID):
        ApprovesInses = self.getFirstInstance(approveID)
        firstData = HavalehForooshApproveSerializer(instance=ApprovesInses).data
        idOfFirstData = firstData['id']
        # we should get AQty of first data to zero when user select to modify Qty
        firstData = query(firstData['item']['items']).group_by(
            lambda x: x['PartCode'], result_selector=lambda key, group: {'PartCode': key, 'sumOfQty': query(group).sum(
                lambda x: x['Qty'])}).to_list()
        return firstData

    def calcRemainQty(self, approve, itemOfQty):
        firstIns = HavalehForooshApprove.objects.filter(havalehForooshLink=approve['havalehForooshLink']).order_by(
            "id").first()
        firstInsItems = firstIns.item['items']
        inss = HavalehForooshApprove.objects.filter(
            havalehForooshLink=approve['havalehForooshLink'], item__thisApproveFinished=True)
        aqty = 0
        qty = 0
        for ins in inss:
            for item in ins['item']['items']:
                if item['PartCode'] == itemOfQty['PartCode']:
                    aqty = aqty + item['AQty']
        sumQty = query(firstInsItems).where(lambda x: x['PartCode'] == itemOfQty['PartCode']).sum(lambda x: x['Qty'])
        return sumQty - aqty

    @detail_route(methods=["GET"])
    def startFromRemaining(self, request, *args, **kwargs):
        approveID = kwargs['id']

        hfs = HavalehForooshApprove.objects.filter(havalehForooshLink=kwargs['id'],
                                                   item__thisApproveFinished=True).order_by("id")
        hfs = HavalehForooshApproveSerializer(instance=hfs, many=True).data
        if len(hfs) == 0:
            firstIns = HavalehForooshApprove.objects.filter(havalehForooshLink=kwargs['id']).order_by("id").first()
            firstIns = HavalehForooshApproveSerializer(instance=firstIns).data
            firstQty = query(firstIns['item']['items']).sum(lambda x: x['Qty'])
        if len(hfs) == 1:
            firstIns = hfs[0]
            firstQty = query(firstIns['item']['items']).sum(lambda x: x['Qty'])
        if len(hfs) > 1:
            firstIns = HavalehForooshApprove.objects.filter(havalehForooshLink=kwargs['id']).order_by("-id").first()
            firstIns = HavalehForooshApproveSerializer(instance=firstIns).data
            firstQty = query(firstIns['item']['items']).sum(lambda x: x['Qty'])

        hfs = [x['item']['items'] for x in hfs]
        hfs = list(chain(*hfs))
        #
        # firstIns = HavalehForooshApprove.objects.filter(havalehForooshLink=kwargs['id']).order_by("id").first()
        # firstIns = HavalehForooshApproveSerializer(instance=firstIns).data
        # firstQty = query(firstIns['item']['items']).sum(lambda x: x['Qty'])
        #

        otherAQty = query(hfs).sum(lambda x: x['AQty'])
        for f in firstIns['item']['items']:
            cc = query(firstIns['item']['items']).where(lambda x: x['PartCode'] == f['PartCode']).sum(
                lambda x: x['Qty'])
            aa = query(hfs).where(lambda x: x['PartCode'] == f['PartCode']).sum(lambda x: x['AQty'])
            f['Qty'] = cc - aa
            f['AQty'] = f['Qty']
            f['MQty'] = f['Qty']
        firstIns['item']['thisApproveFinished'] = False
        firstIns['item']['closed'] = False
        firstIns['item']['isAllFinished'] = False
        firstIns['item']['items'] = query(firstIns['item']['items']).where(lambda x: x['Qty'] > 0).to_list()
        del firstIns['id']
        ss = HavalehForooshApproveSerializer(data=firstIns)
        ss.is_valid(raise_exception=True)
        ss.save()
        return Response(ss.data)

    @detail_route(methods=["GET"])
    def isThisApproveFinishedTotaly(self, request, *args, **kwargs):

        current_instance = self.queryset.get(id=kwargs['id'])
        hfs = HamkaranHavaleForooshOrderApprove.objects.filter(havalehForooshLink=kwargs['id'],
                                                               item__closed=False).count()
        if hfs != 0:
            return Response({'result': True})

        hfs = HamkaranHavaleForooshOrderApprove.objects.filter(havalehForooshLink=kwargs['id'],
                                                               item__thisApproveFinished=True).order_by("id")
        hfs = HavalehForooshApproveSerializer(instance=hfs, many=True).data
        hfs = [x['item']['items'] for x in hfs]
        hfs = list(chain(*hfs))

        firstIns = HamkaranHavaleForooshOrderApprove.objects.filter(havalehForooshLink=kwargs['id']).order_by(
            "id").first()
        firstIns = HavalehForooshApproveSerializer(instance=firstIns).data
        firstQty = query(firstIns['item']['items']).sum(lambda x: x['OrderItemQuantity'])

        if firstIns['item'].get('closed') == None:
            return Response({'result': True})

        otherAQty = query(hfs).sum(lambda x: x['AQty'])
        return Response({"result": ((firstQty - otherAQty) == 0)})

    @list_route(methods=["POST"])
    def changesayer(self, request, *args, **kwargs):
        data = request.data
        approveIns = HamkaranHavaleForooshOrderApprove.objects.get(id=data['approve']['id'])
        # dt = query(approveIns.item['items']).where(lambda x:x['PoartCode'] == data['item']['PartCode']).first()
        item = approveIns.item
        for d in item['items']:
            if d['OrderItemProductNumber'] == data['item']['OrderItemProductNumber']:
                d['tarikheTahvil'] = data['item']['tarikheTahvil']
        sr = HavalehForooshApproveSerializer(instance=approveIns, data={"item": item}, partial=True)
        sr.is_valid(raise_exception=True)
        sr.save()
        return Response(sr.data)

    @list_route(methods=["POST"])
    def proveTolid(self, request, *args, **kwargs):
        if request.user.groups.all().filter(name="group_havalehforoosh_permited_to_tolid").count() == 0:
            return Response({"msg": "شما مجاز نیستید به تولید"})

        currentPos = GetPositionViewset().GetCurrentPositionDocumentInstance(self.request)
        convIns = HavalehForooshConv.objects.get(id=request.data.get("id"))
        exp = convIns.exp
        if convIns.exp.get("approve") == None:
            exp['approve'] = {
                "positionID": currentPos.positionID,
                "dateOfApprove": datetime.now(),
                "type": 1,  # means accept
                "avatar": currentPos.avatar,
                "name": currentPos.profileName + "-" + currentPos.chartName
            }
            ins = HavalehForooshConvSerializer(instance=convIns, data={"exp": dict(exp)}, partial=True)
            ins.is_valid(raise_exception=True)
            ins.save()
            return Response(ins.data)
        return None

    @list_route(methods=["POST"])
    def tolidBelaApply(self, request, *args, **kwargs):
        data = request.data
        approveIns = HavalehForooshApprove.objects.get(id=data['approve']['id'])
        # dt = query(approveIns.item['items']).where(lambda x:x['PoartCode'] == data['item']['PartCode']).first()
        # checking permission
        # permission to change this step is 5
        if request.user.groups.filter(name="group_havalehforoosh_permited_to_view_5").count() == 0:
            return Response({"type": "err", "msg": "شما مجوز تغییر این مورد را ندارید"})
        dt = approveIns.item
        dt['tolidBela'] = request.data.get('item', False)
        ser = HavalehForooshApproveSerializer(instance=approveIns, data={'item': dt}, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()

        return Response({"type": "ok", "msg": dt['tolidBela']})

    @list_route(methods=["POST"])
    def ersaleFactorApply(self, request, *args, **kwargs):
        data = request.data
        approveIns = HamkaranHavaleForooshOrderApprove.objects.get(id=data['approve']['id'])
        # dt = query(approveIns.item['items']).where(lambda x:x['PoartCode'] == data['item']['PartCode']).first()
        # checking permission
        # permission to change this step is 5
        if request.user.groups.filter(name="group_havalehforoosh_permited_to_view_1").count() == 0:
            return Response({"type": "err", "msg": "شما مجوز تغییر این مورد را ندارید"})
        dt = approveIns.item
        dt['ersaleFactor'] = request.data.get('item', False)
        ser = HavalehForooshApproveSerializer(instance=approveIns, data={'item': dt}, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({"type": "ok", "msg": dt['ersaleFactor']})

    @list_route(methods=["POST"])
    def khroojBelaApply(self, request, *args, **kwargs):
        data = request.data
        approveIns = HavalehForooshApprove.objects.get(id=data['approve']['id'])
        # dt = query(approveIns.item['items']).where(lambda x:x['PoartCode'] == data['item']['PartCode']).first()
        # checking permission
        # permission to change this step is 5
        if request.user.groups.filter(name="group_havalehforoosh_permited_to_view_5").count() == 0:
            return Response({"type": "err", "msg": "شما مجوز تغییر این مورد را ندارید"})
        dt = approveIns.item
        dt['khroojBela'] = request.data.get('item', False)
        ser = HavalehForooshApproveSerializer(instance=approveIns, data={'item': dt}, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()

        return Response({"type": "ok", "msg": dt['tolidBela']})

    @list_route(methods=["POST"])
    def changekarbord(self, request, *args, **kwargs):
        data = request.data
        approveIns = HamkaranHavaleForooshOrderApprove.objects.get(id=data['approve']['id'])
        # dt = query(approveIns.item['items']).where(lambda x:x['PoartCode'] == data['item']['PartCode']).first()
        item = approveIns.item
        for d in item['items']:
            if d['OrderItemProductNumber'] == data['item']['OrderItemProductNumber']:
                d['karbord'] = data['item']['karbord']
        sr = HavalehForooshApproveSerializer(instance=approveIns, data={"item": item}, partial=True)
        sr.is_valid(raise_exception=True)
        sr.save()
        return Response(sr.data)

    @list_route(methods=["POST"])
    def saveApprove(self, request, *args, **kwargs):
        approveID = request.query_params.get("ai")
        stepID = request.query_params.get("s")
        # getting first Qty
        data = request.data
        sentData = query(data['item']['items']).group_by(
            lambda x: x['PartCode'], result_selector=lambda key, group: {'PartCode': key, 'sumOfAQty': query(group).sum(
                lambda x: x['AQty'])}).to_list()

        # -----------------------------------------
        # -----------------------------------------
        # we should get AQty of first data to zero when user select to modify Qty
        firstData = self.getFirstItemByApproveID(approveID)
        # -----------------------------------------
        # -----------------------------------------
        # --- Getting Other AQty
        firstApprove = self.getFirstInstance(approveID)
        ApprovesInses = HavalehForooshApprove.objects.filter(
            havalehForooshLink=firstApprove.havalehForooshLink, id__ne=firstApprove.id).order_by("id")
        ApprovesInses = HavalehForooshApproveSerializer(instance=ApprovesInses, many=True).data

        otherDts = []
        for a in ApprovesInses:
            otherDts += a['item']['items']

        otherData = query(otherDts).group_by(
            lambda x: x['PartCode'], result_selector=lambda key, group: {'PartCode': key, 'sumOfAQty': query(group).sum(
                lambda x: x['AQty'])}).to_list()
        # -----------------------------------------
        # -----------------------------------------
        # -----------------------------------------
        bugs = []
        if len(otherDts) >= 0:  # it means this is the first suggestion
            for sd in sentData:
                for fd in firstData:
                    if sd['PartCode'] == fd['PartCode']:
                        if sd['sumOfAQty'] > fd['sumOfQty']:
                            bugs.append({
                                "PartCode": sd['PartCode'],
                                "reason": "مقدار وارد شده بیش از حواله است"
                            })
            if len(bugs) > 0:
                return Response(bugs)
            del data['id']
            havalehForooshClosed = HavalehForooshApprove.objects.filter(
                havalehForooshLink=firstApprove.havalehForooshLink)
            for h in havalehForooshClosed:
                item = h['item']
                item['closed'] = True
                item['isAllFinished'] = self.isHavalehFinished(data)['result']
                """
                here we should make first row AQty to zero to make it disable in other calcs
                """
                # for i in item['items']:
                #     i['AQty'] = 0
                hser = HavalehForooshApproveSerializer(instance=h, data={'item': item}, partial=True)
                hser.is_valid(raise_exception=True)
                hser.save()

            currentPosID = GetPositionViewset().GetCurrentPositionDocumentInstance(self.request).positionID
            data["positionID"] = currentPosID

            for d in data['item']['items']:
                d['Qty'] = self.calcRemainQty(data, d)
            data['item']['thisApproveFinished'] = False
            data['item']['closed'] = False
            data['item']['isAllFinished'] = False
            newApprove = HavalehForooshApproveSerializer(data=data)
            newApprove.is_valid(raise_exception=True)
            newApprove = newApprove.save()

            # send notification to all
            notification_reciever_group_name = "group_havalehforoosh"
            joint_users = Group.objects.filter(name__contains=notification_reciever_group_name)
            for j in joint_users:
                users = j.user_set.all()
                for u in users:
                    profileInstance = Profile.objects.filter(userID=u.id).first()
                    profileSerial = ProfileSerializer(instance=profileInstance).data
                    hfs = newApprove
                    fsi = newApprove.item['items'][0]
                    dt = {
                        'type': 7,
                        'typeOfAlarm': 3,
                        'informType': 5,
                        'userID': u.id,
                        'extra': {
                            'prevSignerName': profileSerial['extra']['Name'],
                            'prevSignerAvatar': profileSerial['extra']['profileAvatar']['url'],
                            'havalehForooshID': str(fsi['VchNo']),
                            'dbid': str(hfs.havalehForooshLink),
                            'customer': fsi['CstmrName'],
                            'qty': int(query(newApprove.item['items']).sum(lambda x: x['Qty'])),
                            'dateOf': mil_to_sh(fsi['VchDate'], splitter="/"),
                        }
                    }

                    ntSerial = NotificationsSerializer(data=dt)
                    ntSerial.is_valid(raise_exception=True)
                    ntSerial.save()

        # if len(otherDts) > 0:  # it means this is the first suggestion
        #     for sd in sentData:
        #         for fd in firstData:
        #             if sd['PartCode'] == fd['PartCode']:
        #                 if sd['sumOfAQty'] > fd['sumOfQty']:
        #                     bugs.append({
        #                         "PartCode": sd['PartCode'],
        #                         "reason": "مقدار وارد شده بیش از حواله است"
        #                     })
        #     if len(bugs) > 0:
        #         return Response(bugs)
        #

        return Response({})

    def getPositionDocByPosID(self, positionID):
        ps = PositionsDocument.objects.filter(positionID=positionID).order_by('-postDate')
        ps = ps[0]
        s = {"positionName": ps["profileName"], "positionchartName": ps["chartName"], "positionavatar": ps["avatar"]}
        return s

    def getAllJs(self, html):
        soup = bs4.BeautifulSoup(html, features='html.parser')
        scripts = soup.find_all('script')
        srcs = [link['src'] for link in scripts if 'src' in link.attrs]
        return srcs

    @list_route(methods=["POST"])
    def sendAutomated_tolid(self, request, *args, **kwargs):
        letterViewCreate = LetterViewSet()
        request.POST._mutable = True
        request.GET._mutable = True

        # detecting how who to recieve letters
        sign = HavalehForooshSigns.objects.filter(id=request.data['dt']['id']).first()
        approve = HamkaranHavaleForooshOrderApprove.objects.get(id=sign.HavalehForooshApproveLink)
        # havaleh = HavalehForooshs.objects.get(id=approve.havalehForooshLink)

        iii = []
        for a in approve.item['items']:
            d = a['OrderItemProductNumber'][0:2]
            iii.append(d)
        iii = query(iii).distinct().to_list()

        nahieh_1 = False
        nahieh_2 = False

        for i in iii:
            if i in ['66', '77', '88', '65', '75', '85']:
                nahieh_1 = True
            if i in ['89', '90', '93', '92', '93', '98']:
                nahieh_2 = True

        request.data.update(newLetter)
        user = MyUser.objects.get(username="automatedprocess")
        letterViewCreate.request = request
        letterViewCreate.format_kwarg = {}
        request.user = user
        url = request._request.environ['HTTP_ORIGIN'] + "/#!/Sales/hf/" + str(
            approve.havalehForooshLink) + "/details"
        recs['subject'] = "حواله فروش - تولید"
        recs['body'] = """
        <h3>حواله تولید زیر مورد تایید است</h3>
        <p>لطفا حواله ی زیر را به دقت بررسی کنید</p>
        <iframe style='width:100%;height:1000px' allowfullscreen  src=""" + url + """ name="example-month-input-directive"></iframe>
        """

        result = letterViewCreate.create(request, args, kwargs)
        letterID = result.data['id']

        recs['id'] = letterID
        recs['recievers'] = []
        if nahieh_1:
            recs['recievers'] = recs['recievers'] + nahieh_1_tolid
        if nahieh_2:
            recs['recievers'] = recs['recievers'] + nahieh_2_tolid
        request.data.update(recs)
        result = letterViewCreate.create(request, args, kwargs)

        return result

    @list_route(methods=["POST"])
    def sendAutomated_foroosh(self, request, *args, **kwargs):
        letterViewCreate = LetterViewSet()
        request.POST._mutable = True
        request.GET._mutable = True

        # detecting how who to recieve letters
        sign = HavalehForooshSigns.objects.filter(id=request.data['dt']['id']).first()
        approve = HavalehForooshApprove.objects.get(id=sign.HavalehForooshApproveLink)
        # havaleh = HavalehForooshs.objects.get(id=approve.havalehForooshLink)

        iii = []
        for a in approve.item['items']:
            d = a['PartCode'][0:2]
            iii.append(d)
        iii = query(iii).distinct().to_list()

        nahieh_1 = False
        nahieh_2 = False

        for i in iii:
            if i in ['66', '77', '88', '65', '75', '85']:
                nahieh_1 = True
            if i in ['89', '90', '93', '92', '93', '98']:
                nahieh_2 = True

        request.data.update(newLetter)
        user = MyUser.objects.get(username="automatedprocess")
        letterViewCreate.request = request
        letterViewCreate.format_kwarg = {}
        request.user = user
        url = request._request.environ['HTTP_ORIGIN'] + "/#!/Sales/hf/" + str(
            approve.havalehForooshLink) + "/details"
        recs['subject'] = "حواله فروش - خروج"
        recs['body'] = """
        <h3>حواله فروش زیر مورد تایید است</h3>
        <p>لطفا حواله ی زیر را به دقت بررسی کنید</p>
        <iframe style='width:100%;height:1000px' allowfullscreen  src=""" + url + """ name="example-month-input-directive"></iframe>
        """

        result = letterViewCreate.create(request, args, kwargs)
        letterID = result.data['id']

        recs['id'] = letterID
        recs['recievers'] = []
        if nahieh_1:
            recs['recievers'] = recs['recievers'] + nahieh_1_foroosh
        if nahieh_2:
            recs['recievers'] = recs['recievers'] + nahieh_2_foroosh
        request.data.update(recs)
        result = letterViewCreate.create(request, args, kwargs)
        return Response({})

    @detail_route(methods=["GET"])
    def getDetailBarnamehSigns(self, request, *args, **kwargs):
        # getting signs
        signs = list(HavalehForooshSigns.objects.filter(HavalehForooshApproveLink=kwargs['id']))
        # qrexit_ + exit_id + _ + positionID + _ +stepID
        if len(signs) > 0:
            signs = HavalehForooshSignSerializer(instance=signs, many=True).data
            for s in signs:
                ps = PositionsDocument.objects.filter(positionID=s["positionID"]).order_by('-postDate')
                ps = ps[0]
                s["positionName"] = ps["profileName"]
                s["positionchartName"] = ps["chartName"]
                s["positionavatar"] = ps["avatar"]
                s["signCount"] = len(signs)
                s["hash"] = s['id']
        return Response(signs)

    @list_route(methods=["post"])
    def signHavalehFromMobile(self, request, *args, **kwargs):
        forooshInstance = 1
        """
        VchHdrId: "6194dd4063ef16aa7274cbe4"
        httppost: "/api/v1/havakehForoosh/signHavaleh/"
        signType: 1
        signpass: "****"
        stepID: 5
        withSMS: false
        """
        forooshInstances = HamkaranHavaleForoosh.objects.get(id=request.data['selid'])
        forooshApprovesInstances = HamkaranHavaleForooshOrderApprove.objects.filter(
            havalehForooshLink=forooshInstances.id).first()
        signs = HavalehForooshSigns.objects.filter(HavalehForooshApproveLink=forooshApprovesInstances.id)
        signs = HavalehForooshSignSerializer(instance=signs, many=True).data

        whichStep = 1

        ss1 = query(signs).where(lambda x: x['whichStep'] == 1).to_list()
        if len(ss1) > 0:
            whichStep = 2

        ss2 = query(signs).where(lambda x: x['whichStep'] == 2).to_list()
        if len(ss2) > 0:
            whichStep = 3

        """
        حالا اینجا هم مدیرعامل میتواند امضا کند و هم مالی
        """
        ss3 = query(signs).where(lambda x: x['whichStep'] == 3).to_list()
        if len(ss3) > 0:
            current_group = request.user.groups.filter(name='group_havalehforoosh_permited_to_view_4').count()
            if current_group > 0:
                whichStep = 4

            current_group = request.user.groups.filter(name='group_havalehforoosh_permited_to_view_5').count()
            if current_group > 0:
                whichStep = 5

        """
        حالا اینجا هم مدیرعامل میتواند امضا کند و هم مالی
        """
        ss4 = query(signs).where(lambda x: x['whichStep'] == 4).to_list()
        if len(ss4) > 0:
            current_group = request.user.groups.filter(name='group_havalehforoosh_permited_to_view_6').count()
            if current_group > 0:
                whichStep = 6

            current_group = request.user.groups.filter(name='group_havalehforoosh_permited_to_view_7').count()
            if current_group > 0:
                whichStep = 7

        dt = {
            'VchHdrId': forooshApprovesInstances.id,
            'signType': 1,
            'signpass': request.data['entetedPass'],
            'stepID': whichStep,
            'withSMS': False

        }

        _mutable = request.data._mutable
        request.data._mutable = True
        request.data.update(dt)
        request.data._mutable = False
        result = self.signHavaleh(request, *args, **kwargs)
        return result

    @list_route(methods=["post"])
    def signHavaleh(self, request, *args, **kwargs):
        if int(request.data.get("signType")) != 1:  # means exit sign
            return Response({'errorcode': 1, 'msg': 'این امضا برای این تابع مجاز نیست'})

        signPass = request.data.get('signpass')
        uvs = UserViewSet()
        signPassIsOK = uvs.checkUserSignPass(request.user, signPass)

        if not signPassIsOK:
            return Response({'errcode': 2, 'msg': 'رمز دوم اشتباه است'})

        havalehID = request.data.get("VchHdrId")
        approveInstance = HamkaranHavaleForooshOrderApprove.objects.get(id=havalehID)
        stepNum = str(request.data.get("stepID"))
        if stepNum == "-1":  # means than finding latest step
            havalehSignsInstance = HavalehForooshSigns.objects.filter(
                havalehForooshLink=request.data.get("VchHdrId")).order_by("-whichStep").first()
            stepNum = str(havalehSignsInstance.whichStep + 1)

        positionInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        groupName = "group_havalehforoosh_permited_to_view_" + stepNum
        if stepNum == '6':
            groupName = "group_havalehforoosh_permited_to_view_4"
        if stepNum == '7':
            groupName = "group_havalehforoosh_permited_to_view_5"
        group = Group.objects.filter(name=groupName)
        if group.count() == 0:
            return Response({
                "errcode": 1,
                "msg": "گروه های عملیاتی توسط بهمنی ساخته نشده اند"
            })
            # raise Exception("1_" + groupName + " does not created Mohammad Please create it !")
        # user = MyUser.objects.get(id = positionInstance.userID)
        group = group[0]
        isAllowed = group.user_set.all().filter(id=positionInstance.userID).count()
        if isAllowed == 0:
            return Response({
                "errcode": 2,
                "msg": "شما مجور امضا زدن ندارید"
            })
            # raise Exception("2_" + str(positionInstance.userID) + " does not have permission !")
        dt = {
            "positionID": positionInstance.positionID,
            "HavalehForooshApproveLink": havalehID,
            "whichStep": int(stepNum),
            "comment": request.data.get("comment"),
            "dateOfPost": datetime.now()
        }

        # ------------------------------------------------------------
        # ------------------------------------------------------------
        # ------------------------------------------------------------
        # checking if previous sign signed
        # checking hierarchy of signs
        currentStep = int(stepNum)
        for c in range(1, currentStep):
            countOfPrevStep = HavalehForooshSigns.objects.filter(
                HavalehForooshApproveLink=havalehID,
                whichStep=c
            ).count()
            if (countOfPrevStep == 0) and (stepNum not in ['5', '6', '7']):
                return Response({
                    "errcode": 3,
                    "msg": "ترتیب امضا رعایت نشده است لطفا از امضای امضا کننده های قبلی اطمینان پیدا کنید"
                })
                # raise Exception("3_" +
                # str(positionInstance.userID) + " signed before previous signs > person before you must sgn first !")
        # --------------------------------------------------------------
        # --------------------------------------------------------------
        # --------------------------------------------------------------
        filter = {}
        filter['HavalehForooshApproveLink'] = dt['HavalehForooshApproveLink']
        filter['whichStep'] = dt['whichStep']
        countOfSigns = HavalehForooshSigns.objects.filter(**filter).count()
        if countOfSigns > 0:
            return Response({
                "errcode": 4,
                "msg": "شما قبلا امضا زده اید - لطفا صبر کنید و صفحه را رفرش کنید"
            })
            # raise Exception("4_" + str(positionInstance.userID) + " you have signed it before why ??")

        # -----------------------------------------------
        # now removing current notifications of user
        Notifications.objects.filter(
            extra__havalehForooshID=havalehID
        ).delete()

        # -----------------------------------------------
        # -----------------------------------------------
        # -----------------------------------------------

        ser = HavalehForooshSignSerializer(data=dt)
        ser.is_valid(raise_exception=True)
        ser.save()

        if request.data.get('withSMS') == True:
            cellno = request.data.get('cellno')
            smms = """با سلام
امضای شما در حواله ی %s با کد %s ثبت شده است
تاریخ امضا %s
میزان خروجی %s
نام مشتری %s
**** ****""" % (
                "فروش",
                request.data.get('exitID'),
                mil_to_sh_with_time(datetime.now()),
                "??",
                "??",
            )
            sendSMS.delay(cellno, smms)
        return Response(ser.data)


class HavalehForooshConvViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = HavalehForooshConv.objects.all()
    serializer_class = HavalehForooshConvSerializer
    pagination_class = DetailsPagination

    def get_queryset(self):
        if self.request.method == "GET":
            self.queryset = self.queryset.filter(havalehForooshLink=int(self.request.query_params['convID']))
        return super(HavalehForooshConvViewSet, self).get_queryset()

    def initial(self, request, *args, **kwargs):
        if request.method != "GET" and request.method != "DELETE":
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            request.data["positionID"] = posiIns.positionID
            request.data["companyID"] = posiIns.companyID

        return super(HavalehForooshConvViewSet, self).initial(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request.data['dateOfPost'] = datetime.now()
        return super(HavalehForooshConvViewSet, self).create(request, *args, **kwargs)

    @detail_route(methods=["POST"])
    def AddToReplay(self, request, *args, **kwargs):
        dt = request.data
        dt["havalehForooshLink"] = kwargs["id"]
        sc = HavalehForooshConv(**dt)
        sc.save()
        return Response({})

    @list_route(methods=["GET"])
    def removeReplay(self, request, *args, **kwargs):
        ins = HavalehForooshConv.objects.get(id=request.query_params["replayID"])
        if ins.positionID == GetPositionViewset().GetCurrentPositionDocumentInstance(request).positionID:
            ins.delete()
        return Response({})

    @list_route(methods=["POST"])
    def weProduceIt(self, request, *args, **kwargs):
        if request.user.groups.all().filter(name="group_havalehforoosh_permited_to_tolid").count() == 0:
            return Response({"msg": "شما مجاز نیستید به تولید"})
        ins = HamkaranHavaleForooshOrderApprove.objects.get(id=request.data['approve']['id'])
        posi = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        dt = {
            'HavalehForooshApproveLink': str(ins.id),
            'positionID': posi.positionID,
            'comment': 'در برنامه تولید قرار گرفت',
            'dateOfPost': datetime.now(),
            'companyID': posi.companyID,
            'exp': {
                "approve": {
                    "positionID": posi.positionID,
                    "dateOfApprove": datetime.now(),
                    "type": 3,  # means accept
                    "avatar": posi.avatar,
                    "name": posi.profileName + "-" + posi.chartName
                }
            }
        }

        ans = HavalehForooshConvSerializer(data=dt)
        ans.is_valid(raise_exception=True)
        ans.save()

        return Response(ans.data)

    @list_route(methods=["POST"])
    def readyToSend(self, request, *args, **kwargs):
        if request.user.groups.all().filter(name="group_havalehforoosh_permited_to_tolid").count() == 0:
            return Response({"msg": "شما مجاز نیستید به تولید"})
        ins = HamkaranHavaleForooshOrderApprove.objects.get(id=request.data['approve']['id'])
        posi = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        dt = {
            'HavalehForooshApproveLink': str(ins.id),
            'positionID': posi.positionID,
            'comment': 'آماده ارسال',
            'dateOfPost': datetime.now(),
            'companyID': posi.companyID,
            'exp': {
                "approve": {
                    "positionID": posi.positionID,
                    "dateOfApprove": datetime.now(),
                    "type": 4,  # means accept
                    "avatar": posi.avatar,
                    "name": posi.profileName + "-" + posi.chartName
                }
            }
        }

        ans = HavalehForooshConvSerializer(data=dt)
        ans.is_valid(raise_exception=True)
        ans.save()
        return Response(ans.data)

    @detail_route(methods=["GET"])
    def getReplays(self, request, *args, **kwargs):

        all = HavalehForooshConv.objects.filter(havalehForooshLink=int(kwargs["id"])).order_by('-id')
        replays = []
        for pp in all:
            ps = PositionsDocument.objects.get(positionID=pp.positionID)
            replays.append({
                "isEditable": (pp["positionID"] == ps.positionID),
                "positionName": ps.profileName,
                "dateOfPost": pp.dateOfPost,
                "comment": pp.comment,
                "id": pp.id,
            })
        return Response(replays)

    def list(self, request, *args, **kwargs):
        result = super(HavalehForooshConvViewSet, self).list(request, *args, **kwargs)
        for d in result.data["results"]:
            positionDoc = PositionsDocument.objects.filter(
                positionID=d["positionID"],
                companyID=request.user.current_company_id,
            )

            sls = HavalehForooshConv.objects.filter(havalehForooshLink=d["havalehForooshLink"]).order_by("-id")
            replays = []
            for pp in sls:
                replays.append({
                    "positionName": PositionsDocument.objects.get(positionID=pp.positionID).profileName,
                    "dateOfPost": pp.dateOfPost,
                    "comment": pp.comment,
                    "id": pp.id,
                })
            d["replays"] = replays
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
            d["isEditable"] = (d["positionID"] == positionDoc.positionID)

        return result


class OLD_HavalehForooshViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = HavalehForooshs.objects.all()
    serializer_class = HavalehForooshSerializer
    pagination_class = DetailsPagination

    """
    permitted group for coming to exitis :
    group_havalehforoosh_permited_to_view

    qrcode signature format :
    type = qrexit_
    qrexit_ + exit_id + _ + positionID

    steps:
     group_havalehforoosh_start
     group_havalehforoosh_permited_to_view_1
     group_havalehforoosh_permited_to_view_2
     group_havalehforoosh_permited_to_view_3
     group_havalehforoosh_permited_to_view_4
     group_havalehforoosh_permited_to_view_5
     group_havalehforoosh_end


    """

    def fixChar(self, currentChar):
        if currentChar == None:
            return 'کارکتر نا معتبر'
        cc = currentChar
        cc = cc.replace("ش", "ش")
        cc = cc.replace("ر", "ر")
        cc = cc.replace("ک", "ک")
        cc = cc.replace("ت", "ت")
        cc = cc.replace("ي", "ی")
        cc = cc.replace("ي", "ی")
        cc = cc.replace("گ", "گ")
        cc = cc.replace("س", "س")
        cc = cc.replace("م", "م")
        cc = cc.replace("غ", "غ")
        cc = cc.replace("ا", "ا")
        cc = cc.replace("آ", "آ")
        cc = cc.replace("ذ", "ذ")
        cc = cc.replace("ن", "ن")
        cc = cc.replace("خ", "خ")
        cc = cc.replace("ل", "ل")
        cc = cc.replace("پ", "پ")
        cc = cc.replace("ه", "ه")
        cc = cc.replace("ص", "ص")
        cc = cc.replace("ع", "ع")
        cc = cc.replace("د", "د")
        cc = cc.replace("و", "و")
        return cc

    # AccvwSLERepOrder
    def mapHamkaran(self):
        lastVchHdrRefInstance = lastHavalehForooshID.objects.first()

        if lastVchHdrRefInstance == None:
            ll = lastHavalehForooshID(lastVchHdrRef=0)
            ll.save()
            lastVchItmId = ll

        pool = ConnectionPools.objects.get(name="AccvwSLERepOrder")
        sql = pool.sqls[0]["code"]
        sql = sql.replace("str__lessthan", " > " + str(lastVchHdrRefInstance.lastVchHdrRef))
        sql = sql.replace("<:", "")
        sql = sql.replace(":>", "")
        connection = Connections.objects.get(databaseName="sgdb")
        connection = ConnectionsViewSet().getConnection(connection)
        connection.execute(sql)
        sql_res = connection.fetchall()
        grouped_result = query(sql_res).group_by(lambda x: x['VchHdrRef'],
                                                 result_selector=lambda key, group: {'key': key,
                                                                                     "group": group.to_list()}).order_by(
            lambda x: x['key']).to_list()
        for g in grouped_result:
            if HavalehForooshs.objects.filter(VchHdrRef=g['key']).count() == 0:
                if len(g["group"]) == 0:
                    raise Exception("حواله خروجی پیدا شده است که هیچ آیتمی ندارد - لطفا دوستان فروش اطلاع بدهید")
                dt = {
                    "VchHdrRef": g['key'],
                    "customerName": self.fixChar(g["group"][0]['CstmrName']),
                    "havalehNo": g["group"][0]['VchNo'],
                    "tarikheSodoor": mil_to_sh(g["group"][0]["VchDate"]),
                    "mizanAvaliehSefaresh": int(query(g['group']).sum(lambda x: x['Qty']))
                }
                ss = self.serializer_class(data=dt)
                ss.is_valid(raise_exception=True)
                ss = ss.save()

                dt = {
                    'havalehForooshLink': ss.id,
                    'reason': 'ثبت اولیه از همکاران',
                    'item': {
                        'items': g['group'],
                    },
                    'parent': None,
                    'positionID': None,
                }

                for d in dt['item']['items']:
                    d['AQty'] = d['Qty']
                    d['CstmrName'] = self.fixChar(d['CstmrName'])
                    d['PartName'] = self.fixChar(d['PartName'])
                    d['StockName'] = self.fixChar(d['StockName'])
                    d['BaseVchTypeDesc'] = self.fixChar(d['BaseVchTypeDesc'])

                hser = HavalehForooshApproveSerializer(data=dt)
                hser.is_valid(raise_exception=True)
                hser.save()

                lastHavalehForooshID.objects.all().delete()
                lastHavalehForooshID(lastVchHdrRef=g.get("key")).save()

    def list(self, request, *args, **kwargs):

        self.mapHamkaran()
        result = super(OLD_HavalehForooshViewSet, self).list(request, args, kwargs)
        return result

    @detail_route(methods=["GET"])
    def nextRecord(self, request, *args, **kwargs):
        id = kwargs.get("id")
        fff = HavalehForooshs.objects.filter(id__gt=id).order_by("id").first()
        if not fff:
            return Response({"id": ""})
        return Response({'id': str(fff.id)})

    @detail_route(methods=["GET"])
    def prevRecord(self, request, *args, **kwargs):
        id = kwargs.get("id")
        fff = HavalehForooshs.objects.filter(id__lt=id).order_by("-id").first()
        if not fff:
            return Response({"id": ""})
        return Response({'id': str(fff.id)})

    def getVaziat(self, step):

        if step == 1:
            return "منتظر امضای حسابداری فروش"
        if step == 2:
            return "منتظر امضای مدیر بازرگانی"
        if step == 3:
            return "منتظر تایید تولید مدیر مالی"
        if step == 4:
            return "منتظر تایید تولید مدیر عامل"
        if step == 5:
            return "منتظر تایید خروج مدیر عامل و مالی"
        if step == 6:
            return "منتظر تایید خروج مدیر عامل"
        if step == 7:
            return "دارای تاییده خروج"

    @list_route(methods=["GET"])
    def getAggr(self, request, *args, **kwargs):

        if request.user.groups.filter(name="group_havalehforoosh_permited_to_view").count() == 0:
            return Response({})
        havals = []
        if request.query_params.get('archive'):
            if request.query_params.get('archive') == "true":
                havals = []
                pass
            else:
                havals = [x.havalehForooshLink for x in HavalehForooshApprove.objects.filter(item__closed=None,
                                                                                             dateOfPost__gte=datetime.strptime(
                                                                                                 sh_to_mil(
                                                                                                     "1398/07/21"),
                                                                                                 "%Y/%m/%d"))]
        else:
            havals = [x.havalehForooshLink for x in HavalehForooshApprove.objects.filter(item__closed=None,
                                                                                         dateOfPost__gte=datetime.strptime(
                                                                                             sh_to_mil(
                                                                                                 "1398/07/21"),
                                                                                             "%Y/%m/%d"))]

        # try:
        if request.query_params.get("search") == None:
            self.mapHamkaran()
        else:
            if request.query_params.get("search") == "":
                self.mapHamkaran()

        # except:
        #     pass
        page_size = int(request.query_params.get("page_size", "20"))
        page = int(request.query_params.get("page", "1"))
        search = ""
        search = request.query_params.get("search", "")
        searchDict = {}
        if search != "":
            searchDict["$or"] = [
                {"customerName": {"$regex": search}},
                {"tarikheSodoor": {"$regex": search}},
                {"havalehNo": {"$regex": search}},
            ]
            if search.isdigit():
                searchDict["$or"].append(
                    {"mizanAvaliehSefaresh": int(search)})
        if len(havals) > 0:
            searchDict["$and"] = [{"_id": {"$in": query(havals).select(lambda x: x).distinct().to_list()}}]
            pass

        counter = list(HavalehForooshs.objects.aggregate(
            {"$match": searchDict}, {"$count": "countOf"}))
        if len(counter) == 0:
            return Response({})
        totalCount = counter[0]["countOf"]
        data = HavalehForooshs.objects.aggregate(
            {"$match": searchDict},
            {"$sort": {"_id": -1}},
            {"$limit": ((page - 1) * page_size) + page_size},
            {"$skip": (page - 1) * page_size})

        data = list(data)
        for d in data:
            allApprove = [x['id'] for x in HavalehForooshApprove.objects.filter(havalehForooshLink=d['_id'])]
            lastSigns = list(
                HavalehForooshSigns.objects.filter(HavalehForooshApproveLink__in=allApprove).order_by("-whichStep"))
            if len(lastSigns) == 0:
                d['vaziatInt'] = 1
                d['vaziat'] = "منتظر امضای صادر کننده"
            else:

                # if lastSigns[0].whichStep == 5:
                #     d['vaziatInt'] = 5
                #     d['vaziat'] = "تایید شده"
                # else:
                d['vaziat'] = self.getVaziat(lastSigns[0].whichStep)

        # for d in data :
        #     signCount = HavalehForooshSigns.objects.filter(HavalehForooshApproveLink = d['_id']).count()
        #     d['signCount'] = signCount
        #     commentCount = HavalehForooshConv.objects.filter(HavalehForooshApproveLink = d['_id']).count()
        #     d['commentCount'] = commentCount
        #
        #     d['vaziat'] = self.getVaziat(d)

        result = {
            "next": "/api/v1/havakehForoosh/getAggr/?page_size=%d&page=%d&search=%s" % (page_size, page + 1, search),
            "prev": "/api/v1/havakehForoosh/getAggr/?page_size=%d&page=%d&search=%s" % (
                page_size, page - 1, search) if page - 1 > 0 else None,
            "first": "/api/v1/havakehForoosh/getAggr/?page_size=%d&page=%d&search=%s" % (page_size, 1, search),
            "last": "/api/v1/havakehForoosh/getAggr/?page_size=%d&page=%d&search=%s" % (
                page_size, int(totalCount / page_size) if totalCount > page_size else 1, search),
            "count": totalCount,
            "results": list(data)
        }

        return Response(result)

    @detail_route(methods=["GET"])
    def getDetails(self, request, *args, **kwargs):
        id = kwargs["id"]
        instance = self.queryset.get(id=id)
        # check if user is from tolid department

        ApprovesIns = HavalehForooshApprove.objects.filter(havalehForooshLink=id).order_by("id")
        ApprovesIns = HavalehForooshApproveSerializer(instance=ApprovesIns, many=True).data

        for a in ApprovesIns:
            signsIns = HavalehForooshSigns.objects.filter(HavalehForooshApproveLink=a['id'])
            signsIns = HavalehForooshSignSerializer(instance=signsIns, many=True).data
            a['signs'] = signsIns
            for aa in a['signs']:
                ins = PositionsDocument.objects.filter(positionID=aa['positionID']).first()
                if ins:
                    aa['positionName'] = ins['profileName']
                    aa['positionchartName'] = ins['chartName']
            # detecting duplicated signs
            if len(a['signs']) > 0:
                dup_signs = query(a['signs']).group_by(lambda x: x['HavalehForooshApproveLink'],
                                                       result_selector=lambda key, group: {
                                                           'key': key,
                                                           'group': query(group).group_by(lambda x: x['whichStep'],
                                                                                          result_selector=lambda key,
                                                                                                                 xgroup: {
                                                                                              'whiscStep': key,
                                                                                              'firstOf': xgroup.first()}
                                                                                          ).to_list()
                                                       }
                                                       ).to_list()
                a['signs'] = [x['firstOf'] for x in dup_signs[0]['group']]

            inss = HavalehForooshConv.objects.filter(HavalehForooshApproveLink=a['id']).order_by("id")
            inss = HavalehForooshConvSerializer(instance=inss, many=True).data
            for c in inss:
                ps = PositionsDocument.objects.filter(positionID=c['positionID'])
                if len(ps) > 0:
                    ps = ps[0]
                    c["positionName"] = ps.profileName
                    c["positionSemat"] = ps.chartName
                    c["avatar"] = ps.avatar.replace("thmum50CC", "thmum100")
                else:
                    c["positionName"] = "حذف شده"
                    c["positionSemat"] = "حذف شده"
                    c["avatar"] = "/static/images/avatar_empty.jpg"
            a['convs'] = inss

        c = 1
        for a in ApprovesIns:
            if c != 1:
                posiData = self.getPositionDocByPosID(a['positionID'])
                a['positionName'] = posiData['positionName']
                a['positionchartName'] = posiData['positionchartName']
                a['positionAvatar'] = posiData['positionavatar'].replace("thmum50CC", "thmum100")
            c = c + 1

        return Response(ApprovesIns)

    @list_route(methods=["GET"])
    def getDetailsApprove(self, request, *args, **kwargs):
        appriveID = request.query_params.get("ai")
        stepID = request.query_params.get("s")
        ApprovesIns = HavalehForooshApprove.objects.get(id=appriveID)
        ApprovesIns = HavalehForooshApproveSerializer(instance=ApprovesIns).data

        signsIns = HavalehForooshSigns.objects.filter(HavalehForooshApproveLink=ApprovesIns['id'])
        signsIns = HavalehForooshSignSerializer(instance=signsIns, many=True).data
        ApprovesIns['signs'] = signsIns
        for aa in ApprovesIns['signs']:
            ins = PositionsDocument.objects.filter(positionID=aa['positionID']).first()
            if ins:
                aa['positionName'] = ins['profileName']
                aa['positionchartName'] = ins['chartName']

        return Response(ApprovesIns)

    def isHavalehFinished(self, approve):
        havalehForooshes = HavalehForooshApprove.objects.filter(
            havalehForooshLink=approve['havalehForooshLink']).order_by("id")
        havalehForooshes = HavalehForooshApproveSerializer(instance=havalehForooshes, many=True).data
        otherDts = []
        for a in havalehForooshes[0]['item']['items']:
            a['AQty'] = 0
        for a in havalehForooshes:
            otherDts += a['item']['items']

        firstDts = query(havalehForooshes[0]['item']['items']).group_by(
            lambda x: x['PartCode'], result_selector=lambda key, group: {'PartCode': key, 'sumOfQty': query(group).sum(
                lambda x: x['Qty'])}).to_list()

        otherDts = query(otherDts).group_by(
            lambda x: x['PartCode'], result_selector=lambda key, group: {'PartCode': key, 'sumOfAQty': query(group).sum(
                lambda x: x['AQty'])}).to_list()
        aa = approve['item']['items']
        thisDts = query(aa).group_by(
            lambda x: x['PartCode'], result_selector=lambda key, group: {'PartCode': key, 'sumOfAQty': query(group).sum(
                lambda x: x['AQty'])}).to_list()
        remains = []
        for f in firstDts:
            sumOf = query(otherDts).where(lambda x: x['PartCode'] == f['PartCode']).sum(lambda x: x['sumOfAQty'])
            if (f['sumOfQty'] - sumOf) > 0:
                sumOfNew = query(thisDts).where(lambda x: x['PartCode'] == f['PartCode']).sum(lambda x: x['sumOfAQty'])
                if ((f['sumOfQty'] - sumOf) - sumOfNew) > 0:
                    remains.append({
                        'PartCode': f['PartCode'],
                        'remain_amount': (f['sumOfQty'] - sumOf) - sumOfNew
                    })

        return dict(
            result=len(remains) == 0,
            details=remains
        )

    def getFirstInstance(self, approveID):
        ApprovesIns = HavalehForooshApprove.objects.get(id=approveID)
        ApprovesInses = HavalehForooshApprove.objects.filter(
            havalehForooshLink=ApprovesIns.havalehForooshLink).order_by("id").first()
        return ApprovesInses

    def getFirstItemByApproveID(self, approveID):
        ApprovesInses = self.getFirstInstance(approveID)
        firstData = HavalehForooshApproveSerializer(instance=ApprovesInses).data
        idOfFirstData = firstData['id']
        # we should get AQty of first data to zero when user select to modify Qty
        firstData = query(firstData['item']['items']).group_by(
            lambda x: x['PartCode'], result_selector=lambda key, group: {'PartCode': key, 'sumOfQty': query(group).sum(
                lambda x: x['Qty'])}).to_list()
        return firstData

    def calcRemainQty(self, approve, itemOfQty):
        firstIns = HavalehForooshApprove.objects.filter(havalehForooshLink=approve['havalehForooshLink']).order_by(
            "id").first()
        firstInsItems = firstIns.item['items']
        inss = HavalehForooshApprove.objects.filter(
            havalehForooshLink=approve['havalehForooshLink'], item__thisApproveFinished=True)
        aqty = 0
        qty = 0
        for ins in inss:
            for item in ins['item']['items']:
                if item['PartCode'] == itemOfQty['PartCode']:
                    aqty = aqty + item['AQty']
        sumQty = query(firstInsItems).where(lambda x: x['PartCode'] == itemOfQty['PartCode']).sum(lambda x: x['Qty'])
        return sumQty - aqty

    @detail_route(methods=["GET"])
    def startFromRemaining(self, request, *args, **kwargs):
        approveID = kwargs['id']

        hfs = HavalehForooshApprove.objects.filter(havalehForooshLink=kwargs['id'],
                                                   item__thisApproveFinished=True).order_by("id")
        hfs = HavalehForooshApproveSerializer(instance=hfs, many=True).data
        if len(hfs) == 0:
            firstIns = HavalehForooshApprove.objects.filter(havalehForooshLink=kwargs['id']).order_by("id").first()
            firstIns = HavalehForooshApproveSerializer(instance=firstIns).data
            firstQty = query(firstIns['item']['items']).sum(lambda x: x['Qty'])
        if len(hfs) == 1:
            firstIns = hfs[0]
            firstQty = query(firstIns['item']['items']).sum(lambda x: x['Qty'])
        if len(hfs) > 1:
            firstIns = HavalehForooshApprove.objects.filter(havalehForooshLink=kwargs['id']).order_by("-id").first()
            firstIns = HavalehForooshApproveSerializer(instance=firstIns).data
            firstQty = query(firstIns['item']['items']).sum(lambda x: x['Qty'])

        hfs = [x['item']['items'] for x in hfs]
        hfs = list(chain(*hfs))
        #
        # firstIns = HavalehForooshApprove.objects.filter(havalehForooshLink=kwargs['id']).order_by("id").first()
        # firstIns = HavalehForooshApproveSerializer(instance=firstIns).data
        # firstQty = query(firstIns['item']['items']).sum(lambda x: x['Qty'])
        #

        otherAQty = query(hfs).sum(lambda x: x['AQty'])
        for f in firstIns['item']['items']:
            cc = query(firstIns['item']['items']).where(lambda x: x['PartCode'] == f['PartCode']).sum(
                lambda x: x['Qty'])
            aa = query(hfs).where(lambda x: x['PartCode'] == f['PartCode']).sum(lambda x: x['AQty'])
            f['Qty'] = cc - aa
            f['AQty'] = f['Qty']
            f['MQty'] = f['Qty']
        firstIns['item']['thisApproveFinished'] = False
        firstIns['item']['closed'] = False
        firstIns['item']['isAllFinished'] = False
        firstIns['item']['items'] = query(firstIns['item']['items']).where(lambda x: x['Qty'] > 0).to_list()
        del firstIns['id']
        ss = HavalehForooshApproveSerializer(data=firstIns)
        ss.is_valid(raise_exception=True)
        ss.save()
        return Response(ss.data)

    @detail_route(methods=["GET"])
    def isThisApproveFinishedTotaly(self, request, *args, **kwargs):

        hfs = HavalehForooshApprove.objects.filter(havalehForooshLink=kwargs['id'],
                                                   item__closed=False).count()
        if hfs != 0:
            return Response({'result': True})

        approveID = kwargs['id']
        hfs = HavalehForooshApprove.objects.filter(havalehForooshLink=kwargs['id'],
                                                   item__thisApproveFinished=True).order_by("id")
        hfs = HavalehForooshApproveSerializer(instance=hfs, many=True).data
        hfs = [x['item']['items'] for x in hfs]
        hfs = list(chain(*hfs))

        firstIns = HavalehForooshApprove.objects.filter(havalehForooshLink=kwargs['id']).order_by("id").first()
        firstIns = HavalehForooshApproveSerializer(instance=firstIns).data
        firstQty = query(firstIns['item']['items']).sum(lambda x: x['Qty'])

        if firstIns['item'].get('closed') == None:
            return Response({'result': True})

        otherAQty = query(hfs).sum(lambda x: x['AQty'])
        return Response({"result": ((firstQty - otherAQty) == 0)})

    @list_route(methods=["POST"])
    def changesayer(self, request, *args, **kwargs):
        data = request.data
        approveIns = HavalehForooshApprove.objects.get(id=data['approve']['id'])
        # dt = query(approveIns.item['items']).where(lambda x:x['PoartCode'] == data['item']['PartCode']).first()
        item = approveIns.item
        for d in item['items']:
            if d['PartCode'] == data['item']['PartCode']:
                d['tarikheTahvil'] = data['item']['tarikheTahvil']
        sr = HavalehForooshApproveSerializer(instance=approveIns, data={"item": item}, partial=True)
        sr.is_valid(raise_exception=True)
        sr.save()
        return Response(sr.data)

    @list_route(methods=["POST"])
    def proveTolid(self, request, *args, **kwargs):
        if request.user.groups.all().filter(name="group_havalehforoosh_permited_to_tolid").count() == 0:
            return Response({"msg": "شما مجاز نیستید به تولید"})

        currentPos = GetPositionViewset().GetCurrentPositionDocumentInstance(self.request)
        convIns = HavalehForooshConv.objects.get(id=request.data.get("id"))
        exp = convIns.exp
        if convIns.exp.get("approve") == None:
            exp['approve'] = {
                "positionID": currentPos.positionID,
                "dateOfApprove": datetime.now(),
                "type": 1,  # means accept
                "avatar": currentPos.avatar,
                "name": currentPos.profileName + "-" + currentPos.chartName
            }
            ins = HavalehForooshConvSerializer(instance=convIns, data={"exp": dict(exp)}, partial=True)
            ins.is_valid(raise_exception=True)
            ins.save()
            return Response(ins.data)
        return None

    @list_route(methods=["POST"])
    def tolidBelaApply(self, request, *args, **kwargs):
        data = request.data
        approveIns = HavalehForooshApprove.objects.get(id=data['approve']['id'])
        # dt = query(approveIns.item['items']).where(lambda x:x['PoartCode'] == data['item']['PartCode']).first()
        # checking permission
        # permission to change this step is 5
        if request.user.groups.filter(name="group_havalehforoosh_permited_to_view_5").count() == 0:
            return Response({"type": "err", "msg": "شما مجوز تغییر این مورد را ندارید"})
        dt = approveIns.item
        dt['tolidBela'] = request.data.get('item', False)
        ser = HavalehForooshApproveSerializer(instance=approveIns, data={'item': dt}, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()

        return Response({"type": "ok", "msg": dt['tolidBela']})

    @list_route(methods=["POST"])
    def ersaleFactorApply(self, request, *args, **kwargs):
        data = request.data
        approveIns = HavalehForooshApprove.objects.get(id=data['approve']['id'])
        # dt = query(approveIns.item['items']).where(lambda x:x['PoartCode'] == data['item']['PartCode']).first()
        # checking permission
        # permission to change this step is 5
        if request.user.groups.filter(name="group_havalehforoosh_permited_to_view_1").count() == 0:
            return Response({"type": "err", "msg": "شما مجوز تغییر این مورد را ندارید"})
        dt = approveIns.item
        dt['ersaleFactor'] = request.data.get('item', False)
        ser = HavalehForooshApproveSerializer(instance=approveIns, data={'item': dt}, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response({"type": "ok", "msg": dt['tolidBela']})

    @list_route(methods=["POST"])
    def khroojBelaApply(self, request, *args, **kwargs):
        data = request.data
        approveIns = HavalehForooshApprove.objects.get(id=data['approve']['id'])
        # dt = query(approveIns.item['items']).where(lambda x:x['PoartCode'] == data['item']['PartCode']).first()
        # checking permission
        # permission to change this step is 5
        if request.user.groups.filter(name="group_havalehforoosh_permited_to_view_5").count() == 0:
            return Response({"type": "err", "msg": "شما مجوز تغییر این مورد را ندارید"})
        dt = approveIns.item
        dt['khroojBela'] = request.data.get('item', False)
        ser = HavalehForooshApproveSerializer(instance=approveIns, data={'item': dt}, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()

        return Response({"type": "ok", "msg": dt['tolidBela']})

    @list_route(methods=["POST"])
    def changekarbord(self, request, *args, **kwargs):
        data = request.data
        approveIns = HavalehForooshApprove.objects.get(id=data['approve']['id'])
        # dt = query(approveIns.item['items']).where(lambda x:x['PoartCode'] == data['item']['PartCode']).first()
        item = approveIns.item
        for d in item['items']:
            if d['PartCode'] == data['item']['PartCode']:
                d['karbord'] = data['item']['karbord']
        sr = HavalehForooshApproveSerializer(instance=approveIns, data={"item": item}, partial=True)
        sr.is_valid(raise_exception=True)
        sr.save()
        return Response(sr.data)

    @list_route(methods=["POST"])
    def saveApprove(self, request, *args, **kwargs):
        approveID = request.query_params.get("ai")
        stepID = request.query_params.get("s")
        # getting first Qty
        data = request.data
        sentData = query(data['item']['items']).group_by(
            lambda x: x['PartCode'], result_selector=lambda key, group: {'PartCode': key, 'sumOfAQty': query(group).sum(
                lambda x: x['AQty'])}).to_list()

        # -----------------------------------------
        # -----------------------------------------
        # we should get AQty of first data to zero when user select to modify Qty
        firstData = self.getFirstItemByApproveID(approveID)
        # -----------------------------------------
        # -----------------------------------------
        # --- Getting Other AQty
        firstApprove = self.getFirstInstance(approveID)
        ApprovesInses = HavalehForooshApprove.objects.filter(
            havalehForooshLink=firstApprove.havalehForooshLink, id__ne=firstApprove.id).order_by("id")
        ApprovesInses = HavalehForooshApproveSerializer(instance=ApprovesInses, many=True).data

        otherDts = []
        for a in ApprovesInses:
            otherDts += a['item']['items']

        otherData = query(otherDts).group_by(
            lambda x: x['PartCode'], result_selector=lambda key, group: {'PartCode': key, 'sumOfAQty': query(group).sum(
                lambda x: x['AQty'])}).to_list()
        # -----------------------------------------
        # -----------------------------------------
        # -----------------------------------------
        bugs = []
        if len(otherDts) >= 0:  # it means this is the first suggestion
            for sd in sentData:
                for fd in firstData:
                    if sd['PartCode'] == fd['PartCode']:
                        if sd['sumOfAQty'] > fd['sumOfQty']:
                            bugs.append({
                                "PartCode": sd['PartCode'],
                                "reason": "مقدار وارد شده بیش از حواله است"
                            })
            if len(bugs) > 0:
                return Response(bugs)
            del data['id']
            havalehForooshClosed = HavalehForooshApprove.objects.filter(
                havalehForooshLink=firstApprove.havalehForooshLink)
            for h in havalehForooshClosed:
                item = h['item']
                item['closed'] = True
                item['isAllFinished'] = self.isHavalehFinished(data)['result']
                """
                here we should make first row AQty to zero to make it disable in other calcs
                """
                # for i in item['items']:
                #     i['AQty'] = 0
                hser = HavalehForooshApproveSerializer(instance=h, data={'item': item}, partial=True)
                hser.is_valid(raise_exception=True)
                hser.save()

            currentPosID = GetPositionViewset().GetCurrentPositionDocumentInstance(self.request).positionID
            data["positionID"] = currentPosID

            for d in data['item']['items']:
                d['Qty'] = self.calcRemainQty(data, d)
            data['item']['thisApproveFinished'] = False
            data['item']['closed'] = False
            data['item']['isAllFinished'] = False
            newApprove = HavalehForooshApproveSerializer(data=data)
            newApprove.is_valid(raise_exception=True)
            newApprove = newApprove.save()

            # send notification to all
            notification_reciever_group_name = "group_havalehforoosh"
            joint_users = Group.objects.filter(name__contains=notification_reciever_group_name)
            for j in joint_users:
                users = j.user_set.all()
                for u in users:
                    profileInstance = Profile.objects.filter(userID=u.id).first()
                    profileSerial = ProfileSerializer(instance=profileInstance).data
                    hfs = newApprove
                    fsi = newApprove.item['items'][0]
                    dt = {
                        'type': 7,
                        'typeOfAlarm': 3,
                        'informType': 5,
                        'userID': u.id,
                        'extra': {
                            'prevSignerName': profileSerial['extra']['Name'],
                            'prevSignerAvatar': profileSerial['extra']['profileAvatar']['url'],
                            'havalehForooshID': str(fsi['VchNo']),
                            'dbid': str(hfs.havalehForooshLink),
                            'customer': fsi['CstmrName'],
                            'qty': int(query(newApprove.item['items']).sum(lambda x: x['Qty'])),
                            'dateOf': mil_to_sh(fsi['VchDate'], splitter="/"),
                        }
                    }

                    ntSerial = NotificationsSerializer(data=dt)
                    ntSerial.is_valid(raise_exception=True)
                    ntSerial.save()

        # if len(otherDts) > 0:  # it means this is the first suggestion
        #     for sd in sentData:
        #         for fd in firstData:
        #             if sd['PartCode'] == fd['PartCode']:
        #                 if sd['sumOfAQty'] > fd['sumOfQty']:
        #                     bugs.append({
        #                         "PartCode": sd['PartCode'],
        #                         "reason": "مقدار وارد شده بیش از حواله است"
        #                     })
        #     if len(bugs) > 0:
        #         return Response(bugs)
        #

        return Response({})

    def getPositionDocByPosID(self, positionID):
        ps = PositionsDocument.objects.filter(positionID=positionID).order_by('-postDate')
        ps = ps[0]
        s = {"positionName": ps["profileName"], "positionchartName": ps["chartName"], "positionavatar": ps["avatar"]}
        return s

    def getAllJs(self, html):
        soup = bs4.BeautifulSoup(html, features='html.parser')
        scripts = soup.find_all('script')
        srcs = [link['src'] for link in scripts if 'src' in link.attrs]
        return srcs

    # Utility function
    # def convertHtmlToPdf(self, sourceHtml, outputFilename):
    #     # open output file for writing (truncated binary)
    #     resultFile = open(outputFilename, "w+b")
    #
    #     # convert HTML to PDF
    #     # pisaStatus = pisa.CreatePDF(
    #     #     sourceHtml,  # the HTML to convert
    #     #     dest=resultFile)  # file handle to recieve result
    #
    #     # close output file
    #     resultFile.close()  # close output file
    #
    #     # return True on success and False on errors
    #     return pisaStatus.err

    @list_route(methods=["POST"])
    def sendAutomated_tolid(self, request, *args, **kwargs):
        letterViewCreate = LetterViewSet()
        request.POST._mutable = True
        request.GET._mutable = True

        # detecting how who to recieve letters
        sign = HavalehForooshSigns.objects.filter(id=request.data['dt']['id']).first()
        approve = HavalehForooshApprove.objects.get(id=sign.HavalehForooshApproveLink)
        # havaleh = HavalehForooshs.objects.get(id=approve.havalehForooshLink)

        iii = []
        for a in approve.item['items']:
            d = a['PartCode'][0:2]
            iii.append(d)
        iii = query(iii).distinct().to_list()

        nahieh_1 = False
        nahieh_2 = False

        for i in iii:
            if i in ['66', '77', '88', '65', '75', '85']:
                nahieh_1 = True
            if i in ['89', '90', '93', '92', '93', '98']:
                nahieh_2 = True

        request.data.update(newLetter)
        user = MyUser.objects.get(username="automatedprocess")
        letterViewCreate.request = request
        letterViewCreate.format_kwarg = {}
        request.user = user
        url = request._request.environ['HTTP_ORIGIN'] + "/#!/Sales/hf/" + str(
            approve.havalehForooshLink) + "/details"
        recs['subject'] = "حواله فروش - تولید"
        recs['body'] = """
        <h3>حواله تولید زیر مورد تایید است</h3>
        <p>لطفا حواله ی زیر را به دقت بررسی کنید</p>
        <iframe style='width:100%;height:1000px' allowfullscreen  src=""" + url + """ name="example-month-input-directive"></iframe>
        """

        result = letterViewCreate.create(request, args, kwargs)
        letterID = result.data['id']

        recs['id'] = letterID
        recs['recievers'] = []
        if nahieh_1:
            recs['recievers'] = recs['recievers'] + nahieh_1_tolid
        if nahieh_2:
            recs['recievers'] = recs['recievers'] + nahieh_2_tolid
        request.data.update(recs)
        result = letterViewCreate.create(request, args, kwargs)

        return Response({})

    @list_route(methods=["POST"])
    def sendAutomated_foroosh(self, request, *args, **kwargs):
        letterViewCreate = LetterViewSet()
        request.POST._mutable = True
        request.GET._mutable = True

        # detecting how who to recieve letters
        sign = HavalehForooshSigns.objects.filter(id=request.data['dt']['id']).first()
        approve = HavalehForooshApprove.objects.get(id=sign.HavalehForooshApproveLink)
        # havaleh = HavalehForooshs.objects.get(id=approve.havalehForooshLink)

        iii = []
        for a in approve.item['items']:
            d = a['PartCode'][0:2]
            iii.append(d)
        iii = query(iii).distinct().to_list()

        nahieh_1 = False
        nahieh_2 = False

        for i in iii:
            if i in ['66', '77', '88', '65', '75', '85']:
                nahieh_1 = True
            if i in ['89', '90', '93', '92', '93', '98']:
                nahieh_2 = True

        request.data.update(newLetter)
        user = MyUser.objects.get(username="automatedprocess")
        letterViewCreate.request = request
        letterViewCreate.format_kwarg = {}
        request.user = user
        url = request._request.environ['HTTP_ORIGIN'] + "/#!/Sales/hf/" + str(
            approve.havalehForooshLink) + "/details"
        recs['subject'] = "حواله فروش - خروج"
        recs['body'] = """
        <h3>حواله فروش زیر مورد تایید است</h3>
        <p>لطفا حواله ی زیر را به دقت بررسی کنید</p>
        <iframe style='width:100%;height:1000px' allowfullscreen  src=""" + url + """ name="example-month-input-directive"></iframe>
        """

        result = letterViewCreate.create(request, args, kwargs)
        letterID = result.data['id']

        recs['id'] = letterID
        recs['recievers'] = []
        if nahieh_1:
            recs['recievers'] = recs['recievers'] + nahieh_1_foroosh
        if nahieh_2:
            recs['recievers'] = recs['recievers'] + nahieh_2_foroosh
        request.data.update(recs)
        result = letterViewCreate.create(request, args, kwargs)
        return Response({})

    @detail_route(methods=["GET"])
    def getDetailBarnamehSigns(self, request, *args, **kwargs):
        # getting signs
        signs = list(HavalehForooshSigns.objects.filter(HavalehForooshApproveLink=kwargs['id']))
        # qrexit_ + exit_id + _ + positionID + _ +stepID
        if len(signs) > 0:
            signs = HavalehForooshSignSerializer(instance=signs, many=True).data
            for s in signs:
                ps = PositionsDocument.objects.filter(positionID=s["positionID"]).order_by('-postDate')
                ps = ps[0]
                s["positionName"] = ps["profileName"]
                s["positionchartName"] = ps["chartName"]
                s["positionavatar"] = ps["avatar"]
                s["signCount"] = len(signs)
                s["hash"] = s['id']
        return Response(signs)

    @list_route(methods=["post"])
    def signHavaleh(self, request, *args, **kwargs):
        if int(request.data.get("signType")) != 1:  # means exit sign
            return Response({'errorcode': 1, 'msg': 'این امضا برای این تابع مجاز نیست'})

        signPass = request.data.get('signpass')
        uvs = UserViewSet()
        signPassIsOK = uvs.checkUserSignPass(request.user, signPass)

        if not signPassIsOK:
            return Response({'errcode': 2, 'msg': 'رمز دوم اشتباه است'})

        havalehID = request.data.get("VchHdrId")
        approveInstance = HavalehForooshApprove.objects.get(id=havalehID)
        stepNum = str(request.data.get("stepID"))
        if stepNum == "-1":  # means than finding latest step
            havalehSignsInstance = HavalehForooshSigns.objects.filter(
                havalehForooshLink=request.data.get("VchHdrId")).order_by("-whichStep").first()
            stepNum = str(havalehSignsInstance.whichStep + 1)

        positionInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        groupName = "group_havalehforoosh_permited_to_view_" + stepNum
        if stepNum == '6':
            groupName = "group_havalehforoosh_permited_to_view_4"
        if stepNum == '7':
            groupName = "group_havalehforoosh_permited_to_view_5"
        group = Group.objects.filter(name=groupName)
        if group.count() == 0:
            return Response({
                "errcode": 1,
                "msg": "گروه های عملیاتی توسط بهمنی ساخته نشده اند"
            })
            # raise Exception("1_" + groupName + " does not created Mohammad Please create it !")
        # user = MyUser.objects.get(id = positionInstance.userID)
        group = group[0]
        isAllowed = group.user_set.all().filter(id=positionInstance.userID).count()
        if isAllowed == 0:
            return Response({
                "errcode": 2,
                "msg": "شما مجور امضا زدن ندارید"
            })
            # raise Exception("2_" + str(positionInstance.userID) + " does not have permission !")
        dt = {
            "positionID": positionInstance.positionID,
            "HavalehForooshApproveLink": havalehID,
            "whichStep": int(stepNum),
            "comment": request.data.get("comment"),
            "dateOfPost": datetime.now()
        }

        # ------------------------------------------------------------
        # ------------------------------------------------------------
        # ------------------------------------------------------------
        # checking if previous sign signed
        # checking hierarchy of signs
        currentStep = int(stepNum)
        for c in range(1, currentStep):
            countOfPrevStep = HavalehForooshSigns.objects.filter(
                HavalehForooshApproveLink=havalehID,
                whichStep=c
            ).count()
            if (countOfPrevStep == 0) and (stepNum not in ['5', '6', '7']):
                return Response({
                    "errcode": 3,
                    "msg": "ترتیب امضا رعایت نشده است لطفا از امضای امضا کننده های قبلی اطمینان پیدا کنید"
                })
                # raise Exception("3_" +
                # str(positionInstance.userID) + " signed before previous signs > person before you must sgn first !")
        # --------------------------------------------------------------
        # --------------------------------------------------------------
        # --------------------------------------------------------------

        countOfSigns = HavalehForooshSigns.objects.filter(**dt).count()
        if countOfSigns > 0:
            return Response({
                "errcode": 4,
                "msg": "شما قبلا امضا زده اید - لطفا صبر کنید و صفحه را رفرش کنید"
            })
            # raise Exception("4_" + str(positionInstance.userID) + " you have signed it before why ??")

        # -----------------------------------------------
        # now removing current notifications of user
        Notifications.objects.filter(
            extra__havalehForooshID=havalehID
        ).delete()

        # -----------------------------------------------
        # -----------------------------------------------
        # -----------------------------------------------

        ser = HavalehForooshSignSerializer(data=dt)
        ser.is_valid(raise_exception=True)
        ser.save()

        # --------------------------------------------------------------------
        # --------------------------------------------------------------------
        # --------------------------------------------------------------------
        # if current step = 5 or 7 then send letter
        # --------------------------------------------------------------------
        # --------------------------------------------------------------------
        # we need forooshID

        # login url
        # url = "http://127.0.0.1:8000/api/v1/auth/login/"
        # data = {
        #     "username": "automatedprocess",
        #     "password": "********"
        # }
        # cookieName = CSRF_COOKIE_NAME
        #
        # r = requests.post(url, data)
        #
        # csrf = r.cookies.get(cookieName)
        # sessionID = r.cookies.get('sessionid')
        # cookies = {
        #     CSRF_COOKIE_NAME: csrf,
        #     'sessionid': sessionID
        # }
        #
        # url = "http://127.0.0.1:8000/SpecialApps/#!/home/Sales/hf/"+havalehID+"/details"
        # r = requests.get(url, cookies=cookies)
        #
        # print(r.status_code, r.reason)
        #
        # pd.read_html()

        url = "http://127.0.0.1:8000/SpecialApps/#!/home/Sales/hf/" + havalehID + "/details"
        # HTML(url).write_pdf("d:/dddd.pdf")

        #         if currentStep == 5:
        #             # getting customer profile to sms
        #             customerProfile = SalesCustomerProfile.objects.filter(
        #                 hamkaranCode=exitInstance.item["DLRef"].replace(' ', '')
        #             )
        #             if customerProfile.count() > 0:
        #                 self.sendSMS(
        #                     SalesCustomerProfile.objects.filter(
        #                         hamkaranCode=exitInstance.item["DLRef"].replace(' ', '')
        #                     )[0].exp["contact"]["cell"],
        #                     """با سلام
        # میزان 0کیلو تحویل راننده جلال عالی پور هفشجانی بشماره پلاک 973ع54-43 باموبایل 0913-183-3139 شد
        # مشاهده حواله :
        # http://app.****.ir/xt/::suid
        # **** ****
        #                     """.replace("")
        #
        #                 )
        if request.data.get('withSMS') == True:
            cellno = request.data.get('cellno')
            smms = """با سلام
امضای شما در حواله ی %s با کد %s ثبت شده است
تاریخ امضا %s
میزان خروجی %s
نام مشتری %s
**** ****""" % (
                "فروش",
                request.data.get('exitID'),
                mil_to_sh_with_time(datetime.now()),
                "??",
                "??",
            )
            sendSMS.delay(cellno, smms)
        return Response(ser.data)


class OLD_HavalehForooshConvViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = HavalehForooshConv.objects.all()
    serializer_class = HavalehForooshConvSerializer
    pagination_class = DetailsPagination

    def get_queryset(self):
        if self.request.method == "GET":
            self.queryset = self.queryset.filter(havalehForooshLink=int(self.request.query_params['convID']))
        return super(OLD_HavalehForooshConvViewSet, self).get_queryset()

    def initial(self, request, *args, **kwargs):
        if request.method != "GET" and request.method != "DELETE":
            posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            request.data["positionID"] = posiIns.positionID
            request.data["companyID"] = posiIns.companyID

        return super(OLD_HavalehForooshConvViewSet, self).initial(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request.data['dateOfPost'] = datetime.now()
        return super(OLD_HavalehForooshConvViewSet, self).create(request, *args, **kwargs)

    @detail_route(methods=["POST"])
    def AddToReplay(self, request, *args, **kwargs):
        dt = request.data
        dt["havalehForooshLink"] = kwargs["id"]
        sc = HavalehForooshConv(**dt)
        sc.save()
        return Response({})

    @list_route(methods=["GET"])
    def removeReplay(self, request, *args, **kwargs):
        ins = HavalehForooshConv.objects.get(id=request.query_params["replayID"])
        if ins.positionID == GetPositionViewset().GetCurrentPositionDocumentInstance(request).positionID:
            ins.delete()
        return Response({})

    @list_route(methods=["POST"])
    def weProduceIt(self, request, *args, **kwargs):
        if request.user.groups.all().filter(name="group_havalehforoosh_permited_to_tolid").count() == 0:
            return Response({"msg": "شما مجاز نیستید به تولید"})
        ins = HavalehForooshApprove.objects.get(id=request.data['approve']['id'])
        posi = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        dt = {
            'HavalehForooshApproveLink': str(ins.id),
            'positionID': posi.positionID,
            'comment': 'در برنامه تولید قرار گرفت',
            'dateOfPost': datetime.now(),
            'companyID': posi.companyID,
            'exp': {
                "approve": {
                    "positionID": posi.positionID,
                    "dateOfApprove": datetime.now(),
                    "type": 3,  # means accept
                    "avatar": posi.avatar,
                    "name": posi.profileName + "-" + posi.chartName
                }
            }
        }

        ans = HavalehForooshConvSerializer(data=dt)
        ans.is_valid(raise_exception=True)
        ans.save()

        return Response(ans.data)

    @list_route(methods=["POST"])
    def readyToSend(self, request, *args, **kwargs):
        if request.user.groups.all().filter(name="group_havalehforoosh_permited_to_tolid").count() == 0:
            return Response({"msg": "شما مجاز نیستید به تولید"})
        ins = HavalehForooshApprove.objects.get(id=request.data['approve']['id'])
        posi = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        dt = {
            'HavalehForooshApproveLink': str(ins.id),
            'positionID': posi.positionID,
            'comment': 'آماده ارسال',
            'dateOfPost': datetime.now(),
            'companyID': posi.companyID,
            'exp': {
                "approve": {
                    "positionID": posi.positionID,
                    "dateOfApprove": datetime.now(),
                    "type": 4,  # means accept
                    "avatar": posi.avatar,
                    "name": posi.profileName + "-" + posi.chartName
                }
            }
        }

        ans = HavalehForooshConvSerializer(data=dt)
        ans.is_valid(raise_exception=True)
        ans.save()
        return Response(ans.data)

    @detail_route(methods=["GET"])
    def getReplays(self, request, *args, **kwargs):

        all = HavalehForooshConv.objects.filter(havalehForooshLink=int(kwargs["id"])).order_by('-id')
        replays = []
        for pp in all:
            ps = PositionsDocument.objects.get(positionID=pp.positionID)
            replays.append({
                "isEditable": (pp["positionID"] == ps.positionID),
                "positionName": ps.profileName,
                "dateOfPost": pp.dateOfPost,
                "comment": pp.comment,
                "id": pp.id,
            })
        return Response(replays)

    def list(self, request, *args, **kwargs):
        result = super(OLD_HavalehForooshConvViewSet, self).list(request, *args, **kwargs)
        for d in result.data["results"]:
            positionDoc = PositionsDocument.objects.filter(
                positionID=d["positionID"],
                companyID=request.user.current_company_id,
            )

            sls = HavalehForooshConv.objects.filter(havalehForooshLink=d["havalehForooshLink"]).order_by("-id")
            replays = []
            for pp in sls:
                replays.append({
                    "positionName": PositionsDocument.objects.get(positionID=pp.positionID).profileName,
                    "dateOfPost": pp.dateOfPost,
                    "comment": pp.comment,
                    "id": pp.id,
                })
            d["replays"] = replays
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
            d["isEditable"] = (d["positionID"] == positionDoc.positionID)

        return result
