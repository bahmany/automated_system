from datetime import datetime

from asq.initiators import query
from django.contrib.auth.models import Group
from elasticsearch_dsl import Q
from elasticsearch_dsl import Search
from fcm_django.models import FCMDevice
from mongoengine import Q as QQ
from pyfcm import FCMNotification
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amsp.settings import FCM_DJANGO_SETTINGS
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.Secretariat.viewes.SecretariatsViews import SecretariatsViewSet
from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh_with_time, mil_to_sh, get_date_str
from amspApp.Letter.elasticConn import getElasticSearch
from amspApp.Letter.models import Letter, Inbox
from amspApp.Letter.search.InboxSearch import InboxSearchViewClass
from amspApp.Edari.Morekhasi.views.MorekhasiSaatiViews import MorekhasiSaatiViewSet
from amspApp.Notifications.models import Notifications, HasNotifications
from amspApp.Notifications.serializers.NotificationSerializer import NotificationsSerializer
from amspApp.Sales.models import HamkaranKhoroojSigns, HamkaranKhorooj, HamkaranHavaleForoosh, HavalehForooshSigns, \
    HavalehForooshApprove, HamkaranHavaleForooshOrderApprove
from amspApp.Sales.serializers.HavalehForooshSerializer import HavalehForooshSerializer
from amspApp.Sales.serializers.KhoroojSerializer import HamkaranKhoroojSerializer
from amspApp.Sales.views.ExitsView import KhoroojViewSet
from amspApp._Share.ListPagination import ListPagination
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage


def checkIfLettersAreCorrect(res):
    letterIDToDelete = []
    inboxIDToDelete = []
    ppp = res

    client = getElasticSearch()
    for r in res:
        defaultSecratriat = SecretariatsViewSet().GetDefaultSecretariatInstanceByUserID(r["userID"])

        if "extra" in r:
            if "letterID" in r["extra"]:
                countLetter = Letter.objects.filter(id=r["extra"]["letterID"]).count()
                if countLetter == 0:
                    letterIDToDelete.append(r["extra"]["letterID"])

            if "inboxID" in r["extra"]:
                countInbox = Inbox.objects.filter(id=r["extra"]["inboxID"]).count()

                # getting elastic index name
                elasticIndexName = InboxSearchViewClass().getElasticIndexName(r['userID'])
                # this line check if index exsits in elastic or not
                # this line protect exception of not found index in elastic and return null
                hasIndex = True
                if not client.indices.exists(index=elasticIndexName):
                    hasIndex = False
                    inboxIDToDelete.append(r["extra"]["inboxID"])

                elasticCount = Search(using=client, index=elasticIndexName, ).query(
                    Q("match", id=r["extra"]["inboxID"])).count() if hasIndex == True else 0
                if elasticCount == 0:
                    inboxIDToDelete.append(r["extra"]["inboxID"])

                if countInbox == 0:
                    inboxIDToDelete.append(r["extra"]["inboxID"])

    # searching letters
    for d in letterIDToDelete:
        ppp = query(ppp).where(lambda x: x["extra"]["letterID"] != d).to_list()

    # searching inboxes
    for d in inboxIDToDelete:
        ppp = query(ppp).where(lambda x: x["extra"]["inboxID"] != d).to_list()
    return ppp


