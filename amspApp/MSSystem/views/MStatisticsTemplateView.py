from copy import copy
import io
import pickle
import asq
from bson import ObjectId
import math
from asq.initiators import query
from django.db.models import Max, Min
from rest_framework_mongoengine import viewsets

from amspApp.BPMSystem.serializers.LPInboxSerializer import LPInboxSerializer
from amspApp.BPMSystem.serializers.ShowDiagramSerializer import ShowDiagramSerializer
from amspApp.BPMSystem.serializers.ShowFormSerializer import ShowFormSerializer
from amspApp.CompaniesManagment.Positions.serializers.PositionSerializer import PositionDocumentSerializer
from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh
from amspApp.Infrustructures.MySpiffWorkflow.bpmn.parser.util import xpath_eval
from datetime import datetime
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from mongoengine import Q
from rest_framework.decorators import detail_route, list_route
from rest_framework_mongoengine import viewsets as me_viewsets
from rest_framework.renderers import HTMLFormRenderer, JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework import status
from amspApp.BPMSystem.MyEngine.BpmEngine import BpmEngine
from amspApp.BPMSystem.models import LunchedProcess, LunchedProcessArchive, Statistic, BigArchive
from amspApp.BPMSystem.serializers.LunchedProcessSerializer import LunchedProcessSerializer
from amspApp.BPMSystem.serializers.MessageProcessSerializer import MessageProcessSerializer
from amspApp.CompaniesManagment.Processes.models import Bpmn
from amspApp.CompaniesManagment.Positions.models import Position, PositionsDocument
from amspApp.CompaniesManagment.Processes.serializers.BpmnSerializer import BpmnSerializer
from amspApp.FileServer.views.BpmsFileView import BpmsFileViewSet
from amspApp.MSSystem.models import MSTemplate, MSData
from amspApp.MSSystem.serializers.MSDataSerializer import MSDataSerializer
from amspApp.MSSystem.serializers.MSTemplateSerializer import MSTemplateSerializer, MSTemplateInboxSerializer
from amspApp._Share.ListPagination import DetailsPagination
from amspApp.amspUser.views.UserView import UserListPagination


class MStatisticsTemplateViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = MSTemplate.objects.all()
    serializer_class = MSTemplateInboxSerializer
    pagination_class = DetailsPagination

    @list_route(methods=["get"])
    def getPosDoc(self, request):
        posDocID = request.query_params["q"]
        posIns = PositionsDocument.objects.get(id=posDocID)
        posRes = PositionDocumentSerializer(instance=posIns).data
        # here we have a security bugs //

        return Response(posRes)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        posDoc = PositionsDocument.objects.get(positionID=pos.id)

        serializer = MSTemplateSerializer(instance)
        result = (str(posDoc.id) == serializer.data["position_id"])
        if result:
            return Response(serializer.data)
        else:
            return Response({"msg": "you are not author of this template"}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        serializer = MSTemplateSerializer(data=request.data)
        if serializer.is_valid():
            posistionObj = PositionsDocument.objects.get(userID=request.user.id,
                                                         companyID=request.user.current_company.id)
            serializer.validated_data['position_id'] = posistionObj.id
            serializer.validated_data['companyId'] = request.user.current_company.id
            new = serializer.create(serializer.validated_data)
            return Response(str(new.pk), status=status.HTTP_201_CREATED)
        return Response({'message': serializer.errors,
                         'status': 'Bad request'},
                        status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = MSTemplateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def get_queryset(self):
        posInstance = PositionsDocument.objects.get(userID=self.request.user.id,
                                                    companyID=self.request.user.current_company.id)
        self.queryset = self.queryset.filter(Q(position_id=posInstance.id) | (
        Q(publishedUsersDetail__positionID=posInstance.positionID, publishedUsersDetail__canEdit=True)))
        self.pagination_class.page_size = 50;
        return super(MStatisticsTemplateViewSet, self).get_queryset()

    @detail_route(methods=["get"])
    def GetSmallStatic(self, request, *args, **kwargs):
        instance = self.queryset.filter(id=kwargs['id'])
        if instance.count() == 0:
            return Response([])
        objs = MSData.objects.filter(template_id=instance[0].id).order_by("-entryDate").limit(10)
        avg = MSData.objects.filter(template_id=instance[0].id).average("value")
        maxIns = MSData.objects.filter(template_id=instance[0].id).order_by("-value").limit(1)
        max = 0
        maxTime = ""
        if maxIns.count() > 0:
            max = maxIns[0].value
            maxTime = mil_to_sh(maxIns[0].entryDate)
        else:
            max = 0
        # msds = [{"value":x.value, "dt":x.entryDate} for x in objs]
        msds = {"name": instance[0].name, "desc": instance[0].desc,
                "items": [{"val": x.value, "dt": mil_to_sh(x.entryDate)} for x in objs],
                "itemsJV": [x.value for x in objs],
                "avg": int(avg),
                "max": int(max),
                "maxTime": maxTime,
                "exp": instance[0].exp,
                "tmpl": MSTemplateInboxSerializer(instance=instance[0]).data["id"],
                "id": str(instance[0].id)
                }
        return Response(msds)

    @list_route(methods=["post"])
    def GetSmallStaticContrastive(self, request, *args, **kwargs):
        staticIds = request.data
        ids = []
        for s in staticIds:
            objs = list(MSData.objects.filter(template_id=s).order_by("-entryDate").limit(10))
            ids.append(objs)
        # generating labels
        labels = []
        for s in ids:
            for ss in s:
                labels.append(ss.entryDate.date())
        distictLabels = list(query(labels).distinct().order_by())

        fres = []
        for s in ids:
            cc = []
            tmplInstamce = MSTemplate.objects.get(id=s[0].template_id)
            tmplInstamce = MSTemplateSerializer(instance=tmplInstamce).data
            for d in distictLabels:
                result = query(s).where(lambda x: x.entryDate.date() == d).order_by_descending(lambda x: x.id).to_list()
                firstOne = None
                if len(result) > 0:
                    firstOne = result[0].value

                if "publishedUsersDetail" in tmplInstamce: tmplInstamce.pop("publishedUsersDetail")
                if "publishedUsers" in tmplInstamce: tmplInstamce.pop("publishedUsers")
                cc.append({
                    "date": mil_to_sh(d),
                    "value": firstOne,
                })
            cc.reverse()
            max = MSData.objects.filter(template_id=tmplInstamce["id"]).order_by("-value").limit(1)[0]
            min = MSData.objects.filter(template_id=tmplInstamce["id"]).order_by("value").limit(1)[0]
            latest = MSData.objects.filter(template_id=tmplInstamce["id"]).order_by("-id").limit(1)[0]
            fres.append(
                {
                    "values": cc,
                    "tmpl": tmplInstamce,
                    "exp": {
                        "min": min.value,
                        "minDate": mil_to_sh(min.entryDate),
                        "max": max.value,
                        "maxDate": mil_to_sh(max.entryDate),
                        "latest": latest.value,
                        "latestDate": mil_to_sh(latest.entryDate)
                    }
                })
        lbls = [mil_to_sh(x) for x in distictLabels]
        lbls.reverse()
        outPut = {
            'labels': lbls,
            'datasets': fres
        }

        return Response(outPut)

    def list(self, request, *args, **kwargs):

        posInstance = PositionsDocument.objects.get(userID=self.request.user.id,
                                                    companyID=self.request.user.current_company.id)

        result = super(MStatisticsTemplateViewSet, self).list(request, *args, **kwargs)
        for r in result.data["results"]:
            r["isOwner"] = True if r["position_id"] == str(posInstance.id) else False
            if not r["isOwner"]:
                creatorPosIns = PositionsDocument.objects.filter(id=r["position_id"]).first()
                r["creatorName"] = str(creatorPosIns.profileName) + " - " + str(
                    creatorPosIns.chartName) if creatorPosIns != None else "بدون سمت"

        return result

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        objsForDel = MSData.objects.filter(template_id=instance.id)
        for itm in objsForDel:
            itm.delete()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @list_route(methods=['get'])
    def GetCurrentBoxes(self, request, *args, **kwargs):
        posistionObj = PositionsDocument.objects.get(userID=request.user.id,
                                                     companyID=request.user.current_company.id)

        if not 'dashboard' in posistionObj.desc:
            posistionObj.desc['dashboard'] = {}
            curExtra = {'msBox1': '',
                        'msBox2': '',
                        'msBox3': '',
                        'msBox4': ''}
            posistionObj.desc['dashboard'] = curExtra
            posistionObj.save()

            msTemplates = MSTemplate.objects.filter(companyId=request.user.current_company.id,
                                                    publishedUsers__contains=str(posistionObj.id))
            i = 1
            newDAssj = curExtra
            for itm in msTemplates:
                if i > 4:
                    break
                newDAssj['msBox%s' % (str(i),)] = str(itm.id)
                i += 1
            posistionObj.desc['dashboard'] = newDAssj
            posistionObj.save()
        res = {}
        currDashboard = copy(posistionObj.desc['dashboard'])
        i = 1
        while i <= 4:
            if currDashboard['msBox%s' % (str(i),)] != '':
                res['box%s' % (str(i),)] = {}
                dataObjs = MSData.objects.filter(template_id=ObjectId(currDashboard['msBox%s' % (str(i),)])).order_by(
                    '-value')
                thisTemplate = MSTemplate.objects.get(id=ObjectId(currDashboard['msBox%s' % (str(i),)]))
                res['box%s' % (str(i),)]['name'] = thisTemplate.name
                res['box%s' % (str(i),)]['unit'] = thisTemplate.dataType
                res['box%s' % (str(i),)]['icon'] = thisTemplate.icon
                res['box%s' % (str(i),)]['max'] = dataObjs[0].value if len(dataObjs) != 0 else '---'
                res['box%s' % (str(i),)]['min'] = dataObjs[dataObjs.count() - 1].value if len(dataObjs) != 0 else '---'
                res['box%s' % (str(i),)]['latest'] = dataObjs.order_by('-entryDate')[0].value if len(
                    dataObjs) != 0 else '---'
                res['box%s' % (str(i),)]['average'] = math.ceil(dataObjs.average('value')) if len(
                    dataObjs) != 0 else '---'
            i += 1
        return Response(res)

    @list_route(methods=['get'])
    def MSTemplateList(self, request, *args, **kwargs):
        posistionObj = PositionsDocument.objects.get(userID=request.user.id,
                                                     companyID=request.user.current_company.id)
        res = []
        msTemplates = MSTemplate.objects.filter(companyId=request.user.current_company.id,
                                                publishedUsers__contains=str(posistionObj.id)).only('id').only(
            'name').only('position_id')
        posNameList = list(
            PositionsDocument.objects.filter(id__in=msTemplates.distinct('position_id')).only('id', 'profileName',
                                                                                              'chartName'))
        for itm in msTemplates:
            postionTitle = ""
            for posN in posNameList:
                if posN.id == itm.position_id:
                    if posN.profileName :
                        if posN.chartName :
                            postionTitle = posN.profileName + " " + posN.chartName

            res.append({'name': itm.name, 'id': str(itm.id), 'positionName': postionTitle})
        return Response(res)

    @list_route(methods=['post'])
    def ChangeMSBox(self, request, *args, **kwargs):
        data = request.data
        posistionObj = PositionsDocument.objects.get(userID=request.user.id,
                                                     companyID=request.user.current_company.id)
        newDAsh = copy(posistionObj.desc['dashboard'])
        if len(newDAsh) < 4:
            newDAsh = {'msBox1': '',
                       'msBox2': '',
                       'msBox3': '',
                       'msBox4': ''}

        newDAsh['msBox%s' % (str(data['boxPos']))] = data['new']
        if not 'dashboard' in posistionObj.desc:
            posistionObj.desc['dashboard'] = {}
        posistionObj.desc['dashboard'] = newDAsh
        posistionObj.save()
        return Response({})

    def template_view_statistics_base(self, request, *args, **kwargs):
        return render_to_response('Statistics/BaseStatistics.html', {},
                                  context_instance=RequestContext(request))

    def template_view_statistics_new(self, request, *args, **kwargs):
        return render_to_response('Statistics/NewStatisticTemplate.html', {},
                                  context_instance=RequestContext(request))

    def template_view_statistics_edit(self, request, *args, **kwargs):
        return render_to_response('Statistics/EditStatisticTemplate.html', {},
                                  context_instance=RequestContext(request))

    def template_view_statistics_publish(self, request, *args, **kwargs):
        return render_to_response('Statistics/PublishTemplate.html', {},
                                  context_instance=RequestContext(request))

    def template_view_statistics_share(self, request, *args, **kwargs):
        return render_to_response('Statistics/ShareUsers.html', {},
                                  context_instance=RequestContext(request))
