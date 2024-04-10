import collections

from django.core.cache import cache
from mongoengine import Q
from rest_framework.decorators import list_route
from rest_framework.renderers import HTMLFormRenderer, JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets as me_viewsets

from amspApp.BPMSystem.models import BigArchive
from amspApp.BPMSystem.serializers.BigArchiveSerializer import BigArchiveSerializer
from amspApp.CompaniesManagment.Positions.models import Position, PositionsDocument
from amspApp.amspUser.views.UserView import UserListPagination


class BigArchiveViewSet(me_viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = BigArchive.objects.all()
    serializer_class = BigArchiveSerializer
    pagination_class = UserListPagination
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer)

    @list_route(methods=['get'])
    def InboxStatistics(self, request, *args, **kwargs):
        pass


    """
    this def is cache enabled
    """

    def getData(self, posDocID):
        data = []
        cacheName = "OpenedProcess_" + str(posDocID)
        cacheProcess = cache.get(cacheName)
        if not cacheProcess:
            data = list(self.queryset.filter(
                (Q(starterId=posDocID) |
                 Q(prevPerformer__id=str(posDocID))) & Q(isProcessDone=False)).order_by("doneDate"))
            allData = [x._data for x in data]
            cache.set(cacheName, allData, 1500)
            cacheProcess = allData
        countOfNew = self.queryset.filter(
            (Q(starterId=posDocID) |
             Q(prevPerformer__id=str(posDocID))) & Q(isProcessDone=False)).count()
        if countOfNew != len(cacheProcess):
            allData = list(self.queryset.filter(
                (Q(starterId=posDocID) |
                 Q(prevPerformer__id=str(posDocID))) & Q(isProcessDone=False)).order_by("doneDate"))
            allData = [x._data for x in data]
            cache.set(cacheName, allData, 1500)
        return cache.get(cacheName)


    @list_route(methods=['get'])
    def getOpenedMyArchive(self, request, *args, **kwargs):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        posDocID = PositionsDocument.objects.get(positionID=pos.id)

        allData = self.getData(posDocID.id)

        # now counts of myrolls and which i start


        countOfDistictedProcessesStarter_PosID = collections.Counter([d["starterId"] for d in allData])
        countOfDistinctedProcessIHaveRoll_PosID = collections.Counter(
            [d["prevPerformer"]["id"] for d in allData if len(d["prevPerformer"]["id"]) > 18])
        countOfDistictedProcessesStarter_PosID = collections.Counter([d["starterId"] for d in allData])

        countOfDistinctedProcessIHaveRoll_PosID = collections.Counter(
            [d["prevPerformer"]["id"] for d in allData if len(d["prevPerformer"]["id"]) > 18])


        return Response({})


        # countOfDistictedProcessesStarter_ProcessID = collections.Counter([d["bpmnId"] for d in allData])
        # countOfDistinctedProcessIHaveRoll_PosID = collections.Counter([d["starterId"] for d in allData])

        # I_StartedProcess = groupby([["starterId", posDocID.id]], allData)





        self = self
        pass


