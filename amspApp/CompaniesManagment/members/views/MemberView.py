from asq.initiators import query
from django.contrib.auth.models import User
from django.core.cache import cache
from django.shortcuts import render_to_response
from django.template import RequestContext
from mongoengine import Q
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_mongoengine import generics
from rest_framework_mongoengine import viewsets as __viewsets

from amspApp.BPMSystem.models import BigArchive
from amspApp.CompaniesManagment.Charts.models import Chart, ChartZones, ZoneItems
from amspApp.CompaniesManagment.Charts.serializers.ChartSerializers import ChartSerializer
from amspApp.CompaniesManagment.Charts.serializers.ZoneSerializers import ZoneSerializer, ZoneItemsSerializer
from amspApp.CompaniesManagment.Positions.models import Position, PositionsDocument, PositionSentHistory
from amspApp.CompaniesManagment.Positions.serializers.PositionSerializer import PositionDocumentSerializer, \
    PositionDocumentLessDataSerializer
from amspApp.CompaniesManagment.members.serializers.MemberSerializer import MembersSerializer, MembersDocumentSerializer
from amspApp.CompaniesManagment.models import Company
from amspApp.CompaniesManagment.permissions.CompanyPermissions import CanCruid
from amspApp.CompaniesManagment.permissions.PermissionChecker import get_permissions
from amspApp.Infrustructures.Classes.PublicFilters import QuerySetFilter
from amspApp.Letter.models import InboxGroup, Inbox
from amspApp.Letter.serializers.InboxGroupSerializer import InboxGroupSerializer
from amspApp.MyProfile.models import Profile
from amspApp.UserSettings.Views.AccessToSecratariatView import AccessToSecratariatViewSet
from amspApp._Share.ListPagination import ListPagination, DetailsPagination
from amspApp.amspUser.models import MyUser
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset

__author__ = 'mohammad'


class MemberViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    # queryset = CompanyProductions.objects.all()
    serializer_class = MembersSerializer
    pagination_class = ListPagination
    # filter_backends = (filters.DjangoFilterBackend,)
    permission_name = "Can_remove_members"
    permission_classes = (CanCruid,)

    def get_position_from_personnel_code(self, personnel_code):
        ins = MyUser.objects.filter(personnel_code=personnel_code).first()
        if ins is None:
            Response({'msg': 'invalid'})

        posins = PositionsDocument.objects.filter(userID=ins.id, companyID__ne=None).order_by("-id").first()
        if posins is None:
            Response({'msg': 'invalid'})
        posser = PositionDocumentLessDataSerializer(instance=posins).data
        return posser

    @list_route(methods=['POST'])
    def update_emzaha(self, request, *args, **kwargs):
        posIns = PositionsDocument.objects.get(id=request.data['id'])
        desc = posIns.desc
        desc['taeed'] = request.data['desc']['taeed']
        posInsSerial = PositionDocumentSerializer(instance=posIns, data={'desc': desc}, partial=True)
        posInsSerial.is_valid(raise_exception=True)
        posInsSerial.save()
        return Response({"msg": "saved"})

    @list_route(methods=['GET'])
    def get_position_from_personnel_code_req(self, request, *args, **kwargs):
        resp = self.get_position_from_personnel_code(request.query_params['q'])
        if resp is None:
            Response({'msg': 'invalid'})
        return Response(resp)

    def get_permissions(self):
        return get_permissions(self, MemberViewSet)

    def get_queryset(self):
        companyInstance = Company.objects.get(
            id=self.kwargs["companyID_id"],
        )
        self.queryset = Position.objects.filter(company=companyInstance).order_by("-id")

        return super(MemberViewSet, self).get_queryset()

    @list_route(methods=["get"])
    def getList(self, request, *args, **kwargs):
        if (kwargs['companyID_id'] == '0'):
            posInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            kwargs['companyID_id'] = posInstance.companyID

        positions = list(Position.objects.filter(company_id=int(kwargs['companyID_id'])))
        positionsDocs = PositionsDocument.objects.filter(positionID__in=[x.id for x in positions])
        # if "q" in request.query_params:
        #     q = request.query_params["q"]
        #     if  q== "undefined":
        #         q = ""
        #
        # positionsDocs = positionsDocs.filter( Q(chartName__contains = q)| Q(profileName__contains = q))
        positionsDocs = PositionDocumentSerializer(instance=positionsDocs, many=True).data

        for p in positionsDocs:
            usr = MyUser.objects.filter(id=p['userID']).first()
            if usr:
                p['cellphone'] = usr.cellphone
                p['personnel_code'] = usr.personnel_code
            p["desc"] = None
            p["chartName"] = query(positions).where(lambda x: x.id == p["positionID"]).first().chart.title
            # p["inboxCount"] = Inbox.objects.filter(currentPositionID=p["positionID"]).count()
            # p["processCount"] = BigArchive.objects.filter(thisPerformerId=
            #                                               PositionsDocument.objects.filter(
            #                                                   positionID=p["positionID"]).first().id
            #                                               if PositionsDocument.objects.filter(
            #                                                   positionID=p["positionID"]).first() != None else None
            #                                               ).count()

            p["processCount"] = 0
            p["inboxCount"] = 0

            if p["userID"]:
                userInstance = MyUser.objects.get(id=p["userID"])
                p["username"] = userInstance.username
                p["email"] = userInstance.email
                p["date_joined"] = userInstance.date_joined
                p["current_company"] = userInstance.current_company.name

        return Response(positionsDocs)

    @list_route(methods=["get"])
    def getListJustHasPos(self, request, *args, **kwargs):
        if (kwargs['companyID_id'] == '0'):
            posInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            kwargs['companyID_id'] = posInstance.companyID

        positions = list(Position.objects.filter(company_id=int(kwargs['companyID_id']), user__isnull=False))
        positionsDocs = PositionsDocument.objects.filter(positionID__in=[x.id for x in positions])
        # if "q" in request.query_params:
        #     q = request.query_params["q"]
        #     if  q== "undefined":
        #         q = ""
        #
        # positionsDocs = positionsDocs.filter( Q(chartName__contains = q)| Q(profileName__contains = q))
        positionsDocs = PositionDocumentSerializer(instance=positionsDocs, many=True).data

        for p in positionsDocs:
            usr = MyUser.objects.filter(id=p['userID']).first()
            if usr:
                p['cellphone'] = usr.cellphone
                p['personnel_code'] = usr.personnel_code
            p["desc"]['automation'] = None
            p["desc"]['dashboard'] = None
            p["chartName"] = query(positions).where(lambda x: x.id == p["positionID"]).first().chart.title
            # p["inboxCount"] = Inbox.objects.filter(currentPositionID=p["positionID"]).count()
            # p["processCount"] = BigArchive.objects.filter(thisPerformerId=
            #                                               PositionsDocument.objects.filter(
            #                                                   positionID=p["positionID"]).first().id
            #                                               if PositionsDocument.objects.filter(
            #                                                   positionID=p["positionID"]).first() != None else None
            #                                               ).count()

            p["processCount"] = 0
            p["inboxCount"] = 0

            if p["userID"]:
                userInstance = MyUser.objects.filter(id=p["userID"]).first()
                if userInstance:
                    p["username"] = userInstance.username
                    p["email"] = userInstance.email
                    p["date_joined"] = userInstance.date_joined
                    p["current_company"] = userInstance.current_company.name

        return Response(positionsDocs)

    @list_route(methods=["get"])
    def getListJustHasPosWithSearch(self, request, *args, **kwargs):
        if (kwargs['companyID_id'] == '0'):
            posInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
            kwargs['companyID_id'] = posInstance.companyID

        positions = list(Position.objects.filter(company_id=int(kwargs['companyID_id']), user__isnull=False))
        positionsDocs = PositionsDocument.objects.filter(positionID__in=[x.id for x in positions])
        q = ""
        if "q" in request.query_params:
            q = request.query_params["q"]
            if q == "undefined":
                q = ""

        positionsDocs = positionsDocs.filter(Q(chartName__contains=q) | Q(profileName__contains=q))
        positionsDocs = PositionDocumentSerializer(instance=positionsDocs, many=True).data

        for p in positionsDocs:
            usr = MyUser.objects.filter(id=p['userID']).first()
            if usr:
                p['cellphone'] = usr.cellphone
                p['personnel_code'] = usr.personnel_code
            p["desc"]['automation'] = None
            p["desc"]['dashboard'] = None
            p["chartName"] = query(positions).where(lambda x: x.id == p["positionID"]).first().chart.title
            # p["inboxCount"] = Inbox.objects.filter(currentPositionID=p["positionID"]).count()
            # p["processCount"] = BigArchive.objects.filter(thisPerformerId=
            #                                               PositionsDocument.objects.filter(
            #                                                   positionID=p["positionID"]).first().id
            #                                               if PositionsDocument.objects.filter(
            #                                                   positionID=p["positionID"]).first() != None else None
            #                                               ).count()

            p["processCount"] = 0
            p["inboxCount"] = 0

            if p["userID"]:
                userInstance = MyUser.objects.get(id=p["userID"])
                p["username"] = userInstance.username
                p["email"] = userInstance.email
                p["date_joined"] = userInstance.date_joined
                p["current_company"] = userInstance.current_company.name

        return Response(positionsDocs)

    def list(self, request, *args, **kwargs):
        result = super(MemberViewSet, self).list(request, *args, **kwargs)
        for r in result.data['results']:
            r["inboxCount"] = Inbox.objects.filter(currentPositionID=r["id"]).count()
            r["processCount"] = BigArchive.objects.filter(thisPerformerId=
                                                          PositionsDocument.objects.filter(
                                                              positionID=r["id"]).first().id
                                                          if PositionsDocument.objects.filter(
                                                              positionID=r["id"]).first() != None else None
                                                          ).count()
            posIns = Position.objects.get(id=r["id"])
            if posIns.user:
                userInstance = MyUser.objects.get(id=posIns.user_id)
                r["username"] = userInstance.username
                r["email"] = userInstance.email
                r["date_joined"] = userInstance.date_joined
                r["current_company"] = userInstance.current_company.name

        return result

    @list_route(methods=['get'])
    def GetChartPositionList(self, request, *args, **kwargs):
        # pos = Position.objects.get(
        #     user=self.request.user,
        #     # company=self.request.user.current_company
        # )
        ChartInstance = Chart.objects.get(
            id=request.query_params["id"],
            # owner = self.request.user.current_company
        )
        posList = PositionsDocument.objects.filter(chartID=ChartInstance.id)
        serial = []
        for p in posList:
            ser = MembersDocumentSerializer(instance=p).data
            ser.pop('desc')
            serial.append(ser)

        serial = query(serial).where(lambda x: x["userID"] != None).to_list()

        # serial = MembersSerializer(instance=posList, many=True).data
        return Response(serial)

    def template_page(self, request, *args, **kwargs):
        return render_to_response("companyManagement/Members.html", {}, context_instance=RequestContext(self.request))


