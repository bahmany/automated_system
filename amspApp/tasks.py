# Create your tasks here
from __future__ import absolute_import, unicode_literals

from datetime import datetime

import requests
from asq.initiators import query
from elasticsearch import Elasticsearch
from fcm_django.models import FCMDevice
from pyfcm import FCMNotification
from zeep import Client, Transport

from amsp import settings
from amsp.settings import FCM_DJANGO_SETTINGS
from amspApp.Sales.models import HavalehForooshApprove, HamkaranHavaleForooshOrderApprove
from .Letter.elasticConn import getElasticSearch
from .mycelery import app


@app.task
def sendSMS(_mobile, body):
    s = 1
    mobile = ""

    mobile = "+98" + _mobile
    mobile = mobile.replace("+98+98", "+98")
    mobile = mobile.replace("+9809", "+989")
    sms = {}
    sms["Message"] = body
    sms["DestinationAddress"] = mobile
    sms["Number"] = "100088197230"
    sms["UserName"] = "***"
    sms["Password"] = "***"
    sms["IP_Send"] = "http://193.104.22.14:2055/CPSMSService/Access"
    sms["Company"] = "****"
    sms["IsFlash"] = False
    sms["ident"] = "****+" + datetime.now().strftime('%Y%m%d%H%M%S%f')
    msg = ''.join(["%02X " % ord(x) for x in "سلام"]).strip().split()
    msg = [' %04d ' % (int(x),) for x in msg]
    # sms["Message"] = ''.join(msg).replace(' ', '')
    # AOurl = "http://panel.rahyab.ir/RahyabSMSService.asmx"
    session = requests.Session()
    session.trust_env = False
    transport = Transport(timeout=10)
    transport.session = session

    client = Client("http://193.104.22.227/RahyabSMSService.asmx?WSDL", transport=transport)
    response = client.service.SendSMS_Single(
        "RahyabSMS",
        "R@hy@bSoap_V1",
        sms["Message"],
        sms["DestinationAddress"],
        sms["Number"],
        sms["UserName"],
        sms["Password"],
        sms["Company"],
        "http://193.104.22.14:2055/CPSMSService/Access",
        "dd")
    return response


