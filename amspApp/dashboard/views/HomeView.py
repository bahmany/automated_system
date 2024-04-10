from datetime import datetime
import timeit
from django.shortcuts import render_to_response
from mongoengine.base import BaseDict
import pytz
import time
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.views import APIView
from django.template import RequestContext
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage

from amspApp.CompaniesManagment.Positions.models import Position, PositionsDocument
from amspApp.CompaniesManagment.Positions.serializers.PositionSerializer import PositionDocumentSerializer
from amspApp.Infrustructures.Classes.DateConvertors import convertTimeZoneToUTC, sh_to_mil, mil_to_sh, \
    mil_to_sh_with_time, unix_time_millis
from amspApp.MyProfile.models import Profile
from amspApp.MyProfile.serializers.ProfileSerializer import ProfileSerializer
from amspApp.models import Sidebar, Helpbar
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset
from amspApp.serializers import HelpbarSerializer


class Home(viewsets.ViewSet):
    def handleCurrentUser(self, request):
        userProfile = Profile.objects.get(userID=request.user.id)
        return userProfile

    def getDashboardHelp(self, request):
        helping = Helpbar.objects.filter(url=request.QUERY_PARAMS['q'])
        res = {}
        if helping.count() != 0:
            helpSer = HelpbarSerializer(instance=helping[0]).data
            res = helpSer
        return Response(res)

    def addSomeToProfile(self, request):
        extra = request.user.get_user_profile().extra
        hasDoneBefore = False
        if "firstAfterRegProfile" in extra:
            hasDoneBefore = extra["firstAfterRegProfile"]
        return Response({"result": hasDoneBefore})

    def profileSeenFirstTime(self, request):
        profileDocInstance = request.user.get_user_profile()
        extra = profileDocInstance.extra
        extra["firstAfterRegProfile"] = True
        profileSerial = ProfileSerializer(instance=profileDocInstance, data={"extra": extra})
        profileSerial.is_valid(raise_exception=True)
        result = self.addSomeToProfile(request)
        profileSerial.save()
        return result

    def home(self, request):
        if not request.user.is_active:
            return render_to_response('authentication/logins/returnToLogin.html', {},
                                      context_instance=RequestContext(request))
        profile = self.handleCurrentUser(request)
        userAvatar = profile.extra['profileAvatar']['url'].split("=")[0] + "=thmum100_" + \
                     profile.extra['profileAvatar']['url'].split("=")[1] if profile.extra['profileAvatar'][
                                                                                'url'] != '/static/images/avatar_empty.jpg' else '/static/images/avatar_empty.jpg'

        data = {
            'currentUser': request.user.username,
            'userAvatar': userAvatar

        }
        return render_to_response('others/home.html', data, context_instance=RequestContext(request))

    def topnav(self, request):
        profile = self.handleCurrentUser(request)
        posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        userAvatar = profile.extra['profileAvatar']['url'] if profile.extra['profileAvatar'][
                                                                  'url'] != '/static/images/avatar_empty.jpg' else '/static/images/avatar_empty.jpg'
        # settingstime_zone = pytz.timezone(request.user.timezone)
        cc = datetime.now(pytz.timezone(request.user.timezone))
        data = {
            'currentUser': request.user.username,
            'userAvatar': userAvatar,
            'currenttime': int((time.mktime(cc.timetuple()) + cc.microsecond / 1000000.0) * 1000),
            'currentdatesh': mil_to_sh(datetime.now()),
            'currentdatemil': datetime.now().strftime("%Y/%m/%d"),
            'name': profile.extra["Name"],
            'title': profile.extra["Title"],
            'currentCOmpany': posiIns.companyName,
            'chart': posiIns.chartName,
            'lastLogin': request.user.last_login,
            'rahsoonEmail': request.user.username + "@" + request._request.subdomain.subdomainName + ".rahsoon.com",

        }
        return render_to_response('others/top-nav/topnav.html', data, context_instance=RequestContext(request))

    def getNameAndFamily(self, profileInstance):
        # extra = profileInstance.extra
        # extra["Name"]=profileInstance.extra['job']['Shenasnameh']['Name'] + " " +profileInstance.extra['job']['Shenasnameh']['Family']
        #
        # pf = ProfileSerializer(
        #     instance=profileInstance,
        #     data={"extra":extra},
        #     partial=True
        # )
        # pf.is_valid(raise_exception=True)
        # pf.update(instance=profileInstance, validated_data={"extra": {}})
        # pf.update(instance=profileInstance, validated_data={"extra":extra})
        return ""

    def sidebar(self, request):
        profile = self.handleCurrentUser(request)
        posiIns = GetPositionViewset().GetCurrentPositionDocumentInstance(request)

        userAvatar = profile.extra['profileAvatar']['url'] if profile.extra['profileAvatar'][
                                                                  'url'] != '/static/images/avatar_empty.jpg' else '/static/images/avatar_empty.jpg'
        userBackAvatar = profile.extra["profileHeaderBackground"]["url"].split("=")[0] + "=thmum100_" + \
                         profile.extra['profileHeaderBackground']['url'].split("=")[1] if \
            profile.extra['profileHeaderBackground'][
                'url'] != '/static/images/person_profile_default.jpg' else '/static/images/person_profile_default.jpg'

        data = {
            'currentUser': request.user.username,
            'profileName': posiIns.profileName,
            'chartName': posiIns.chartName,
            'profileTitle': profile.extra["Title"] if "Title" in profile.extra else "",
            'userAvatar': posiIns.avatar.replace("thmum50CC_", "thmum100_"),
            'userBackAvatar': userBackAvatar.replace("thmum50CC_", ""),
            'lastLogin': mil_to_sh_with_time(request.user.last_login).split("+")[0]
        }
        return render_to_response('others/sidebar/sidebar.html', data, context_instance=RequestContext(request))

    defaultDashboardBlocks = [
        {
            "type": 3,  # types = 3=connected to company profile message
            "sort": 1,
            "items": [

                {
                    "name": "آمارهای کلی",
                    "desc": "آخرین اطلاعیه ها و پیام های شرکت در این قسمت قابل مطالعه و مشاهده می باشد",
                    "data_id": None,
                }]
        },
        {
            "type": 2,  # types = 2=connected to statics
            "sort": 2,
            "items": [
                {
                    "name": "نا مشخص",
                    "static_id": None,
                    "sort": 1
                },
                {
                    "name": "نا مشخص",
                    "static_id": None,
                    "sort": 2
                },
                {
                    "name": "نا مشخص",
                    "static_id": None,
                    "sort": 3
                },
                {
                    "name": "نا مشخص",
                    "static_id": None,
                    "sort": 4
                }]
        },
        {
            "type": 1,  # types = 1=connected to company profile message
            "sort": 3,
            "items": [

                {
                    "name": "اعلانات",
                    "desc": "آخرین اطلاعیه ها و پیام های شرکت در این قسمت قابل مطالعه و مشاهده می باشد",
                    "static_id": None,
                }]
        },

    ]

    def template_dash_static_view(self, request):
        data = {}
        return render_to_response('myProfile/DashboardStatics.html', data, context_instance=RequestContext(request))

    def selectPosition(self, request):
        data = {}
        return render_to_response('Directives/selectPosition/selectPosition.html', data, context_instance=RequestContext(request))

    def selectChart(self, request):
        data = {}
        return render_to_response('Directives/selectChart/selectChart.html', data, context_instance=RequestContext(request))

    def getDashboard(self, request):
        positionInstance = GetPositionViewset().GetCurrentPositionDocumentInstance(request)
        # positionInstance = PositionsDocument.objects.filter(
        #     userID=request.user.id,
        #     companyID=request.user.current_company_id)
        # if positionInstance.count() == 0:
        #     raise Exception("Invalid positionInstance")

        positionSerial = PositionDocumentSerializer(instance=positionInstance).data
        # getting default dashboard blocks
        DashboardBlocks = None
        if "desc" in positionSerial:
            if "dashboard" in positionSerial["desc"]:
                DashboardBlocks = list(positionSerial["desc"]["dashboard"])

        if type(list()) != type(DashboardBlocks):
            DashboardBlocks = self.defaultDashboardBlocks
            positionSerial["desc"]["dashboard"] = DashboardBlocks
            ser = PositionDocumentSerializer(instance=positionInstance, data=positionSerial)
            ser.is_valid(raise_exception=True)
            ser.save()
        if DashboardBlocks == None:
            DashboardBlocks = self.defaultDashboardBlocks
            positionSerial["desc"]["dashboard"] = DashboardBlocks
            ser = PositionDocumentSerializer(instance=positionInstance, data=positionSerial)
            ser.is_valid(raise_exception=True)
            ser.save()

        if (len(DashboardBlocks) > 0):
            if not isinstance(DashboardBlocks[0], BaseDict):
                DashboardBlocks = self.defaultDashboardBlocks
                positionSerial["desc"]["dashboard"] = DashboardBlocks
                ser = PositionDocumentSerializer(instance=positionInstance, data=positionSerial)
                ser.is_valid(raise_exception=True)
                ser.save()

        if (len(DashboardBlocks)) == 0:
            DashboardBlocks = self.defaultDashboardBlocks
            positionSerial["desc"]["dashboard"] = DashboardBlocks
            ser = PositionDocumentSerializer(instance=positionInstance, data=positionSerial)
            ser.is_valid(raise_exception=True)
            ser.save()

        return Response(DashboardBlocks)

    def generateSideBar(self, request):
        sidebarItems = Sidebar.objects.all().order_by("order")
        menu = []
        for s in sidebarItems.filter(parent=0):
            result = {}
            result["name"] = s.name
            result["type"] = s.type
            result["state"] = s.state
            result["icon"] = s.icon
            if s.type == "toggle":
                result["pages"] = []
                for ss in sidebarItems.filter(parent=s.id):
                    result["pages"].append({
                        "name": ss.name,
                        "type": ss.type,
                        "state": ss.state,
                        "icon": ss.icon
                    })
            menu.append(result)
        return Response(menu)

    def setDashboard(self, request):
        positionsDocument = PositionsDocument.objects.get(
            userID=self.request.user.id,
            companyID=self.request.user.current_company_id
        )
        positionsDocumentSer = PositionDocumentSerializer(instance=positionsDocument).data
        positionsDocumentSer["desc"] = request.data
        posDocSer = PositionDocumentSerializer(instance=positionsDocument, data=positionsDocumentSer)
        posDocSer.is_valid(raise_exception=True)
        posDocSer.save()

        return Response(request.data)

    def setStaticDashboard(self, request):
        positionsDocument = PositionsDocument.objects.get(
            userID=self.request.user.id,
            companyID=self.request.user.current_company_id
        )
        positionsDocumentSer = PositionDocumentSerializer(instance=positionsDocument).data

        for dd in positionsDocumentSer['desc']['dashboard']:
            if dd["type"] == 2:
                for item in dd["items"]:
                    if "static_id" in item:
                        if item["static_id"] == request.data["id"]:
                            item["static_id"] = None

        posDocSer = PositionDocumentSerializer(instance=positionsDocument, data=positionsDocumentSer)
        posDocSer.is_valid(raise_exception=True)
        posDocSer.save()

        return Response(request.data)
