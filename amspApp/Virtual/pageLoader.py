from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import viewsets, permissions, views
from rest_framework.response import Response
from amspApp.Administrator.Customers.views.CustomerRegistrationView import CustomerRegistrationViewSet
from amspApp.CompaniesManagment.CompanyProfile.models import CompanyProfile
from amspApp.CompaniesManagment.CompanyProfile.serializers.CompanyProfileSerializers import CompanyProfileSerializer
# from amspApp.CompaniesManagment.models import Company, CompanyDetails
# from amspApp.Converts.Estekhdam import startMapping
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.MyProfile.models import Profile
from amspApp.MyProfile.serializers.ProfileSerializer import ProfileSerializer
from amspApp.Virtual.Registration.forms.loginForm import RegisterationHireForm, RegisterationLoginForm, ForgetForm, \
    ResetForm
from amspApp.amspUser.models import MyUser
from amspApp.amspUser.views.UserView import UserViewSet


class PageLoaderApi(viewsets.ModelViewSet):
    def index(self, request):

        customerInstance = CustomerRegistrationViewSet().GetCustomerInstanceFromBilling(request)
        user = MyUser.objects.get(username=customerInstance.username)
        company = CompanyProfile.objects.get(companyID=user.current_company_id)
        company = CompanyProfileSerializer(instance=company).data
        rank = UserViewSet().GetProfileLevel(request).data["rank"]
        if not request.user.is_active:
            return render_to_response(
                'Virtual/index.html',
                {'company': company,
                 'rank': rank,
                 'login': False,
                 },
                context_instance=RequestContext(request))

        user = MyUser.objects.filter(username=request.user.username)
        if user.count() == 0:
            return HttpResponseRedirect(
                request._request.META['wsgi.url_scheme'] + "://" + request._request.META["HTTP_HOST"] + "/reg/#/login")
        user = user[0]
        userProfile = Profile.objects.get(userID=user.id)
        userProfile = ProfileSerializer(instance=userProfile).data
        company = CompanyProfile.objects.get(companyID=user.current_company_id)
        company = CompanyProfileSerializer(instance=company).data
        res = {
            'profile': userProfile,
            'login': True,
            'rank': rank,
            'company': company,
        }

        return render_to_response(
            'Virtual/index.html',
            res,
            context_instance=RequestContext(request))

    def base(self, request):
        return render_to_response(
            'Virtual/base.html',
            {},
            context_instance=RequestContext(request))

    def login(self, request):
        if request.user.is_active:
            logout(request)
        return render_to_response(
            'Virtual/Registration/login.html',
            {'form': RegisterationLoginForm()},
            context_instance=RequestContext(request))

    def register(self, request):
        # getting default company LOGO from company Profile
        companyProfile = CompanyProfile.objects.get(companyID=request._request.owner_subdomain_user.current_company.id)
        # form = RegisterationHireForm()
        data = {
            "companyDetails": companyProfile.extra
        }
        return render_to_response(
            'Virtual/Registration/register.html',
            {'form': RegisterationHireForm(), "companyDetails": data["companyDetails"]},
            context_instance=RequestContext(request))

    def home(self, request):
        return render_to_response(
            'Virtual/home.html',
            {},
            context_instance=RequestContext(request))

    def getProfile(self, request):
        customerInstance = CustomerRegistrationViewSet().GetCustomerInstanceFromBilling(request)
        user = MyUser.objects.get(username=customerInstance.username)
        res = self.getCompanyPropByCompanyID(user.current_company_id)
        return res

    def getCompanyPropByCompanyID(self, request, CompanyID):
        company = CompanyProfile.objects.get(companyID=CompanyID)
        company = CompanyProfileSerializer(instance=company).data
        res = {
            "companyName": company["extra"]["name"],
            "introduction": company["extra"]["introduction"],
            "logo": company["extra"]["logo"],
            "background": company["extra"]["background"],
            "username": request.user.username,
            "lastLogin": request.user.last_login
        }
        return res

    def res(self, request):
        if not request.user.is_active:
            return {}

        customerInstance = CustomerRegistrationViewSet().GetCustomerInstanceFromBilling(request)
        user = MyUser.objects.get(username=customerInstance.username)

        company = CompanyProfile.objects.get(companyID=user.current_company_id)
        company = CompanyProfileSerializer(instance=company).data

        res = {
            "companyName": company["extra"]["name"],
            "introduction": company["extra"]["introduction"],
            "logo": company["extra"]["logo"],
            "background": company["extra"]["background"],
            "username": request.user.username,
            "lastLogin": request.user.last_login
        }
        return res

    def profile(self, request):
        # getting current company
        # company name
        # company default logo - background - introduction -
        # if not request.user.is_active:
        # request._request.META['wsgi.url_scheme']+"://"+request._request.META["HTTP_HOST"]+"/reg/#/login"
        # return HttpResponseRedirect(request._request.META['wsgi.url_scheme']+"://"+request._request.META["HTTP_HOST"]+"/reg/#/home/profile/introduction")

        # ----------

        return render_to_response(
            'Virtual/Profile/base.html',
            self.res(request),
            context_instance=RequestContext(request))

    def introduction(self, request):
        # getting current company
        # company name
        # company default logo - background - introduction -

        customerInstance = CustomerRegistrationViewSet().GetCustomerInstanceFromBilling(request)
        user = MyUser.objects.get(username=customerInstance.username)
        company = CompanyProfile.objects.get(companyID=user.current_company_id)
        company = CompanyProfileSerializer(instance=company).data
        if not request.user.is_active:
            return render_to_response(
                'Virtual/Profile/introduction.html',
                {'company': company,
                 'login': False,
                 },
                context_instance=RequestContext(request))
        user = MyUser.objects.filter(username=customerInstance.username)
        if user.count() == 0:
            return HttpResponseRedirect(
                request._request.META['wsgi.url_scheme'] + "://" + request._request.META["HTTP_HOST"] + "/reg/#/login")
        user = user[0]
        userProfile = Profile.objects.get(userID=user.id)
        userProfile = ProfileSerializer(instance=userProfile).data
        company = CompanyProfile.objects.get(companyID=user.current_company_id)
        company = CompanyProfileSerializer(instance=company).data
        res = {
            'profile': userProfile,
            'login': True,
            'company': company,
        }

        # ----------

        return render_to_response(
            'Virtual/Profile/introduction.html',
            res,
            context_instance=RequestContext(request))

    def hamkariDetails(self, request):
        return render_to_response(
            'Virtual/Profile/HamkariDetails/base.html',
            {},
            context_instance=RequestContext(request))

    def step1(self, request):
        return render_to_response(
            'Virtual/Profile/Estekhdam/Step1.html',
            {},
            context_instance=RequestContext(request))

    def step2(self, request):
        # startMapping()
        return render_to_response(
            'Virtual/Profile/Estekhdam/Step2.html',
            {},
            context_instance=RequestContext(request))

    def step3(self, request):
        return render_to_response(
            'Virtual/Profile/Estekhdam/Step3.html',
            {},
            context_instance=RequestContext(request))

    def step4(self, request):
        return render_to_response(
            'Virtual/Profile/Estekhdam/Step4.html',
            {},
            context_instance=RequestContext(request))

    def step5(self, request):
        return render_to_response(
            'Virtual/Profile/Estekhdam/Step5.html',
            {},
            context_instance=RequestContext(request))

    def step6(self, request):
        return render_to_response(
            'Virtual/Profile/Estekhdam/Step6.html',
            {},
            context_instance=RequestContext(request))

    def step7(self, request):
        return render_to_response(
            'Virtual/Profile/Estekhdam/Step7.html',
            {},
            context_instance=RequestContext(request))

    def step8(self, request):
        return render_to_response(
            'Virtual/Profile/Estekhdam/Step8.html',
            {},
            context_instance=RequestContext(request))

    def preview(self, request):
        return render_to_response(
            'Virtual/Profile/Estekhdam/Preview.html',
            {},
            context_instance=RequestContext(request))

    def selectJob(self, request):
        return render_to_response(
            'Virtual/Profile/Estekhdam/Jobs.html',
            {},
            context_instance=RequestContext(request))

    def resultJob(self, request):
        return render_to_response(
            'Virtual/Profile/Estekhdam/Results.html',
            {},
            context_instance=RequestContext(request))

    def forget(self, request):
        if not request.user.is_active:
            return render_to_response(
                'Virtual/Registration/forget.html',
                {"form": ForgetForm()},
                context_instance=RequestContext(request))
        else:
            raise Exception("logout first plz hackersss!!!")

    def reset(self, request):
        if not request.user.is_active:
            return render_to_response(
                'Virtual/Registration/reset.html',
                {"form": ResetForm()},
                context_instance=RequestContext(request))
        else:
            raise Exception("logout first plz hackersss!!!")

    def hamkariDetailsItemModal(self, request):
        isUserRegister = request.user.is_active
        return render_to_response(
            'Virtual/Profile/HamkariDetails/modalDetails.html',
            {"isUserRegister": isUserRegister},
            context_instance=RequestContext(request))

    # def goodsSupplay(self, request):
    #     return render_to_response(
    #         "Virtual/GoodsProviders/base.html",
    #         {
    #             "form": GoodsSupplayForm(),
    #             "frmNumbs": map(str, list(range(1, 27))),
    #             "frmTitles": ["Virtual/GoodsProviders/forooshandeh/frm%s.html" % (x,) for x in
    #                           map(str, list(range(1, 27)))]
    #             # "downloadForm": GoodsSupplayFormDownloadPdf()
    #         },
    #         context_instance=RequestContext(self.request)
    #     )