class NotificationViewSet(viewsets.ModelViewSet):
    pagination_class = ListPagination
    lookup_field = "id"
    serializer_class = NotificationsSerializer
    queryset = Notifications.objects.all().order_by('-id')

    def get_queryset(self):
        self.queryset = self.queryset.filter(userID=self.request.user.id)
        self.queryset = self.queryset.filter(type__nin=[4, 5, 6, 7])
        return super(NotificationViewSet, self).get_queryset()

    def list(self, request, *args, **kwargs):

        self.get_all_unsings(request, *args, **kwargs)

        jt = request.query_params.get("jt")
        if (jt != None):
            self.queryset = self.queryset.filter(type=int(jt), extra__group_name=None)

        result = super(NotificationViewSet, self).list(request, *args, **kwargs)
        for noti in result.data["results"]:

            noti['summery'] = ''
            noti['senderName'] = ''
            noti['senderAvatar'] = ''
            noti['chartName'] = ''

            if noti.get("type") == 1:
                inboxInstance = Inbox.objects.filter(id=noti.get('extra').get('inboxID')).first()
                if inboxInstance:
                    noti['summery'] = inboxInstance.letter.get("subject")
                    noti['senderName'] = inboxInstance.sender.get("profileName")
                    noti['senderAvatar'] = inboxInstance.sender.get("avatar")
                    noti['chartName'] = inboxInstance.sender.get("profileName")

            if noti.get("type") == 4 and noti.get('extra', {}).get('group_name') == None:
                noti["signCount"] = HamkaranKhoroojSigns.objects.filter(khoroojLink=noti["extra"]["exitID"]).count()
                lastInstance = HamkaranKhoroojSigns.objects.filter(khoroojLink=noti["extra"]["exitID"]).order_by(
                    "-id").first()
                signs = list(HamkaranKhoroojSigns.objects.filter(khoroojLink=noti["extra"]["exitID"]))
                exitInstance = HamkaranKhorooj.objects.filter(id=noti['extra']['exitID']).first()
                if exitInstance is None:
                    aaa = 1
                else:
                    prevSigner = {}
                    prevSigner["name"] = "شما اولین امضا کننده هستید"
                    prevSigner["avatar"] = '/static/images/avatar_empty.jpg'
                    if noti["signCount"] > 0:
                        prevSigner = signs[noti["signCount"] - 1]
                        posiDoc = PositionsDocument.objects.get(positionID=prevSigner.positionID)
                        prevSigner = {}
                        prevSigner["name"] = posiDoc.profileName + " - " + posiDoc.chartName
                        prevSigner["avatar"] = posiDoc.avatar
                    noti["prev"] = prevSigner
                    noti["havaleNo"] = exitInstance.exp['t0_Number']
                    noti["signTitle"] = KhoroojViewSet.get_sign_title(noti['signCount'] + 1)
                    noti['shdateOfPost'] = mil_to_sh_with_time(lastInstance.dateOfPost)
            if noti.get("type") == 5:
                a = 1

        return result

    def retrieve(self, request, *args, **kwargs):
        self.get_queryset = super(NotificationViewSet, self).get_queryset()
        result = super(NotificationViewSet, self).retrieve(request, *args, **kwargs)
        noti = result.data
        noti['summery'] = ''
        noti['senderName'] = ''
        noti['senderAvatar'] = ''
        noti['chartName'] = ''
        if noti.get("type") == 1:
            inboxInstance = Inbox.objects.get(id=noti.get('extra').get('inboxID'))
            noti['summery'] = "نامه : " + inboxInstance.letter.get("subject")
            noti['senderName'] = inboxInstance.sender.get("profileName")
            noti['senderAvatar'] = inboxInstance.sender.get("avatar")
            noti['chartName'] = inboxInstance.sender.get("profileName")
        return result

    @list_route(methods=["get"])
    def GetTopNotification(self, request):
        try:
            return Response(self.GetTopNotificationByUserID(request.user.id))
        except Exception as ex:
            return Response([])

    @list_route(methods=["get"])
    def GetLatestNotificationID(self, request):
        # checking if user read the letter or not !
        res = list(HasNotifications.objects.filter(userID=request.user.id).limit(1))
        result = None
        if (len(res) > 0):
            if res[0].has:
                result = Response({"id": 1})
        if result == None:
            result = Response({"id": 0})
        NotificationsSerializer().markNotificationRead(request.user.id)
        return result

    def GetTopNotificationByUserID(self, userID):
        objs = self.queryset.filter(userID=userID).limit(20)
        res = NotificationsSerializer(instance=objs, many=True).data
        res = [dict(x) for x in res]
        # check if letter exists in inbox or not
        # if the letter is not in inbox or elasticsearch it means
        # it must be deleted
        res = checkIfLettersAreCorrect(res)

        objs = res
        NotificationsSerializer().markNotificationRead(userID)
        return objs

    def changesHappened(self, userID_int):
        NotificationsSerializer().changesHappened(userID_int)

    """
    msg_type = 4 = good_stay_in_location
    recievers : baskol, vorood be anbar
    
    msg_type = 5 = good_stay_in_location_with_QC_argue
    msg_type = 6 = good_moved_another_location_with_QC_argue
    msg_type = 7 = create_barcode
    
    msg_body = dict
    """

    def send_to_group_message_with_ws(self, msg_type, msg_content, group_name, msg_body):
        msg = str(msg_type) + "___" + msg_content
        users = list(Group.objects.get(name=group_name).user_set.all())

        for u in users:
            redis_publisher = RedisPublisher(facility='foobar', users=[u.username])
            dt = {
                'type': msg_type,
                'typeOfAlarm': 1,
                'priority': 1,
                'informType': 1,
                'userID': u.id,
                'dateOfPost': datetime.now(),
                'extra': {
                    'msg_type': msg_type,
                    'msg_content': msg_content,
                    'group_name': group_name,
                    'msg_body': msg_body,
                }
            }
            ser = NotificationsSerializer(data=dt)
            ser.is_valid(raise_exception=True)
            ser = ser.save()
            message = RedisMessage(msg + "___" + str(ser.id))
            redis_publisher.publish_message(message, expire=60)

    @list_route(methods=["get"])
    def get_all_unsings_foroosh(self, request, *args, **kwargs):
        # HamkaranHavaleForoosh
        current_groups = request.user.groups.filter(name__contains="group_havalehforoosh_permited_to_view_")
        current_groups = query(current_groups).select(lambda x: int(x.name.split('_')[5])).to_list()
        allowed_to_view = []
        for i in current_groups:
            if i == 1:
                allowed_to_view.append(1)
            if i == 2:
                allowed_to_view.append(2)
            if i == 3:
                allowed_to_view.append(3)
            if i == 4:
                allowed_to_view.append(4)
            if i == 5:
                allowed_to_view.append(4)
            if i == 6:
                allowed_to_view.append(4)
            if i == 7:
                allowed_to_view.append(4)

        """
        دریافت تمامی ح.اله هایی که امضای ۶ یا ۷ دارند ها
        """

        unsigns = list(HavalehForooshSigns.objects.aggregate(
            {
                "$match": {
                    "whichStep": {"$in": [6, 7]},
                }
            },
            {
                "$group": {
                    "_id": "HavalehForooshApproveLink",
                    "ids": {"$push": "$HavalehForooshApproveLink"}
                }
            }
        ))[0]['ids']

        unsigns = list(HamkaranHavaleForooshOrderApprove.objects.aggregate(
            {
                "$match": {
                    "_id": {"$in": unsigns}
                },
            }, {
                "$group": {
                    "_id": "havalehForooshLink",
                    "ids": {"$push": "$havalehForooshLink"}
                }
            }
        ))[0]['ids']

        hvfs = HamkaranHavaleForoosh.objects.filter(
            id__nin=unsigns,
            tarikheSodoor__gte=datetime.strptime('2021-10-21', '%Y-%m-%d'),
            vaziat__in=allowed_to_view
        )
        hvfs = HavalehForooshSerializer(instance=hvfs, many=True).data

        for m in hvfs:
            m['_type_of'] = 2
            m['_type_of_title'] = 'حواله فروش'
            m['_sort_date'] = datetime.strptime(m['tarikheSodoor'].split("T")[0], '%Y-%m-%d')
            m['_sort_date_sh'] = mil_to_sh(m['_sort_date'])
            m['_sort_date_sh_pretty'] = get_date_str(m['_sort_date'])
            m['exp']['TotalQty'] = query(
                HamkaranHavaleForooshOrderApprove.objects.get(
                    havalehForooshLink=m['id']).item['items']).sum(lambda x: x['OrderItemQuantity'])
            m['exp']['Unit'] = query(
                HamkaranHavaleForooshOrderApprove.objects.get(
                    havalehForooshLink=m['id']).item['items']).first().get('OrderItemUnitName', '')
        return hvfs




    @list_route(methods=["get"])
    def get_all_unsings_khorooj(self, request, *args, **kwargs):
        """
        دریافت تمامی خروج هایی که کمتر از ۵ امضا دارند
        """
        inss = list(HamkaranKhoroojSigns.objects.aggregate({
            "$match": {
                "whichStep": 5,
            }
        }, {

            "$group": {
                "_id": "whichStep",
                "count": {"$sum": 1},
                "ids": {"$push": "$khoroojLink"}
            }
        }, {
            "$sort": {
                "_id": -1
            }
        })
        )[0]['ids']

        hmks = HamkaranKhorooj.objects.filter(
            id__nin=inss,
            exp__t0_CreationDate__gte=datetime.strptime('2021-10-21', '%Y-%m-%d')).order_by("-id").limit(100)

        kmkss = HamkaranKhoroojSerializer(instance=hmks, many=True).data
        """
        این قسمت آخرین لول امضا را میکشد بیرون
        """
        for k in kmkss:
            all_steps = query(k['signs']).order_by_descending(lambda x: x['whichStep'], )
            if all_steps.count() == 0:
                k['latest_step'] = 0
            else:
                k['latest_step'] = query(k['signs']).order_by_descending(lambda x: x['whichStep'], ).first()[
                    'whichStep']

        """
        حالا باید دوستانی که در مراحل مختلف هستند شناسایی شود
        کار از این قرار است
        حالا میریم سراغ گروه کاربر جاری
        """

        current_group = request.user.groups.filter(name__contains="group_extis_permited_to_view_")
        current_groups = query(current_group).select(lambda x: int(x.name.split('_')[5])).to_list()
        my_allowed = query(kmkss).where(lambda x: x['latest_step'] + 1 in current_groups).to_list()
        for m in my_allowed:
            m['_type_of'] = 1
            m['_type_of_title'] = 'حواله خروج'
            m['_sort_date'] = m['dateOfPost']
            m['_sort_date_sh'] = mil_to_sh(m['_sort_date'])
            m['_sort_date_sh_pretty'] = get_date_str(m['_sort_date'])
        return my_allowed

    @list_route(methods=["get"])
    def sendTestNotif(self, request, *args, **kwargs):

        lll = FCMDevice.objects.filter(user_id=request.user.id).order_by("-id")
        reg_ids = [{"id": x.registration_id, "tp": x.type} for x in lll]

        push_service = FCMNotification(api_key=FCM_DJANGO_SETTINGS.get("FCM_SERVER_KEY"), json_encoder=None)
        ids = query(reg_ids).select(lambda x: x['id']).to_list()

        result = push_service.notify_multiple_devices(
            registration_ids=ids,
            message_title='tex',
            message_body='test t t t t ',
            message_icon=None,
            data_message=None,
            sound="default",
            badge=None,
            collapse_key=None,
            low_priority=False,
            condition=None,
            time_to_live=150,
            click_action='http://app.****.com',
            delay_while_idle=True,
            restricted_package_name=None,
            dry_run=False,
            color=None,
            tag=None,
            body_loc_key=None,
            body_loc_args=None,
            title_loc_key=None,
            title_loc_args=None,
            content_available=None)
        # push_service = FCMNotification(api_key=FCM_DJANGO_SETTINGS.get("FCM_SERVER_KEY"))
        return Response(result)

    @list_route(methods=["get"])
    def get_all_unsings(self, request, *args, **kwargs):
        khoroojs = self.get_all_unsings_khorooj(request, *args, **kwargs)
        forooshs = self.get_all_unsings_foroosh(request, *args, **kwargs)

        merger = khoroojs + forooshs
        merger = query(merger).order_by_descending(lambda x: x['_sort_date']).to_list()
        res = {
            'count': len(merger),
            'results': merger
        }
        return Response(res)

    @list_route(methods=["get"])
    def getUnreadsCount(self, request, *args, **kwargs):
        """
        جهت مرخصی ساعتی
        """
        msv = MorekhasiSaatiViewSet()
        msv.request = request
        q1 = QQ(exp__pos_modire_mali__is_signed__ne=True)
        q2 = QQ(exp__pos_masoole_edari__is_signed__ne=True)
        q3 = q1 & q2
        morekhasi_saati_count = msv.get_queryset().filter(q3).count()

        return Response({
            'edari': morekhasi_saati_count
        })
