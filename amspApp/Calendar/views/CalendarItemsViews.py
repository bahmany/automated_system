from datetime import datetime

from asq.initiators import query
from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets
import json
from amspApp.Calendar.models import CalendarItems
from amspApp.Calendar.queries.CalendarJsonQueries import calendarGetDateBetweenAggregate, InboxGetDateBetweenAggregate
from amspApp.Calendar.serializers.CalendarItemsSerializer import CalendarItemsSerializer
from amspApp.Infrustructures.Classes.DateConvertors import convertZoneToMilday, is_valid_shamsi_date, \
    CheckShamsiDateValidationInRequestAndConvert, parseZoneAwareDateStr, mil_to_sh
from amspApp.Letter.models import Inbox
from amspApp._Share.ListPagination import DetailsPagination
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset

__author__ = 'mohammad'


class CalendarItemsViewSet(viewsets.ModelViewSet):
    pagination_class = DetailsPagination
    lookup_field = "id"
    serializer_class = CalendarItemsSerializer
    DetailsPagination.page_size = 5

    # queryset = CalendarItems.objects.all()




    """
    here i want to put
    current date cal count
    current date unread letter count
    """

    @list_route(methods=['post'])
    def getCount(self, request, *args, **kwargs):
        agg_query = calendarGetDateBetweenAggregate()
        inbox_query = InboxGetDateBetweenAggregate()
        positionInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        qs = request.data['dates']
        qs = query(qs).select(lambda x: parseZoneAwareDateStr(convertZoneToMilday(self.request.user.id, x))).to_list()
        dateMilFrom = min(qs)
        dateMilTo = max(qs)

        # agg_query[0]['$match']['startDate']['$gte'] = dateMilFrom
        # agg_query[0]['$match']['startDate']['$lte'] = dateMilTo

        if ((dateMilTo - dateMilFrom).days > 60):
            raise Exception("Days are more than usual")

        calCount = list(
            CalendarItems.objects.filter(
                startDate__lte=dateMilTo,
                startDate__gte=dateMilFrom,
                userID=request.user.id).aggregate(*agg_query))

        inboxSeenCount = list(
            Inbox.objects.filter(
                currentPositionID=positionInstance.positionID,
                itemType=1,
                seen=True,
                dateOfObservable__lte=dateMilTo,
                dateOfObservable__gte=dateMilFrom).aggregate(*inbox_query))
        inboxUnSeenCount = list(
            Inbox.objects.filter(
                currentPositionID=positionInstance.positionID,
                itemType=1,
                seen=False,
                dateOfObservable__lte=dateMilTo,
                dateOfObservable__gte=dateMilFrom).aggregate(*inbox_query))

        calCount = query(calCount).select(lambda x:
                                          {"dt": mil_to_sh(
                                              str(x["_id"]["year"]) + "/" + str(x["_id"]["month"]) + "/" + str(
                                                  x["_id"]["day"]), splitter="/"),
                                              "count": x["count"]

                                          }
                                          ).to_list()
        inboxSeenCount = query(inboxSeenCount).select(lambda x:
                                                      {"dt": mil_to_sh(
                                                          str(x["_id"]["year"]) + "/" + str(
                                                              x["_id"]["month"]) + "/" + str(
                                                              x["_id"]["day"]), splitter="/"),
                                                          "count": x["count"]

                                                      }
                                                      ).to_list()
        inboxUnSeenCount = query(inboxUnSeenCount).select(lambda x:
                                                          {"dt": mil_to_sh(
                                                              str(x["_id"]["year"]) + "/" + str(
                                                                  x["_id"]["month"]) + "/" + str(
                                                                  x["_id"]["day"]), splitter="/"),
                                                              "count": x["count"]

                                                          }
                                                          ).to_list()

        return Response({
            "cal_count": calCount,
            "inb_seen": inboxSeenCount,
            "inb_unseen": inboxUnSeenCount,
        })

    @detail_route(methods=["post"])
    def partialUpdate(self, request, *args, **kwargs):
        obj = CalendarItems.objects.filter(userID=request.user.id).get(id=kwargs['id'])
        serial = CalendarItemsSerializer(instance=obj, data=request.data, partial=True)
        serial.is_valid(raise_exception=True)
        serial.update(obj, request.data)
        return Response(status=status.HTTP_200_OK)

    def get_queryset(self):
        dateMilFrom = convertZoneToMilday(self.request.user.id, self.request.query_params['q'] + " 00:00")
        dateMilTo = convertZoneToMilday(self.request.user.id, self.request.query_params['q'] + " 23:59")
        self.queryset = CalendarItems.objects.filter(
            userID=self.request.user.id,
            startDate__gte=dateMilFrom,
            startDate__lte=dateMilTo).order_by('finished', '-id')
        return super(CalendarItemsViewSet, self).get_queryset()

    def list(self, request, *args, **kwargs):
        return super(CalendarItemsViewSet, self).list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request.data['userID'] = request.user.id
        return super(CalendarItemsViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        obj = CalendarItems.objects.filter(userID=request.user.id).get(id=kwargs['id'])
        obj.delete()
        return Response(status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):

        checkResult = CheckShamsiDateValidationInRequestAndConvert(request, 'startDate', "زمان شروع",
                                                                   "زمان شروع را به درستی وارد نمایید")
        if checkResult["result"] == False:
            return Response({
                'status': 'Not Acceptable',
                'message': [{"fieldName": checkResult["fieldStrName"],
                             "message": checkResult["errorMessage"]}],
            }, status=status.HTTP_406_NOT_ACCEPTABLE)
        request.data['startDate'] = checkResult["converted"]

        checkResult = CheckShamsiDateValidationInRequestAndConvert(request, 'endDate', "زمان پایان",
                                                                   "زمان پایان را به درستی وارد نمایید")
        if checkResult["result"] == False:
            return Response({
                'status': 'Not Acceptable',
                'message': [{"fieldName": checkResult["fieldStrName"],
                             "message": checkResult["errorMessage"]}],

            }, status=status.HTTP_406_NOT_ACCEPTABLE)
        request.data['endDate'] = checkResult["converted"]
        request.data['userID'] = request.user.id

        return super(CalendarItemsViewSet, self).create(request, *args, **kwargs)