class MemberViewSetMongo(generics.ListCreateAPIView):
    lookup_field = 'id'
    model = PositionsDocument
    serializer_class = MembersDocumentSerializer
    pagination_class = ListPagination

    # filter_backends = (filters.DjangoFilterBackend,)
    # my_filter_fields = ("chartName","profileName","companyName", )

    def get_queryset(self):
        if self.request.query_params["cid"] == "drede23fa":
            companyInstance = Company.objects.get(
                id=self.request.user.current_company_id,
                # owner_user = self.request.user.id
            )
        else:
            companyInstance = Company.objects.get(
                id=int(self.request.query_params["cid"])
                # owner_user=self.request.user.id
            )

        self.queryset = QuerySetFilter().filter(
            querySet=PositionsDocument.objects.filter(companyID=companyInstance.id),
            kwargs=self.request.query_params
        )
        return super(MemberViewSetMongo, self).get_queryset()


class MemberViewSetMongoWithCustomePaging(__viewsets.ReadOnlyModelViewSet):
    lookup_field = 'id'
    serializer_class = MembersDocumentSerializer
    pagination_class = DetailsPagination

    my_filter_fields = ('avatar', 'chartID')  # specify the fields on which you want to filter

    def get_kwargs_for_filtering(self):
        filtering_kwargs = {}
        for field in self.my_filter_fields:  # iterate over the filter fields
            field_value = self.request.query_params.get(field)  # get the value of a field from request query parameter
            if field_value:
                filtering_kwargs[field] = field_value
        return filtering_kwargs

    @detail_route(methods=["get"])
    def getByChartID(self, request, *args, **kwargs):
        chartInstance = Chart.objects.get(id=int(kwargs["id"]))

        # this is for filtering thoes which are in Position Docs and thoes not
        # only positions are allowed to observe then has an mysql position
        querySet = Position.objects.filter(chart_id=int(kwargs["id"]), company_id=chartInstance.owner_id)
        querySet = PositionsDocument.objects.filter(positionID__in=[x.id for x in querySet]).order_by("-id")

        usersInstance = list(MyUser.objects.filter(id__in=[x['userID'] for x in querySet]))
        users = [{"name": x.username, "email": x.email, "id": x.id} for x in usersInstance]
        result = [{
            "name": x.profileName,
            "chartName": x.chartName,
            "id": str(x.id),
            "positionID": x.positionID,
            "username": query(users).where(lambda z: z["id"] == x.userID).to_list()[0][
                "name"] if x.userID != None else None,
            "email": query(users).where(lambda z: z["id"] == x.userID).to_list()[0][
                "email"] if x.userID != None else None,

            "inboxCount": Inbox.objects.filter(currentPositionID=x.positionID).count(),
            "processCount": BigArchive.objects.filter(thisPerformerId=
                                                      PositionsDocument.objects.filter(
                                                          positionID=x.positionID).first().id
                                                      if PositionsDocument.objects.filter(
                                                          positionID=x.positionID).first() != None else None
                                                      ).count(),
            "companyID": x.companyID,
            "userID": x.userID
        } for x in querySet]

        # result = json.dumps(result)
        return Response(result)

    def get_queryset(self):
        pos = Position.objects.get(
            user=self.request.user,
            company=self.request.user.current_company)
        companyInstance = self.request.user.current_company
        if "companyID" in self.request.query_params:
            if (self.request.query_params["companyID"] == 'undefined' or (
                    self.request.query_params["companyID"] == 'null')):
                companyInstance = self.request.user.current_company
            else:
                companyInstance = Company.objects.get(
                    id=self.request.query_params["companyID"]
                )
        else:
            companyInstance = self.request.user.current_company

        self.queryset = QuerySetFilter().filter(
            querySet=PositionsDocument.objects.filter(
                companyID=companyInstance.id),
            kwargs=self.request.query_params)

        self.queryset = self.queryset.filter(userID__ne=None)
        return self.queryset


