import time
from datetime import datetime

import pytz
from django.contrib.auth import authenticate, login as _login, logout
from django.shortcuts import render_to_response
# Create your views here.
from django.template import RequestContext
from django.views.generic.base import TemplateView
from rest_framework import views
from rest_framework.response import Response
from translate import Translator

from amsp import settings
from amspApp.Administrator.Languages.serializers.LanguagesSerializer import LanguagesSerializer
from amspApp.BASE.classes.indexCSSLoader import IndexCSSLoaders
from amspApp.BASE.classes.indexJsLoader import IndexLoaders
from amspApp.CompaniesManagment.CompanyProfile.models import CompanyProfile
from amspApp.CompaniesManagment.CompanyProfile.serializers.CompanyProfileSerializers import CompanyProfileSerializer
from amspApp.CompaniesManagment.Positions.models import Position
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.models import Company
from amspApp.Infrustructures.Classes.DateConvertors import mil_to_sh
from amspApp._Share.odoo_connect import odoo_instance
from amspApp.amspUser.views.UserView import LoginViewset
from amspApp.dashboard.views.HomeView import Home
from amspApp.models import Languages
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


def base(request):
    if not request.user.is_active == False and 'tempUA' in request.COOKIES:
        logout(request)
    if request.user.is_active == False and 'tempUA' in request.COOKIES:
        user = authenticate(username=request.COOKIES["tempUA"], password=request.COOKIES["tempUA"])
        if user.is_active:
            user.current_company = Company.objects.get(id=700)
            user.save()
            _login(request, user)

    # if request.user.is_active == False :
    #     return LoginViewset().getTemplate(request)

    return render_to_response('others/base.html', {}, context_instance=RequestContext(request))


# def loginPartial(request):
# return render_to_response('others/base.html', {}, context_instance=RequestContext(request))


def home(request):
    # getting current company instance
    # if not request.user.is_active:
    #     return redirect("/login")
    if not request.user.is_active:
        return render_to_response('authentication/logins/returnToLogin.html', {},
                                  context_instance=RequestContext(request))

    companyInstance = CompanyProfile.objects.get(companyID=request.user.current_company_id)
    companySerial = CompanyProfileSerializer(instance=companyInstance).data
    msg = companySerial["extra"]["biefIntroduction"]

    return render_to_response('others/home.html', {'msg': msg}, context_instance=RequestContext(request))


def erp_control_project(request):
    return Response({})


def freeRahsoon(request):
    return render_to_response('others/freeRahsoon.html', {}, context_instance=RequestContext(request))


from rest_framework.decorators import api_view


@api_view(['GET', 'POST', ])
def _logout(request):
    logout(request)
    return Response({})


# def signup(request):
#     return render_to_response('authentication/signup.html', {}, context_instance=RequestContext(request))


# def forget(request):
#     return render_to_response('authentication/forget.html', {}, context_instance=RequestContext(request))


def dashboard(request):
    return render_to_response('others/dashboard.html', {}, context_instance=RequestContext(request))


def _dash(request):
    profile = Home().handleCurrentUser(request)
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
        'rahsoonEmail': request.user.username + "@" + request.subdomain.subdomainName + ".rahsoon.com",
    }

    return render_to_response('Dashboard/base.html', data, context_instance=RequestContext(request))


def upload(request):
    return render_to_response('generic-templates/upload.html', {}, context_instance=RequestContext(request))


def selectPosition(request):
    return render_to_response('generic-templates/selectPositions.html', {}, context_instance=RequestContext(request))


def showBpmnStepData(request):
    return render_to_response('generic-templates/showBpmnStepData.html', {}, context_instance=RequestContext(request))


from rest_framework.decorators import api_view


@api_view()
def getCurrent(request):
    from rest_framework.response import Response

    return Response({'company': request.user.current_company.id,
                     'positionMysql': Position.objects.get(user=request.user,
                                                           company=request.user.current_company).id if request.GET[
                         'position'] else '',
                     'positionDocument': str(PositionsDocument.objects.get(companyID=request.user.current_company.id,
                                                                           userID=request.user.id).id) if request.GET[
                         'position'] else ''})


def blank(request):
    return render_to_response('others/blank.html', {},
                              context_instance=RequestContext(request))


def oldAmsp(request):
    return render_to_response('oldAmsp/base.html', {},
                              context_instance=RequestContext(request))


# def newbpmn(request):
#     return render_to_response('others/../templates/companyManagement/newbpmn.html', {},
#                               context_instance=RequestContext(request))


# def build_form(request):
#     return render_to_response('others/../templates/companyManagement/SetupBpmnElements.html', {},
#                               context_instance=RequestContext(request))


def companydash(request):
    return render_to_response('companyManagement/CompanyManagement.html', {},
                              context_instance=RequestContext(request))


