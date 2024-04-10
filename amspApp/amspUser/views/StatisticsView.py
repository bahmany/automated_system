import json
import time
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseRedirect
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from rest_framework import viewsets, permissions, views
from rest_framework.response import Response

from amsp import settings
from amspApp.BPMSystem.models import Statistic
from amspApp.CompaniesManagment.Positions.models import PositionsDocument, Position
from amspApp.CompaniesManagment.Secretariat.viewes.SecretariatsViews import SecretariatsViewSet
from amspApp.Letter.elasticConn import getElasticSearch
from amspApp.Letter.models import InboxFolder, Inbox, InboxLabel
from amspApp.Letter.serializers.InboxSerializer import InboxSerializer


class GetStaticsViewSet(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    """
    it must change to signals ?:_)_____
    """

    def post(self, request, format=None):
        changed = False
        while not changed:
            posistionId = PositionsDocument.objects.get(userID=request.user.id,
                                                        companyID=request.user.current_company.id)
            counterObj = Statistic.objects.get(position_id=posistionId.id)
            counterDict = request.data
            if not 'lp' in counterDict: break
            if counterDict['lp'] != counterObj.Lp: changed = True
            if counterDict['newlp'] != counterObj.newLp: changed = True
            if counterDict['newmp'] != counterObj.newMp: changed = True
            if counterDict['mp'] != counterObj.Mp: changed = True
            time.sleep(3)
        return Response({'lp': counterObj.Lp,
                         'newlp': counterObj.newLp,
                         'newmp': counterObj.newMp,
                         'mp': counterObj.Mp
                         })

    def getFirstTimeInboxStatistics(self, request):
        posistion = Position.objects.get(user_id=request.user.id, company_id=request.user.current_company.id)
        counter = InboxSerializer().GetInboxCounter(posistion, None)
        result = json.dumps(counter)
        return HttpResponse(result, content_type="application/json")

    def UpdateStatics(self, request):
        posistion = Position.objects.get(user_id=request.user.id, company_id=request.user.current_company.id)
        cacheName = "inbox_static_" + str(posistion.id)
        cache.set(cacheName, None)
        cacheName = "folder_counter_" + str(posistion.id)
        cache.set(cacheName, None)
        cacheName = "folder_counter_" + str(posistion.id)
        cache.set(cacheName, None)

        self.getFirstTimeInboxStatistics(request)
        self.getInboxFoldersStatisticsRenewCache(posistion)
        self.getInboxLabelsStatisticsRenewCache(posistion)

        return HttpResponse({}, content_type="application/json")

    def getInboxStatistics(self, request):
        changed = False
        while not changed:
            posistion = Position.objects.get(user_id=request.user.id, company_id=request.user.current_company.id)
            data = json.loads(request.body.decode())
            counter = InboxSerializer().GetInboxCounter(posistion, data)
            if counter != data:
                return HttpResponse(json.dumps(counter), content_type="application/json")
            time.sleep(3)

    def getInboxFoldersStatisticsRenewCache(self, positionInstance):
        # getting entire folders
        # position = Position.objects.get(user_id=request.user.id, company_id=request.user.current_company.id)
        cacheName = "folder_counter_" + str(positionInstance.id)
        folders = InboxFolder.objects.filter(positionID=positionInstance.id)
        defaultSecratriat = SecretariatsViewSet().GetDefaultSecretariatInstanceByPositionInstance(positionInstance)

        indexName = settings.ELASTIC_INBOX_INDEXING_NAME + str(positionInstance.id)
        client = getElasticSearch()

        aggr = client.search(index=indexName, body={
            "query": {
                "bool": {
                    "must_not": [
                        {
                            "range": {
                                "itemPlace": {
                                    "gte": "3",  # it means exclude trash
                                    "lte": "5"
                                }
                            }
                        }
                    ]
                }
            },
            "aggs": {
                "folderCount": {
                    "terms": {
                        "field": "folders.id"
                    }
                }
            }
        })["aggregations"]['folderCount']['buckets']

        result = []
        for f in aggr:
            result.append({
                "id": f['key'],
                "count": f['doc_count']})
        cache.set("cacheName", result)
        return result

        # result = json.dumps(result)
        # return HttpResponse(result, content_type="application/json")

    def getInboxLabelsStatisticsRenewCache(self, positionInstance):
        # getting entire folders
        # position = Position.objects.get(user_id=request.user.id, company_id=request.user.current_company.id)
        cacheName = "labels_counter_" + str(positionInstance.id)
        labels = InboxLabel.objects.filter(positionID=positionInstance.id)
        defaultSecratriat = SecretariatsViewSet().GetDefaultSecretariatInstanceByPositionInstance(positionInstance)

        indexName = settings.ELASTIC_INBOX_INDEXING_NAME + str(positionInstance.id)
        client = getElasticSearch()

        # aggr = client.search(index=indexName, body={
        #     "query": {
        #         "bool": {
        #             "must_not": [
        #                 {
        #                     "range": {
        #                         "itemPlace": {
        #                             "gte": "3",  # it means exclude trash
        #                             "lte": "5"
        #                         }
        #                     }
        #                 }
        #             ]
        #         }
        #     },
        #     "aggs": {
        #         "labelsCount": {
        #             "terms": {
        #                 "field": "labels.id"
        #             }
        #         }
        #     }
        # })["aggregations"]['labelsCount']['buckets']
        aggr = client.search(index=indexName, body={
            "query": {
                "bool": {
                    "must_not": [
                        {
                            "range": {
                                "itemPlace": {
                                    "gte": "3",  # it means exclude trash
                                    "lte": "5"
                                }
                            }
                        }
                    ]
                }
            },
            "aggs": {
                "labelsCount": {
                    "terms": {
                        "field": "labels.id"
                    }
                }
            }
        })["aggregations"]['labelsCount']['buckets']

        result = []
        for f in aggr:
            result.append({
                "id": f['key'],
                "count": f['doc_count']})
        cache.set("cacheName", result)

        return result

        # result = json.dumps(result)
        # return HttpResponse(result, content_type="application/json")

    def getInboxFoldersStatistics(self, request):
        return HttpResponse({}, content_type="application/json")
        # getting entire folders
        # position = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        # cacheName = "folder_counter_" + str(position.id)
        # storedCache = cache.get(cacheName)
        # if storedCache == None:
        #     storedCache = self.getInboxFoldersStatisticsRenewCache(position)
        # result = json.dumps(storedCache)
        # return HttpResponse(result, content_type="application/json")

    def getInboxLabelsStatistics(self, request):
        return HttpResponse("", content_type="application/json")
        try:
            # getting entire folders
            position = Position.objects.get(user_id=request.user.id, company_id=request.user.current_company.id)
            cacheName = "labels_counter_" + str(position.id)
            storedCache = cache.get(cacheName)
            if storedCache == None:
                storedCache = self.getInboxLabelsStatisticsRenewCache(position)
            result = json.dumps(storedCache)
            return HttpResponse(result, content_type="application/json")
        except:
            return HttpResponse("", content_type="application/json")