class ListAllMemberViews(APIView):

    # @list_route(methods=["GET"])
    # def refreshCache(self, request, ):
    #     currentPositionInstace = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
    #     list = self.generate_catch(self.request.user, self.request.user.current_company, FarceGenerate=True)
    #     return Response({"ok": "ok"})

    def generate_catch(self, currentUserInstance, currentCompanyInstance, FarceGenerate=False):

        # getting permitted tabs to load
        positionInstance = Position.objects.get(
            user=currentUserInstance,
            company=currentCompanyInstance)
        if cache.get("searchComplex" + str(positionInstance.id)) and FarceGenerate == False:
            return cache.get("searchComplex" + str(positionInstance.id))

        permittedTabs = AccessToSecratariatViewSet().getSecPer(positionInstance.id)

        # getting all members if allowded
        send_Just_with_Chart_limitation = AccessToSecratariatViewSet().send_Just_with_Chart_limitation(
            positionInstance.id)

        # getting all members if allowded
        not_Allowed_sent_to_All = AccessToSecratariatViewSet().not_Allowed_sent_to_All(positionInstance.id)

        members = []

        if not send_Just_with_Chart_limitation:
            members = PositionsDocument.objects.filter(companyID=currentCompanyInstance.id, userID__nin=[None])
        else:
            currentChart = Chart.objects.get(id=positionInstance.chart_id)
            topChartID = currentChart.top
            lowerChartID = [x.id for x in list(Chart.objects.filter(top=currentChart))]
            final = [currentChart.id, topChartID.id] + lowerChartID
            members = PositionsDocument.objects.filter(chartID__in=final, userID__nin=[None])

        # getting all groups with members
        # group members stored inside group object
        groups = list(InboxGroup.objects.filter(positionID=positionInstance.id))

        # getting all zones with members
        zones = list(ChartZones.objects.filter(company=currentCompanyInstance))
        zoneItems = list(ZoneItems.objects.filter(zone__in=zones))

        # getting all charts
        charts = list(Chart.objects.filter(owner=currentCompanyInstance))

        finalList = {}

        memSerial = MembersDocumentSerializer()

        if any("Members" in x for x in permittedTabs):
            finalList["Members"] = []
            for m in members:
                obj = MembersDocumentSerializer(instance=m).data
                # this line skip suspeneded users
                if "profileName" in obj:
                    if obj["profileName"]:
                        obj["name"] = obj["profileName"] + " " + obj["chartName"]
                        obj.pop("desc", None)
                        finalList["Members"].append(obj)

        if any("Positions" in x for x in permittedTabs):
            finalList["Positions"] = []
            for c in charts:
                obj = ChartSerializer(instance=c).data
                finalList["Positions"].append(obj)
            for c in finalList["Positions"]:
                c["members"] = []
                for m in finalList["Members"]:
                    if c["id"] == m["chartID"]:
                        if "userID" in m:
                            if m["userID"]:
                                c["members"].append(m)
            # here i want to remove positions who has no profile
            if len(finalList["Positions"]) > 0:
                finalList["Positions"] = query(finalList["Positions"]).where(lambda x: len(x["members"]) > 0).to_list()

        if any("Groups" in x for x in permittedTabs):
            finalList["Groups"] = []
            for c in groups:
                obj = InboxGroupSerializer(instance=c).data
                obj["mem"] = obj["members"]
                obj["members"] = []
                for o in obj["mem"]:
                    for m in finalList["Members"]:
                        if o["positionID"] == m["positionID"] and o["userID"] == m["userID"] and o["chartID"] == m[
                            "chartID"]:
                            obj["members"].append(o)
                obj.pop("mem", None)
                finalList["Groups"].append(obj)

        if len(finalList["Groups"]) > 0:
            finalList["Groups"] = query(finalList["Groups"]).where(lambda x: len(x["members"]) > 0).to_list()

        if any("Zones" in x for x in permittedTabs):
            finalList["Zones"] = []
            child = list(ZoneItems.objects.filter(zone__in=zones))
            for c in zones:
                obj = ZoneSerializer(instance=c).data
                obj["members"] = []
                finalList["Zones"].append(obj)
                for cc in child:
                    if cc.zone_id == obj["id"]:
                        objChild = ZoneItemsSerializer(instance=cc).data
                        for ccc in finalList["Positions"]:
                            if ccc["id"] == objChild["chart"]:
                                objChild["chartTitle"] = ccc["title"]
                                objChild["chartMember"] = ccc["members"]
                        obj["members"].append(objChild)
            if len(finalList["Zones"]) > 0:
                finalList["Zones"] = query(finalList["Zones"]).where(lambda x: len(x["members"]) > 0).to_list()
        # sorting by latest sent

        cache.set("searchComplex" + str(positionInstance.id), finalList, 10)
        return finalList

    def post(self, request, format=None):
        # filter = [{"d":int(x.split("___")[0].replace("_",'')),"v":bool(x.split("___")[1])} for x in request.query_params['f'].split("6589")]
        currentPositionInstace = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        list = self.generate_catch(self.request.user, self.request.user.current_company)
        listR = {}

        strq = request.data["q"]
        filter = request.data["f"]

        # each list just contains less then 40 items
        sendToWho = []
        if "Groups" in list:
            # lcom = {'v': True, 'd': 1}
            cc = {'d': 1, 'v': True}
            if cc in filter:
                listR["Groups"] = query(list["Groups"]).where(lambda x: strq in x["title"]).take(40).to_list()
            sendToWho.append({'d': 1, 'v': cc in filter})

        if "Members" in list:
            # lcom = {'v': True, 'd': 2}
            cc = {'d': 2, 'v': True}
            if cc in filter:
                """
                getting sort by latest receivers
                """
                top4HistorySent = PositionSentHistory.objects.filter(
                    positionID=currentPositionInstace.positionID).order_by("-id").limit(10)
                positionsID = [[z["positionID"] for z in x.afterProcess] for x in top4HistorySent]
                sorted = []
                for p in positionsID:
                    sorted.extend(p)
                sortedHeaders = query(sorted).distinct().reverse().to_list()

                for sH in sortedHeaders:
                    for lm in list["Members"]:
                        if lm["positionID"] == sH:
                            itemm = lm
                            list["Members"].remove(itemm)
                            list["Members"].insert(0, itemm)
                            break

                listR["Members"] = query(list["Members"]).where(lambda x: strq in x["name"]).take(60).to_list()
            sendToWho.append({'d': 2, 'v': cc in filter})

        if "Positions" in list:
            # lcom = {'v': True, 'd': 3}
            cc = {'d': 3, 'v': True}
            if cc in filter:
                listR["Positions"] = query(list["Positions"]).where(lambda x: strq in x["title"]).take(40).to_list()
            sendToWho.append({'d': 3, 'v': cc in filter})

        if "Zones" in list:
            # lcom = {'v': True, 'd': 4}
            cc = {'d': 4, 'v': True}
            if cc in filter:
                listR["Zones"] = query(list["Zones"]).where(lambda x: strq in x["title"]).take(40).to_list()
            sendToWho.append({'d': 4, 'v': cc in filter})

        # preparing final list
        items = []
        if "Groups" in listR:
            for c in listR["Groups"]:
                items.append({
                    'name': c["title"],
                    'id': c["id"],
                    'type': 1,  # means group
                    'exp': len(c["members"]),
                    'avatar': ''
                })

        if "Members" in listR:
            for l in listR["Members"]:
                items.append({
                    'name': l["profileName"],
                    'id': l["positionID"],
                    'type': 2,  # means members
                    'exp': l["chartName"],
                    'avatar': l["avatar"].replace("50CC", "100"),
                    'details': l
                })

        if "Positions" in listR:
            for c in listR["Positions"]:
                items.append({
                    'name': c["title"],
                    'id': c["id"],
                    'type': 3,  # means positions
                    'exp': len(c["members"]),
                    'avatar': ''
                })
        if "Zones" in listR:
            for c in listR["Zones"]:
                items.append({
                    'name': c["title"],
                    'id': c["id"],
                    'type': 4,  # means zones
                    'exp': len(c["members"]),
                    'avatar': ''
                })

        return Response(
            {
                'filter': sendToWho,
                'data': items
            })

    def get(self, request):
        if request.query_params.get("fg"):
            list = self.generate_catch(self.request.user, self.request.user.current_company, FarceGenerate=True)
        else:
            list = self.generate_catch(self.request.user, self.request.user.current_company, FarceGenerate=False)
        items = []
        for l in list["Members"]:
            items.append({
                'name': l["profileName"],
                'id': l["positionID"],
                'type': 2,  # means members
                'exp': l["chartName"],
                'avatar': l["avatar"].replace("50CC", "100"),
                'details': l
            })
        return Response(items)


class SearchAllRegisteredUsers(APIView):
    def get(self, request):
        profileSearch = list(
            Profile.objects.filter(extra__Name__contains=request.query_params["q"]).limit(50).order_by("-id"))
        result = query(profileSearch).select(lambda x: {
            "name": x.extra["Name"] if "Name" in x.extra else "",
            "userID": x.userID,
            "avatar": x.extra["profileAvatar"]["url"] if "url" in x.extra[
                "profileAvatar"] else "/static/images/avatar_empty.jpg"
        }).where(lambda x: x["name"] != "").to_list()
        return Response(result)