def companydashboard(request):
    return render_to_response('companyManagement/companyDashboard.html', {},
                              context_instance=RequestContext(request))


def chartcompany(request):
    return render_to_response('companyManagement/CompanyChart.html', {},
                              context_instance=RequestContext(request))


def control_project(request):
    odoo_ins = odoo_instance()
    odoo_ins.check_user_if_not_create(request.user.username)
    odooUrl = settings.ODOO_HTTP_REFERER

    return render_to_response(
        'ControlProject/base.html',

        {"odooURL": odooUrl,
         'username': request.user.username + "@****.com",
         # "session":session_id
         },
        context_instance=RequestContext(request))


def memberscompany(request):
    return render_to_response('companyManagement/CompanyMembers.html', {},
                              context_instance=RequestContext(request))


def profilecompany(request):
    return render_to_response('companyManagement/CompanyProfile.html', {},
                              context_instance=RequestContext(request))


def productscompany(request):
    return render_to_response('companyManagement/CompanyProducts.html', {},
                              context_instance=RequestContext(request))


class IndexView(TemplateView):

    def get(self, request, *args, **kwargs):
        context = {}
        if request.user.is_active == False:
            return LoginViewset().getTemplate(self.request)
        context = {}
        companyInstance = CompanyProfile.objects.get(companyID=request.user.current_company_id)
        companySerial = CompanyProfileSerializer(instance=companyInstance).data

        staticJs = IndexLoaders().getJsLoads(version="0.08")
        staticCSS = IndexCSSLoaders().getCSSLoads(version="0.08")

        context['companyLogo'] = ""
        context['staticJs'] = staticJs
        context['staticCSS'] = staticCSS
        context['userID'] = request.user.id
        context['companyID'] = companyInstance.companyID
        context['companyName'] = companyInstance.extra.get('name','')
        # context['domainname'] = CURRENT_DOMAIN_WEB
        # cc = self.GenerateBasicAuth(request)
        if "extra" in companySerial:
            if "logo" in companySerial["extra"]:
                context['companyLogo'] = companySerial["extra"]["logo"]


        basicAuth = request.session.get('basicAuth')
        context['basicAuth'] = basicAuth

        return render_to_response('others/index.html', context, context_instance=RequestContext(request))

        # def get_context_data(self, **kwargs):
        #     if self.request.user.is_active == False:
        #         return LoginViewset().getTemplate(self.request)
        #
        #
        #         # return super(IndexView, self).get_context_data(**kwargs)
        #
        #     context = super(IndexView, self).get_context_data(**kwargs)
        #     companyInstance = CompanyProfile.objects.get(companyID=self.request.user.current_company_id)
        #     companySerial = CompanyProfileSerializer(instance=companyInstance).data
        #     context['companyLogo'] = ""
        #     if "extra" in companySerial:
        #         if "logo" in companySerial["extra"]:
        #             context['companyLogo'] = companySerial["extra"]["logo"]
        #     return context
        #
        # @method_decorator(ensure_csrf_cookie)
        # def dispatch(self, *args, **kwargs):
        #     return super(IndexView, self).dispatch(*args, **kwargs)


class TranslateUknown(views.APIView):
    def post(self, request):

        dictKeys = request.DATA['items'].split("____")
        # fileDict = ""
        # with open(settings.APP_PATH + "static/languages/fa.json", 'r') as myfile:
        # data = myfile.read().replace('\n', '')
        dbLangs = list(Languages.objects.all().values())

        finalToTranslate = []
        for d in dictKeys:
            found = False
            for db in dbLangs:
                try:
                    if d.replace(' ', '').lower().strip() == db['en'].replace(' ', '').lower().strip():
                        found = True
                except:
                    pass
            if not found:
                finalToTranslate.append(d)

        supp = "  -----.  "
        listToTranslate = []
        translator = Translator(to_lang="fa")
        translation = translator.translate(supp.join(finalToTranslate))
        if supp == "":
            supp = "  -----.  "
        translated = translation.split('---')

        finalList = []
        i = 0
        for t in translated:
            if t != "":
                try:
                    finalList.append({
                        finalToTranslate[i]: t.replace(".", "").replace("-", " ")
                    })
                except:
                    i = i
                    pass
            i += 1

        for f in finalList:
            data = {
                "en": list(f.items())[0][0],
                "fa": list(f.items())[0][1],
            }

            newdt = LanguagesSerializer(data=data)
            newdt.is_valid(raise_exception=True)
            newdt.save()

        return Response({})


class Language(views.APIView):
    def get(self, request):
        langs = Languages.objects.all()
        result = {}
        for l in langs:
            if l.en:
                result[l.en.strip()] = l.fa.strip()

        return Response(result)
