import json
import re
import urllib
from asq.initiators import query
from datetime import datetime, timedelta

from django.http import HttpResponseForbidden
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q, FacetedSearch
from rest_framework import views
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework import viewsets
from rest_framework.response import Response
from amsp import settings
from amspApp.CompaniesManagment.Charts.serializers.ChartSerializers import ChartSerializer
from amspApp.CompaniesManagment.Charts.viewes.ChartViews import ChartViewSet
from amspApp.CompaniesManagment.Positions.models import Position
from amspApp.CompaniesManagment.Secretariat.viewes.SecretariatsViews import SecretariatsViewSet
from amspApp.Infrustructures.Classes.DateConvertors import convertZoneToMilday, mil_to_sh, mil_to_sh_with_time
from amspApp.Letter.elasticConn import getElasticSearch
from amspApp.Letter.models import InboxFolder, InboxLabel, SecTagItems
from amspApp.amspUser.models import MyUser

__author__ = 'mohammad'


# class InboxSearch(FacetedSearch):
# fields = ["any", "sender__profileName", "sender__chartName" ]
#


class InboxSearchViewClass(views.APIView):
    """
    to list user inbox with search
    """
    renderer_classes = (JSONRenderer,)
    paging_size = 10

    def generateOutputFromElastic(self, indexName, elas_search_result):
        result = elas_search_result.hits._l_
        newResult = []
        for r in result:
            z = r.to_dict()
            z["id"] = r.meta.id
            if "any" in z: z.pop("any")
            if "currentPositionID" in z: z.pop("currentPositionID")
            if "dateOfCreate" in z: z.pop("dateOfCreate")
            letter = {}
            if "letter" in z:
                if z["letter"]:
                    letter["attachmentCount"] = len(z["letter"]["attachments"]) if "attachments" in z["letter"] else 0
                    letter["hasAttachmant"] = z["letter"]["hasAttachmant"] if "hasAttachmant" in z["letter"] else False
                    letter["letterType"] = z["letter"]["letterType"] if "letterType" in z["letter"] else None
                    letter["periority"] = z["letter"]["periority"] if "periority" in z["letter"] else None
                    letter["security"] = z["letter"]["security"] if "security" in z["letter"] else None
                    letter["subject"] = z["letter"]["subject"] if "subject" in z["letter"] else None
                    letter["id"] = z["letter"]["id"] if "id" in z["letter"] else None
                    if "exp" in z["letter"]:
                        if "export" in z["letter"]["exp"]:
                            if "companyRecievers" in z["letter"]["exp"]["export"]:
                                if len(z["letter"]["exp"]["export"]["companyRecievers"]) > 0:
                                    letter["senderCompanyName"] = z["letter"]["exp"]["export"]["companyRecievers"][0][
                                        "name"]
                                    # letter["senderCompanyID"] = z["letter"]["exp"]["export"]["companyRecievers"][0][
                                    #     "id"]
                                    letter["senderCompanyGroup"] = z["letter"]["exp"]["export"]["companyRecievers"][0][
                                        "groupname"]

            z["letter"] = letter
            sender = {}
            rec = {}
            if "sender" in z:
                sender["avatar"] = z["sender"]["avatar"]
                sender["chartName"] = z["sender"]["chartName"]
                sender["profileName"] = z["sender"]["profileName"]
            if "reciever" in z:
                rec["avatar"] = z["reciever"]["avatar"]
                rec["chartName"] = z["reciever"]["chartName"]
                rec["profileName"] = z["reciever"]["profileName"]
                rec["others"] = z["reciever"]["others"] if "others" in z["reciever"] else {}
                rec["others_count"] = z["reciever"]["others_count"] if "others_count" in z["reciever"] else {}

            z["sender"] = sender
            z["reciever"] = rec
            if "readTimes" in z: z.pop("readTimes")
            # if "reciever" in z: z.pop("reciever")
            if "replyedInbox" in z: z.pop("replyedInbox")
            newResult.append(z)

        cc = {}
        cc["results"] = newResult
        cc["pageSize"] = self.paging_size
        cc["total"] = elas_search_result.hits.total

        client = getElasticSearch()
        cc["totalNoFilter"] = Search(using=client, index=indexName, )[:0].execute().hits.total
        return cc

    def generateOutputForSecFromElastic(self, indexName, elas_search_result):
        result = elas_search_result.hits._l_
        newResult = []
        for r in result:
            z = r.to_dict()
            z["id"] = r.meta.id
            if "any" in z: z.pop("any")
            if "currentPositionID" in z: z.pop("currentPositionID")
            if "dateOfCreate" in z: z.pop("dateOfCreate")
            letter = {}
            if "letter" in z:
                letter["exp"] = z['letter']['exp']
                letter["cover"] = z['letter']['exp']['cover'] if "cover" in z['letter']['exp'] else None
                letter["cover"] = letter["cover"].replace("q=", "q=thmum200_") if letter["cover"] else None
                letter["attachmentCount"] = len(z["letter"]["attachments"]) if "attachments" in z["letter"] else 0
                letter["letterType"] = z["letter"]["letterType"] if "letterType" in z["letter"] else None
                letter["periority"] = z["letter"]["periority"] if "periority" in z["letter"] else None
                letter["security"] = z["letter"]["security"] if "security" in z["letter"] else None
                letter["subject"] = z["letter"]["subject"] if "subject" in z["letter"] else None
                letter["id"] = z["letter"]["id"] if "id" in z["letter"] else None
                letter["sign"] = z['letter']['sign']['generatedSign'] if 'generatedSign' in z['letter']['sign'] else ""
                try :
                    letter["company_rec"] = [
                        {
                            # "companyID": x["companyID"], "groupID": x["group"]["id"] if x["group"] else None,
                            "name": x["name"],
                            "groupName": x["groupname"]} for x in
                        z['letter']['exp']['export']['companyRecievers']] if "export" in z['letter'][
                        'exp'] else {}
                except:
                    letter["company_rec"] = []

            z["letter"] = letter
            sender = {}
            rec = {}
            if "sender" in z:
                sender["avatar"] = z["sender"]["avatar"]
                sender["chartName"] = z["sender"]["chartName"]
                sender["profileName"] = z["sender"]["profileName"]
            if "reciever" in z:
                rec["avatar"] = z["reciever"]["avatar"]
                rec["chartName"] = z["reciever"]["chartName"]
                rec["profileName"] = z["reciever"]["profileName"]
                rec["others"] = z["reciever"]["others"] if "others" in z["reciever"] else {}
                rec["others_count"] = z["reciever"]["others_count"] if "others_count" in z["reciever"] else {}

            z["reciever"] = rec
            if "readTimes" in z: z.pop("readTimes")
            # if "reciever" in z: z.pop("reciever")
            if "replyedInbox" in z: z.pop("replyedInbox")
            newResult.append(z)

        cc = {}
        cc["results"] = newResult
        cc["pageSize"] = self.paging_size
        cc["total"] = elas_search_result.hits.total

        client = getElasticSearch()
        cc["totalNoFilter"] = Search(using=client, index=indexName, )[:0].execute().hits.total
        return cc

    def generateOutPutLink(self, addressWithOutQueryParam, previuosParams="", newParams={}):
        dest = list(newParams.keys())[0]
        found = False
        newGenParams = ""
        for q in previuosParams.split("&"):
            if q.split("=")[0] == dest:
                newGenParams = newGenParams + "&" + dest + "=" + str(newParams[dest])
                found = True
            else:
                newGenParams = newGenParams + "&" + q
        if found == False:
            newGenParams = newGenParams + "&" + dest + "=" + str(newParams[dest])

        return addressWithOutQueryParam + "?" + newGenParams[1:]

    def getElasticIndexName(self, userID):
        defaultCompanyID = MyUser.objects.get(id=userID).current_company_id
        pos = Position.objects.get(
            user=userID,
            company=defaultCompanyID)
        return settings.ELASTIC_INBOX_INDEXING_NAME + str(pos.id)

    def hasEnoughPermissionOnSecretariats(self, secInstance):
        if not secInstance.permission in ['111', '101', '110', '011']:
            return False
        return True

    def get(self, request, format=None, itemModes="", defaultItemPlace=1):
        pos = Position.objects.get(
            user=request.user,
            company=request.user.current_company)

        indexName = settings.ELASTIC_INBOX_INDEXING_NAME + str(pos.id)

        defaultSecratriat = SecretariatsViewSet().GetDefaultSecretariatInstance(request)

        # this is for switching between inbox and dabirkhaneh
        if itemModes == "Dabirkhaneh":
            # checking sec permissions
            if not self.hasEnoughPermissionOnSecretariats(defaultSecratriat):
                return HttpResponseForbidden()
            indexName = settings.ELASTIC_SEC_INDEXING_NAME + str(defaultSecratriat.secretariat.id)

        qq = self.CreateQuery(
            request.query_params,
            request.user,
            pos,
            defaultSecratriat,
            defaultItemPlace,
            itemModes=itemModes
        )
        # self.tmp_CreateQuery(
        #     request.query_params,
        #     request.user,
        #     pos,
        #     defaultSecratriat,
        #     defaultItemPlace,
        #     itemModes=itemModes
        # )

        startDate = qq["startDate"]
        endDate = qq["endDate"]
        qq = qq["q"]

        s = self.GetElasticData(
            indexName=indexName,
            startDate=startDate,
            endDate=endDate,
            QueryQ=qq
        )
        if "tags" in request.query_params:
            l = request.query_params["tags"].split(",")
            cc = []
            for ll in l:
                if len(ll) > 3:
                    cc.append(l)
            if len(cc) > 0:
                letterIds = SecTagItems.objects.filter(tag__in=l).only("letterID", )
                letterTags = query(letterIds).select(lambda x: str(x["letterID"])).to_list()
                s = s.filter("terms", letter__id=letterTags)

        # client = Elasticsearch()
        # s = Search(using=client, index=indexName, ) \
        # .filter('range', dateOfObservable={'lte': endDate, 'gte': startDate}) \
        # .query(QueryQ) \
        # .sort("-dateOfObservable")

        path = \
            request._request.environ["HTTP_REFERER"] + \
            request._request.META['PATH_INFO'][1:] + "?" + \
            request._request.META['QUERY_STRING']

        startFrom = 0
        if "page" in request.query_params:
            startFrom = (self.paging_size * (int(request.query_params["page"]) - 1))

        # client = Elasticsearch()
        # s = Search(using=client, index=indexName, ) \
        # .filter('range', dateOfObservable={'lte': endDate, 'gte': startDate}) \
        # .query(QueryQ) \
        # .sort("-dateOfObservable")

        if itemModes == "":
            res = self.generateOutputFromElastic(indexName, s[startFrom: startFrom + self.paging_size].execute())
        if itemModes == "Dabirkhaneh":
            res = self.generateOutputForSecFromElastic(indexName, s[startFrom: startFrom + self.paging_size].execute())

        for r in res['results']:
            r['sender']['avatar'] = r['sender']['avatar'].replace("=", "=thmum100_")
            r['sender']['avatar'] = r['sender']['avatar'].replace("thmum50CC", "thmum100")
            r['sender']['avatar'] = r['sender']['avatar'].replace("thmum50CC_thmum50CC_", "thmum100_")
            r['sender']['avatar'] = r['sender']['avatar'].replace("thmum100_thmum50CC_", "thmum100_")
            r['sender']['avatar'] = r['sender']['avatar'].replace("thmum100_thmum100_", "thmum100_")
            # r['dateOfObservable'] = mil_to_sh_with_time(r['dateOfObservable'])

        # handling custom pagination
        res['total'] = res.get('total', {})['value']
        res['totalNoFilter'] = res.get('totalNoFilter', {})['value']

        currentPageNumber = int(((startFrom + self.paging_size) / self.paging_size))
        nextNumber = currentPageNumber + 1
        nextPath = self.generateOutPutLink(
            request._request.environ["HTTP_REFERER"] + request._request.META['PATH_INFO'][1:],
            request._request.META['QUERY_STRING'],
            {"page": nextNumber})
        prevPath = self.generateOutPutLink(
            request._request.environ["HTTP_REFERER"] + request._request.META['PATH_INFO'][1:],
            request._request.META['QUERY_STRING'],
            {"page": str(int(((startFrom + self.paging_size) / self.paging_size)) - 1)})
        res["p"] = request.query_params["p"] if "p" in request.query_params else ""
        res["secname"] = defaultSecratriat.secretariat.name
        res["next"] = nextPath if (startFrom + self.paging_size) < res["total"] else None
        res["from"] = startFrom
        res["count"] = res["total"]
        res["to"] = startFrom + self.paging_size
        res["current_page"] = currentPageNumber
        res["num_pages"] = round(res['count'] / res["pageSize"])
        res["previous"] = None
        res["currentpath"] = self.generateOutPutLink(
            request._request.environ["HTTP_REFERER"] + request._request.META['PATH_INFO'][1:],
            request._request.META['QUERY_STRING'],
            {"page": currentPageNumber})
        if int(((startFrom + self.paging_size) / self.paging_size)) > 1:
            res["previous"] = prevPath
        res["first"] = self.generateOutPutLink(
            request._request.environ["HTTP_REFERER"] + request._request.META['PATH_INFO'][1:],
            request._request.META['QUERY_STRING'],
            {"page": 1})
        res["last"] = self.generateOutPutLink(
            request._request.environ["HTTP_REFERER"] + request._request.META['PATH_INFO'][1:],
            request._request.META['QUERY_STRING'],
            {"page": res["num_pages"]})
        res["page_myrange"] = []
        for pagesInspect in range(res["current_page"] - 2, res["current_page"]):
            if pagesInspect > 0:
                res["page_myrange"].append({"addr": self.generateOutPutLink(
                    request._request.environ["HTTP_REFERER"] + request._request.META['PATH_INFO'][1:],
                    request._request.META['QUERY_STRING'],
                    {"page": pagesInspect}),
                    "index": pagesInspect
                })
        for pagesInspect in range(res["current_page"], res["current_page"] + 2):
            if pagesInspect <= res["num_pages"] and pagesInspect > 0:
                res["page_myrange"].append({"addr": self.generateOutPutLink(
                    request._request.environ["HTTP_REFERER"] + request._request.META['PATH_INFO'][1:],
                    request._request.META['QUERY_STRING'],
                    {"page": pagesInspect}),
                    "index": pagesInspect})
        # end of handling custom pagination

        return Response(res)

    # def tmp_CreateQuery(self, query_params, user, pos, defaultSecratriat, DefaultItemPlace=1, itemModes=""):
    #     queries = []
    #     """
    #     Getting Search Place
    #     """
    #     searchPlace = ""
    #     searchDict = {
    #         "query": {
    #             "bool": {"must": [],
    #                      "filter": {"bool": {"must": []}}},
    #             "_source": {"excludes": ["any", "letter.body"]},
    #             "from": 0,
    #             "size": 20,
    #             "sort": [{"dateOfObservable": {"order": "desc"}}]
    #         },
    #
    #     }
    #
    #     beforeQuery = {}
    #
    #     if "p" in query_params:
    #         if query_params["p"] != None:
    #             if query_params["p"] != "undefined":
    #                 searchPlace = query_params["p"].split(",")
    #                 """
    #                 [0] = LetterType
    #                 [1] = LetterMode
    #                 [2] = LetterPlace
    #                 """
    #                 beforeQuery["itemTyoe"] = list(map(int, searchPlace[0].split(";")))
    #                 beforeQuery["itemMode"] = list(map(int, searchPlace[0].split(";")))
    #                 beforeQuery["itemPlace"] = list(map(int, searchPlace[0].split(";")))
    #                 beforeQuery["companies"] = query_params.get("companies", [])
    #                 beforeQuery["any"] = query_params.get("q")
    #                 beforeQuery["sender.profileName"] = query_params.get("q1")
    #                 beforeQuery["sender.chartName"] = query_params.get("q1")
    #                 beforeQuery["letter.body"] = query_params.get("q2")
    #                 beforeQuery["letter.subject"] = query_params.get("q2")
    #                 beforeQuery["letter.sign.generatedSign"] = query_params.get("q2")
    #
    #                 beforeQuery["startdate"] = datetime.now() - timedelta(days=1000)
    #                 beforeQuery["endDate"] = datetime.now() + timedelta(days=1000)
    #                 if "startdate" in query_params:
    #                     if query_params["startdate"] != "" and query_params["startdate"] != "undefined":
    #                         startDate = convertZoneToMilday(user.id, query_params["startdate"])
    #                         beforeQuery["startdate"] = datetime.strptime(startDate, "%Y-%m-%dT%H:%M")
    #                 if "enddate" in query_params:
    #                     if query_params["enddate"] != "" and query_params["enddate"] != "undefined":
    #                         endDate = convertZoneToMilday(user.id, query_params["enddate"])
    #                         beforeQuery["endDate"] = datetime.strptime(endDate, "%Y-%m-%dT%H:%M")
    #
    #                 beforeQuery["folders.id"] = query_params.get("fi")
    #                 beforeQuery["labels.id"] = query_params.get("li")
    #
    #                 beforeQuery["r"] = query_params.get("r")
    #                 beforeQuery["s"] = query_params.get("s")
    #                 beforeQuery["itemInDabirkhaneh"] = (itemModes == "Dabirkhaneh")
    #                 beforeQuery["currentPositionID"] = pos.id
    #                 # itemType = list(map(int, searchPlace[0].split(";")))
    #                 # if len(itemType) > 0:
    #                 #     if int(itemType[0]) != "-1":
    #                 #         searchDict["query"]["bool"]["filter"]["must"].append(
    #                 #             {"terms": {"itemType": list(map(int, itemType))}}
    #                 #         )
    #                 # # queries.append(Q("match", itemType=int(itemType[0])))
    #                 #
    #                 # else:
    #                 #     vv = []
    #                 #     for im in itemType:
    #                 #         vv.append(Q("match", itemType=int(im)))
    #                 #     queries.append(Q("bool", should=vv, minimum_should_match=2))
    #
    #                 # this line filter auto hamesh that just show auto hamesh in specific portion
    #                 # if int(searchPlace[0]) != "5":
    #                 #     # queries.append(~Q("match", itemType=5))
    #                 #     if not searchDict["query"]["bool"]["filter"].get("must_not"):
    #                 #         searchDict["query"]["bool"]["filter"]["must_not"] = []
    #                 #
    #                 #     searchDict["query"]["filter"]["bool"]["must_not"].append(
    #                 #         {"terms": {"itemType": [5]}}
    #                 #     )
    #
    #                 # ----------------------------------------------
    #                 # this is for multi itemMode purposes for example 5 and 9 in export letters lists
    #                 # itemMode = searchPlace[1].split(";")
    #                 # if len(itemMode) > 0:
    #                 #     if int(searchPlace[1]) != "-1":
    #                 #         searchDict["query"]["bool"]["filter"]["must"].append(
    #                 #             {"terms": {"itemType": list(map(int, itemMode))}}
    #                 #         )
    #
    #                 # queries.append(Q("match", itemMode=int(searchPlace[1])))
    #                 # else:
    #                 #     vv = []
    #                 #     for im in itemMode:
    #                 #         vv.append(Q("match", itemMode=int(im)))
    #                 #     queries.append(Q("bool", should=vv, minimum_should_match=1))
    #                 # ----------------------------------------------
    #
    #                 # itemPlace = searchPlace[2].split(";")
    #                 # if len(itemMode) > 0:
    #                 #     if int(searchPlace[1]) != "-1":
    #                 #         searchDict["query"]["bool"]["filter"]["must"].append(
    #                 #             {"terms": {"itemPlace": list(map(int, itemMode))}}
    #                 #         )
    #                 #     else:
    #                 #         searchDict["query"]["bool"]["filter"]["must"].append(
    #                 #             {"terms": {"itemPlace": [DefaultItemPlace]}}
    #                 #         )
    #                 # else:
    #                 #     searchDict["query"]["bool"]["filter"]["must"].append(
    #                 #         {"terms": {"itemPlace": [DefaultItemPlace]}}
    #                 #     )
    #                 # if "companies" in query_params:
    #                 #     if query_params["companies"] != "" and query_params["companies"] != "companies":
    #                 #         co = query_params["companies"].split("-")
    #                 #         vv = []
    #                 #         for c in co:
    #                 #             # for export letters list
    #                 #             if ('5' in itemMode) or ('9' in itemMode):
    #                 #                 # vv.append(Q("match", letter__exp__export__companyRecievers__name=c))
    #                 #                 searchDict["query"]["bool"]["filter"]["must"].append(
    #                 #                     {"terms": {"letter.exp.export.companyRecievers.name": [c]}}
    #                 #                 )
    #                 #                 # queries.append(Q("bool", must=vv, minimum_should_match=1))
    #
    #                 # if "q" in query_params:
    #                 #     if query_params["q"] != "" and query_params["q"] != "undefined":
    #                 #         searchDict["query"]["bool"]["filter"]["must"].append(
    #                 #             {"terms": {"any": [query_params["q"].encode("UTF-8")]}}
    #                 #         )
    #                 #         queries.append(Q("match", any=query_params["q"].encode("UTF-8")))
    #                 # if "q1" in query_params:
    #                 #     if query_params["q1"] != "" and query_params["q1"] != "undefined":
    #                 #         if not searchDict["query"]["bool"]["filter"]["should"]:
    #                 #             searchDict["query"]["bool"]["filter"]["should"] = []
    #
    #                 # searchDict["query"]["bool"]["filter"]["should"].append({
    #                 #     "terms": {"sender.profileName": query_params["q1"].encode("UTF-8")}
    #                 # })
    #                 # searchDict["query"]["bool"]["filter"]["should"].append({
    #                 #     "terms": {"sender.chartName": query_params["q1"].encode("UTF-8")}
    #                 # })
    #
    #                 # queries.append(
    #                 #     Q("multi_match",
    #                 #       query=query_params["q1"].encode("UTF-8"),
    #                 #       fields=["sender.profileName", "sender.chartName"]))
    #     # if "q2" in query_params:
    #     #     if query_params["q2"] != "" and query_params["q2"] != "undefined":
    #     #         queries.append(
    #     #             Q("bool",
    #     #               should=[
    #     #                   Q("match", letter__body=query_params["q2"].encode("UTF-8")),
    #     #                   Q("match", letter__subject=query_params["q2"].encode("UTF-8")),
    #     #                   Q("match", letter__sign__generatedSign=query_params["q2"].encode("UTF-8")),
    #     #               ]
    #     #               )
    #     #         )
    #
    #     # startDate = datetime.now() - timedelta(days=1000)
    #     # endDate = datetime.now() + timedelta(days=1000)
    #
    #     # if "startdate" in query_params:
    #     #     if query_params["startdate"] != "" and query_params["startdate"] != "undefined":
    #     #         startDate = convertZoneToMilday(user.id, query_params["startdate"])
    #     #         startDate = datetime.strptime(startDate, "%Y-%m-%dT%H:%M")
    #     #
    #     # if "enddate" in query_params:
    #     #     if query_params["enddate"] != "" and query_params["enddate"] != "undefined":
    #     #         endDate = convertZoneToMilday(user.id, query_params["enddate"])
    #     #         endDate = datetime.strptime(endDate, "%Y-%m-%dT%H:%M")
    #
    #     # if "fi" in query_params:
    #     #     if query_params["fi"]:
    #     #         if query_params["fi"] != "undefined":
    #     #             inboxFolder = InboxFolder.objects.get(
    #     #                 id=query_params["fi"],
    #     #                 positionID=pos.id)
    #     #             queries.append(Q("match", folders__id=str(inboxFolder.id)))
    #     # if "li" in query_params:
    #     #     if query_params["li"]:
    #     #         if query_params["li"] != "undefined":
    #     #             inboxLabel = InboxLabel.objects.get(
    #     #                 id=query_params["li"],
    #     #                 positionID=pos.id)
    #     #             queries.append(Q("match", labels__id=str(inboxLabel.id)))
    #     # if 'r' in query_params:
    #     #     if query_params["r"] != "undefined":
    #     #         if query_params["r"]:
    #     #             if query_params["r"] == "2":
    #     #                 queries.append(Q("match", seen=False))
    #     #             if query_params["r"] == "3":
    #     #                 queries.append(Q("match", seen=True))
    #     # if 's' in query_params:
    #     #     if query_params["s"] != "undefined":
    #     #         if query_params["s"]:
    #     #             if query_params["s"] == "2":
    #     #                 queries.append(Q("match", star=True))
    #     #
    #     # qq = Q()
    #     # if not itemModes == "Dabirkhaneh":
    #     #     qq = Q("match", currentPositionID=pos.id)
    #     # for q in queries:
    #     #     if q != None:
    #     #         qq = qq + q
    #     #
    #     # if "starred" in query_params:
    #     #     if query_params["starred"] == "true":
    #     #         qq = qq + Q("match", star=True)
    #
    #     return {"q": "", "startDate": "", "endDate": ""}

    def CreateQuery(self, query_params, user, pos, defaultSecratriat, DefaultItemPlace=1, itemModes=""):
        queries = []
        """
        Getting Search Place
        """
        searchPlace = ""
        if "p" in query_params:
            if query_params["p"] != None:
                if query_params["p"] != "undefined":
                    searchPlace = query_params["p"].split(",")
                    """
                    [0] = LetterType
                    [1] = LetterMode
                    [2] = LetterPlace
                    """
                    itemType = searchPlace[0].split(";")
                    if len(itemType) == 1:
                        if int(itemType[0]) != -1: queries.append(Q("match", itemType=int(itemType[0])))
                    else:
                        vv = []
                        for im in itemType:
                            vv.append(Q("match", itemType=int(im)))
                        queries.append(Q("bool", should=vv, minimum_should_match=2))

                    # this line filter auto hamesh that just show auto hamesh in specific portion
                    if int(searchPlace[0]) != 5: queries.append(~Q("match", itemType=5))

                    # ----------------------------------------------
                    # this is for multi itemMode purposes for example 5 and 9 in export letters lists
                    itemMode = searchPlace[1].split(";")
                    if len(itemMode) == 1:
                        if int(searchPlace[1]) != -1: queries.append(Q("match", itemMode=int(searchPlace[1])))
                    else:
                        vv = []
                        for im in itemMode:
                            vv.append(Q("match", itemMode=int(im)))
                        queries.append(Q("bool", should=vv, minimum_should_match=1))
                    # ----------------------------------------------

                    if int(searchPlace[2]) != -1:
                        queries.append(Q("match", itemPlace=int(searchPlace[2])))
                    else:
                        # this is for filtering deleted items
                        queries.append(Q("match", itemPlace=DefaultItemPlace))

        if "companies" in query_params:
            if query_params["companies"] != "" and query_params["companies"] != "companies":
                co = query_params["companies"].split("-")
                vv = []
                for c in co:
                    # for export letters list
                    if ('5' in itemMode) or ('9' in itemMode):
                        vv.append(Q("match", letter__exp__export__companyRecievers__name=c))
                queries.append(Q("bool", must=vv, minimum_should_match=1))

        if "q" in query_params:
            if query_params["q"] != "" and query_params["q"] != "undefined":
                queries.append(Q("match", any=query_params["q"].encode("UTF-8")))
        if "q1" in query_params:
            if query_params["q1"] != "" and query_params["q1"] != "undefined":
                queries.append(
                    Q("multi_match",
                      query=query_params["q1"].encode("UTF-8"),
                      fields=["sender.profileName", "sender.chartName"],
                      type="phrase_prefix"))
        if "q2" in query_params:
            if query_params["q2"] != "" and query_params["q2"] != "undefined":
                queries.append(
                    Q("multi_match",
                      query=query_params["q2"].encode("UTF-8"),
                      fields=["letter.body", "letter.subject", "letter.sign.generatedSign"],
                      type="phrase_prefix"
                      )
                )

        startDate = datetime.now() - timedelta(days=99000)
        endDate = datetime.now() + timedelta(days=99000)

        if "startdate" in query_params:
            if query_params["startdate"] != "" and query_params["startdate"] != "undefined":
                startDate = convertZoneToMilday(user.id, query_params["startdate"])
                startDate = datetime.strptime(startDate, "%Y-%m-%dT%H:%M")

        if "enddate" in query_params:
            if query_params["enddate"] != "" and query_params["enddate"] != "undefined":
                endDate = convertZoneToMilday(user.id, query_params["enddate"])
                endDate = datetime.strptime(endDate, "%Y-%m-%dT%H:%M")

        if "fi" in query_params:
            if query_params["fi"]:
                if query_params["fi"] != "undefined":
                    inboxFolder = InboxFolder.objects.get(
                        id=query_params["fi"],
                        positionID=pos.id)
                    queries.append(Q("match", folders__id=str(inboxFolder.id)))
        if "li" in query_params:
            if query_params["li"]:
                if query_params["li"] != "undefined":
                    inboxLabel = InboxLabel.objects.get(
                        id=query_params["li"],
                        positionID=pos.id)
                    queries.append(Q("match", labels__id=str(inboxLabel.id)))
        if 'r' in query_params:
            if query_params["r"] != "undefined":
                if query_params["r"]:
                    if query_params["r"] == "2":
                        queries.append(Q("match", seen=False))
                    if query_params["r"] == "3":
                        queries.append(Q("match", seen=True))
        if 's' in query_params:
            if query_params["s"] != "undefined":
                if query_params["s"]:
                    if query_params["s"] == "2":
                        queries.append(Q("match", star=True))

        qq = Q()
        if not itemModes == "Dabirkhaneh":
            qq = Q("match", currentPositionID=pos.id)
        for q in queries:
            if q != None:
                qq = qq + q

        if "starred" in query_params:
            if query_params["starred"] == "true":
                qq = qq + Q("match", star=True)

        return {"q": qq, "startDate": startDate, "endDate": endDate}

    def GetElasticData(self, indexName, startDate, endDate, QueryQ):
        client = getElasticSearch()
        s = Search(using=client, index=indexName, ) \
            .filter('range', dateOfObservable={'lte': endDate, 'gte': startDate}) \
            .query(QueryQ) \
            .sort("-dateOfObservable") \
            .exclude("terms", fields=["any"])
        return s