@app.task
def sendNotification(userID, result):
    print("------------------------------------------------------------")
    print("----------------start sending from ------------------------")
    print(userID)
    print("------------------------------------------------------------")
    lll = FCMDevice.objects.filter(user_id=userID).order_by("-id")
    reg_ids = [{"id": x.registration_id, "tp": x.type} for x in lll]

    # ll.send_data_message(data_message="Title","1_"+str(result.id))

    title = ""
    summery = ""
    link = ""
    if result.get("type"):
        if result['type'] == 1:
            title = "نامه جدید"
            summery = result['extra'].get("name", " ") + " - " + result['extra'].get("subject")
            link = "http://app.****.com/#!/dashboard/Letter/Inbox/" + result['extra'].get("inboxID") + "/Preview"
        if result['type'] == 4:
            title = "امضا خروج محصول"
            summery = result['extra'].get("customer", " ") + " - " + str(
                result['extra'].get("qty")) + " کیلو" + result['extra'].get(
                "dateOf")
            link = "http://app.****.com/SpecialApps/#!/Sales/kh/" + result['extra']['exitID'] + "/details"
        if result['type'] == 5:
            title = "امضا حواله فروش"
            summery = result['extra'].get("customer", " ") + " - " + str(
                result['extra'].get("qty")) + " کیلو" + " شماره " + result['extra']['havalehForooshID']

            link = "http://app.****.com/SpecialApps/#!/Sales/hf/" + result["extra"]["dbid"] + "/details"

        if result['type'] == 6:
            title = "یادداشت برای حواله فروش"
            hc = HamkaranHavaleForooshOrderApprove.objects.get(id=result['extra']['approveForooshID'])
            hno = hc.item['items'][0]['OrderItemID']

            summery = result['extra'].get("customer", " ") + " - " + str(
                result['extra'].get("qty")) + " کیلو" + " شماره " + str(hno)
            link = "http://app.****.com/SpecialApps/#!/Sales/hf/" + result["extra"]["dbid"] + "/details"

        if result['type'] == 7:
            title = "حواله فروش تغییر کرد"
            summery = result['extra'].get("customer", " ") + " - " + str(
                result['extra'].get("qty")) + " کیلو" + " شماره " + result['extra']['havalehForooshID']
            link = "http://app.****.com/SpecialApps/#!/Sales/hf/" + result["extra"]["dbid"] + "/details"

        if result['type'] == 8:
            title = "درخواست کالا"
            summery = result['extra'].get("customer", " ") + " - " + str(
                result['extra'].get("qty")) + " کیلو" + " شماره " + result['extra']['havalehForooshID']
            link = "http://app.****.com/SpecialApps/#!/Sales/hf/" + result["extra"]["dbid"] + "/details"

        push_service = FCMNotification(api_key=FCM_DJANGO_SETTINGS.get("FCM_SERVER_KEY"), json_encoder=None)

        # android msg
        ids = query(reg_ids).where(lambda x: x['tp'] == 'android').select(lambda x: x['id']).to_list()
        # print("---------------------------Android----------------------------------------------------------------")
        # print(ids)
        # print("-------------------------------------------------------------------------------------------")
        if len(ids) > 0:
            result = push_service.notify_multiple_devices(
                registration_ids=ids,
                message_title=title,
                message_body=summery,
                message_icon=None,
                data_message=None,
                sound="default",
                badge=None,
                collapse_key=None,
                low_priority=False,
                condition=None,
                time_to_live=5,
                click_action=link,
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
            print(result)

        push_service = FCMNotification(api_key=FCM_DJANGO_SETTINGS.get("FCM_SERVER_KEY"))
        ids = query(reg_ids).where(lambda x: x['tp'] == 'web').select(lambda x: x['id']).to_list()
        # print("---------------------------Web----------------------------------------------------------------")
        # print(ids)
        # print("-------------------------------------------------------------------------------------------")
        if len(ids) > 0:
            lll = FCMDevice.objects.filter(user_id=userID, registration_id__isnull=False)
            for id in ids:
                result = push_service.notify_single_device(
                    timeout=1,
                    registration_id=id,
                    data_message={
                        "message": {
                            "token": id,
                            "notification": {
                                "title": title,
                                "body": summery,
                                "click_action": link
                            }
                        }
                    }

                )
                print(result)

        print(result)

        # result.addBoth(got_result)
        # reactor.run()


@app.task
def saveToElastic(
        _positionID,
        _secretariatID,
        _inboxInstance_itemMode,
        _doc_type,
        _inboxInstance_id,
        _body
):
    # print("inbox id : " + str(_inboxInstance_id))
    es = getElasticSearch()
    dabirkhaneh_itemModes = [5, 6, 9, 10, 11, 12]
    indexName = settings.ELASTIC_INBOX_INDEXING_NAME + str(_positionID)
    if _inboxInstance_itemMode in dabirkhaneh_itemModes:
        indexName = settings.ELASTIC_SEC_INDEXING_NAME + _secretariatID
    es.indices.create(index=indexName, ignore=400)

    # elastic = {"elastic": es, "indexName": indexName}
    #
    # es = elastic["elastic"]
    es.index(
        index=indexName,
        doc_type=_doc_type,
        id=str(_inboxInstance_id),
        body=_body,
        request_timeout=5)
    # print("----------------letter indexed succ ------------------------")

    # return


@app.task
def saveToElasticBulk(
        _positionID,
        _secretariatID,
        _inboxInstance_itemMode,
        _doc_type,
        _inboxInstance_id,
        _body
):
    print("inbox id : " + str(_inboxInstance_id))
    es = getElasticSearch()
    dabirkhaneh_itemModes = [5, 6, 9, 10, 11, 12]
    indexName = settings.ELASTIC_INBOX_INDEXING_NAME + str(_positionID)
    if _inboxInstance_itemMode in dabirkhaneh_itemModes:
        indexName = settings.ELASTIC_SEC_INDEXING_NAME + _secretariatID
    es.indices.create(index=indexName, ignore=400)

    # elastic = {"elastic": es, "indexName": indexName}
    #
    # es = elastic["elastic"]
    es.index(
        index=indexName,
        doc_type=_doc_type,
        id=str(_inboxInstance_id),
        body=_body,
        request_timeout=5)
    print("----------------letter indexed succ ------------------------")

    # return


@app.task
def updateToElastic(
        _index,
        _doc_type,
        _id,
        _body, ):
    es = getElasticSearch()
    if es.exists(index=_index, id=_id, doc_type=_doc_type):
        es.update(
            index=_index,
            doc_type=_doc_type,
            id=_id,
            body=_body,
        )

        # print("----------------letter indexed succ updated ------------------------")
