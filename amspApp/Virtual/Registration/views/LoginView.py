import json
from datetime import datetime

from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from amspApp.Administrator.Customers.views.CustomerRegistrationView import CustomerRegistrationViewSet
from amspApp.CompaniesManagment.Hamkari.models import Hamkari, RequestHamkari
from amspApp.CompaniesManagment.Hamkari.serializers.HamkariSerializer import HamkariSerializer, \
    RequestHamkariSerializer, \
    ProfileHamkariCommentsSerializer
from amspApp.CompaniesManagment.Positions.models import Position, PositionsDocument
from amspApp.CompaniesManagment.Positions.serializers.PositionSerializer import PositionDocumentSerializer
from amspApp.MyProfile.models import Profile, ProfileHamkariComments
from amspApp.MyProfile.serializers.ProfileSerializer import ProfileSerializer
from amspApp.Sales.permissions.basePermissions import AllAccess
from amspApp.Virtual.Registration.forms.loginForm import RegisterationHireForm, RegisterationLoginForm
from amspApp._Share.ErrorMessageParser import convertFormMessage
from amspApp.amspUser.models import MyUser
from amspApp.amspUser.serializers.UserSerializer import UserSerializer


class LoginViewSet(viewsets.ModelViewSet):
    # def __init__(self):
    # pass

    @never_cache
    @csrf_exempt
    @permission_classes([AllAccess])
    @authentication_classes([AllowAny])
    @list_route(methods=["get"])
    def check_logined(self, request):
        return Response({"is_active": request.user.is_active})

    @never_cache
    @csrf_exempt
    @permission_classes([AllAccess])
    @authentication_classes([AllowAny])
    @list_route(methods=["get"])
    def is_server_available(self, request):
        return Response({"is_available": True})

    @list_route(methods=["post"])
    def login(self, request):
        # validating
        # print("login start")

        loginFrm = RegisterationLoginForm(request.data)
        if self.request.is_ajax():
            if not loginFrm.is_valid():
                to_json_response = dict()
                to_json_response['status'] = 0
                to_json_response['form_errors'] = loginFrm.errors
                to_json_response['new_cptch_key'] = CaptchaStore.generate_key()
                to_json_response['new_cptch_image'] = captcha_image_url(to_json_response['new_cptch_key'])
                return HttpResponse(json.dumps(to_json_response), content_type='application/json')

        user = authenticate(username=loginFrm.data["username"], password=loginFrm.data["password"])
        if user is not None:
            login(request, user)
            return Response({})

        to_json_response = dict()
        to_json_response['status'] = 0
        to_json_response['form_errors'] = {
            "username": ["Invalid username or password"],
            "password": ["Invalid username or password"],
        }
        to_json_response['new_cptch_key'] = CaptchaStore.generate_key()
        to_json_response['new_cptch_image'] = captcha_image_url(to_json_response['new_cptch_key'])
        # print("login end")
        return HttpResponse(json.dumps(to_json_response), content_type='application/json')
        #
        # return Response({"pass":"ok"})

    @list_route(methods=["get"])
    def registerRefCaptcha(self, request):
        to_json_response = {}
        to_json_response['key'] = CaptchaStore.generate_key()
        to_json_response['image_url'] = captcha_image_url(to_json_response['key'])
        return Response(to_json_response)

    @list_route(methods=["post"])
    def register(self, request):
        form = RegisterationHireForm(request.data)
        reg_exp = []
        if not form.is_valid():
            res = convertFormMessage(form.errors)
            json = form.errors
            return Response({
                'status': 'Not Acceptable',
                'message': res,
                'json': json

            }, status=status.HTTP_406_NOT_ACCEPTABLE)
        # checking if username exits
        userCount = MyUser.objects.filter(username=request.data["username"]).count()
        if userCount != 0:
            return Response({
                'status': 'Not Acceptable',
                'message': [{"fieldName": "نام کاربری",
                             "message": "این کاربر قبلا در سیستم ثبت نام کرده است - در صورت فراموشی رمز عبور دکمه ی فراموشی رمز عبور را انتخاب نمایید"}],

            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        userCount = MyUser.objects.filter(email=request.data["email"]).count()
        if userCount != 0:
            return Response({
                'status': 'Not Acceptable',
                'message': [{"fieldName": "ایمیل ",
                             "message": "این ایمیل قبلا در سیستم ثبت نام کرده است - در صورت فراموشی رمز عبور دکمه ی فراموشی رمز عبور را انتخاب نمایید"}],

            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        req = {}
        req = request.data
        req["confirm_password"] = request.data["passwordConfirm"]

        # req["customerID"] = customerID
        serializer = UserSerializer(data=req)

        if serializer.is_valid():
            result = serializer.create(serializer.validated_data)
            CustomerRegistrationViewSet().addUserToCustomer(result.id,
                                                            CustomerRegistrationViewSet().GetCustomerIDFromBilling(
                                                                request))

            user = authenticate(username=form.data["username"], password=form.data["password"])
            login(request, user)

            profileInstance = Profile.objects.get(userID=user.id)
            profileInstance.update(set__extra__isAllowed=False)
            profileInstance.update(set__extra__heIsUserOfThisSubdomainAndFirstLogin=False)
            profileInstance.update(set__extra__Name=form.data["name"] + " " + form.data["family"])
            profileInstance.update(set__extra__job__Shenasnameh__Name=form.data["name"])
            profileInstance.update(set__extra__job__Shenasnameh__Family=form.data["family"])

            return Response({})
        else:
            return Response({
                'status': 'Bad request',
                'message': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

    def registerFromAdmin(self, request):
        form = RegisterationHireForm(request.data)
        reg_exp = []
        if not form.is_valid():
            res = convertFormMessage(form.errors)
            json = form.errors
            return Response({
                'status': 'Not Acceptable',
                'message': res,
                'json': json

            }, status=status.HTTP_406_NOT_ACCEPTABLE)
        # checking if username exits
        userCount = MyUser.objects.filter(username=request.data["username"]).count()
        if userCount != 0:
            return Response({
                'status': 'Not Acceptable',
                'message': [{"fieldName": "نام کاربری",
                             "message": "این کاربر قبلا در سیستم ثبت نام کرده است - در صورت فراموشی رمز عبور دکمه ی فراموشی رمز عبور را انتخاب نمایید"}],

            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        userCount = MyUser.objects.filter(email=request.data["email"]).count()
        if userCount != 0:
            return Response({
                'status': 'Not Acceptable',
                'message': [{"fieldName": "ایمیل ",
                             "message": "این ایمیل قبلا در سیستم ثبت نام کرده است - در صورت فراموشی رمز عبور دکمه ی فراموشی رمز عبور را انتخاب نمایید"}],

            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        req = {}
        req = request.data
        req["confirm_password"] = request.data["passwordConfirm"]

        # req["customerID"] = customerID
        serializer = UserSerializer(data=req)

        if serializer.is_valid():
            result = serializer.create(serializer.validated_data)
            CustomerRegistrationViewSet().addUserToCustomer(result.id,
                                                            CustomerRegistrationViewSet().GetCustomerIDFromBilling(
                                                                request))

            user = authenticate(username=form.data["username"], password=form.data["password"])
            login(request, user)
            profileInstance = Profile.objects.get(userID=user.id)
            profileInstance.update(set__extra__isAllowed=False)
            profileInstance.update(set__extra__Name=form.data["name"] + " " + form.data["family"])
            profileInstance.update(set__extra__job__Shenasnameh__Name=form.data["name"])
            profileInstance.update(set__extra__job__Shenasnameh__Family=form.data["family"])

            return Response({})
        else:
            return Response({
                'status': 'Bad request',
                'message': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

    jobDetails = [
        {'name': 'Shenasnameh', 'value': '1'},
        {'name': 'Education', 'value': '2'},
        {'name': 'Language', 'value': '3'},
        {'name': 'Doreh', 'value': '4'},
        {'name': 'Experience', 'value': '5'},
        {'name': 'Software', 'value': '6'},
        {'name': 'Job', 'value': '7'},
        {'name': 'Resume', 'value': '8'}
    ]

    @detail_route(methods=["post"])
    def step(self, request, *args, **kwargs):
        profile = Profile.objects.get(userID=request.user.id)
        extra = profile.extra
        if not "job" in extra:
            extra["job"] = {}
            serial = ProfileSerializer(instance=profile, data={"extra": extra})
            serial.is_valid(raise_exception=True)
            profile = serial.save()
            extra = profile.extra

        for j in self.jobDetails:
            if not j["name"] in extra["job"]:
                extra["job"][j["name"]] = {}
                serial = ProfileSerializer(instance=profile, data={"extra": extra})
                serial.is_valid(raise_exception=True)
                profile = serial.save()
                extra = profile.extra

        for j in self.jobDetails:
            if kwargs["pk"] == j["value"]:
                extra["job"][j["name"]] = request.data
        extra["Name"] = extra['job']['Shenasnameh']['Name'] + " " + extra['job']['Shenasnameh']['Family']
        serial = ProfileSerializer(instance=profile, data={"extra": extra})
        serial.is_valid(raise_exception=True)
        serial.save()
        return Response({})

    @detail_route(methods=["get"])
    def getstep(self, request, *args, **kwargs):
        profile = Profile.objects.get(userID=request.user.id)
        extra = profile.extra

        res = extra["job"] if "job" in extra else {}
        for j in self.jobDetails:
            if kwargs["pk"] == j["value"]:
                if res != {}:
                    res = extra["job"][j["name"]] if j["name"] in extra["job"] else {}

        return Response(res)

    @list_route(methods=["get"])
    def get_prev(self, request, *args, **kwargs):
        profile = Profile.objects.get(userID=request.user.id)
        extra = profile.extra
        res = profile.extra["job"] if "job" in profile.extra else {}
        return Response(res)

    @list_route(methods=["get"])
    def logout(self, request):
        logout(request)
        return Response({})

    @list_route(methods=["get"])
    def red_logout(self, request):
        logout(request)
        return redirect('/reg/#/login')

    @list_route(methods=["get"])
    def get_all_jobs(self, request):
        customerInstance = CustomerRegistrationViewSet().GetCustomerInstanceFromBilling(request)
        userID = customerInstance.userID
        # loding all jobs
        jobs = Hamkari.objects.filter(startDate__lte=datetime.now()).filter(endDate__gte=datetime.now())
        result = []
        for j in jobs:
            result.append(HamkariSerializer(instance=j).data)
        return Response(result)

    @detail_route(methods=["post"])
    def answerQustions(self, request, *args, **kwargs):
        customerInstance = CustomerRegistrationViewSet().GetCustomerInstanceFromBilling(request)
        userID = request.user.id
        customerID = customerInstance.id
        hamkariID = kwargs["pk"]
        hamkInstance = Hamkari.objects.get(id=hamkariID)
        requestedHamkInstance = RequestHamkari.objects.filter(
            userID=userID,
            customerID=customerID,
            hamkariID=hamkariID
        )
        if requestedHamkInstance.count() == 0:
            dt = {
                "userID": userID,
                "customerID": customerID,
                "hamkariID": hamkariID,
                "extra": {}
            }
            serial = RequestHamkariSerializer(data=dt)
            serial.is_valid(raise_exception=True)
            requestedHamkInstance = serial.save()
        else:
            requestedHamkInstance = requestedHamkInstance[0]

        extra = requestedHamkInstance.extra
        if not "answers" in extra:
            extra = requestedHamkInstance.extra
            extra["answers"] = []
            serial = RequestHamkariSerializer(
                instance=requestedHamkInstance,
                data={'extra': extra},
                partial=True)
            serial.is_valid(raise_exception=True)
            requestedHamkInstance = serial.save()

        if not "requests" in extra:
            extra = requestedHamkInstance.extra
            extra["requests"] = []
            serial = RequestHamkariSerializer(
                instance=requestedHamkInstance,
                data={'extra': extra},
                partial=True)

            serial.is_valid(raise_exception=True)
            requestedHamkInstance = serial.save()

        extra = requestedHamkInstance.extra
        extra["answers"] = request.data
        serial = RequestHamkariSerializer(instance=requestedHamkInstance, data={'extra': extra},
                                          partial=True)
        serial.is_valid(raise_exception=True)
        serial.save()
        return Response({})

    @detail_route(methods=["post"])
    def answerReqs(self, request, *args, **kwargs):
        customerInstance = CustomerRegistrationViewSet().GetCustomerInstanceFromBilling(request)
        userID = request.user.id
        customerID = customerInstance.id
        hamkariID = kwargs["pk"]
        hamkInstance = Hamkari.objects.get(id=hamkariID)
        requestedHamkInstance = RequestHamkari.objects.filter(
            userID=userID,
            customerID=customerID,
            hamkariID=hamkariID
        )
        if requestedHamkInstance.count() == 0:
            dt = {
                "userID": userID,
                "customerID": customerID,
                "hamkariID": hamkariID,
                "extra": {}
            }
            serial = RequestHamkariSerializer(data=dt)
            serial.is_valid(raise_exception=True)
            requestedHamkInstance = serial.save()
        else:
            requestedHamkInstance = requestedHamkInstance[0]

        extra = requestedHamkInstance.extra
        if not "answers" in extra:
            extra = requestedHamkInstance.extra
            extra["answers"] = []
            serial = RequestHamkariSerializer(
                instance=requestedHamkInstance,
                data={'extra': extra},
                partial=True)
            serial.is_valid(raise_exception=True)
            requestedHamkInstance = serial.save()

        if not "requests" in extra:
            extra = requestedHamkInstance.extra
            extra["requests"] = []
            serial = RequestHamkariSerializer(
                instance=requestedHamkInstance,
                data={'extra': extra},
                partial=True)

            serial.is_valid(raise_exception=True)
            requestedHamkInstance = serial.save()

        extra = requestedHamkInstance.extra
        extra["requests"] = request.data
        serial = RequestHamkariSerializer(instance=requestedHamkInstance, data={'extra': extra},
                                          partial=True)
        serial.is_valid(raise_exception=True)
        serial.save()
        return Response({})

    @detail_route(methods=["get"])
    def getJobDetail(self, request, *args, **kwargs):
        customerInstance = CustomerRegistrationViewSet().GetCustomerInstanceFromBilling(request)
        userID = request.user.id
        customerID = customerInstance.id
        hamkariID = kwargs["pk"]
        hamkInstance = Hamkari.objects.get(id=hamkariID)
        requestedHamkInstance = RequestHamkari.objects.filter(
            userID=userID,
            customerID=customerID,
            hamkariID=hamkariID)
        return Response(requestedHamkInstance[0].extra)

    @list_route(methods=["get"])
    def get_reg_jobs(self, request, *args, **kwargs):
        customerInstance = CustomerRegistrationViewSet().GetCustomerInstanceFromBilling(request)
        userID = request.user.id
        customerID = customerInstance.id
        requestedHamkInstance = RequestHamkari.objects.filter(userID=userID)
        hamkari = Hamkari.objects.filter(id__in=[x.hamkariID for x in requestedHamkInstance])

        res = []
        for r in requestedHamkInstance:
            dt = RequestHamkariSerializer(instance=r).data
            dt["hamkarititle"] = hamkari.get(id=dt["hamkariID"]).title
            res.append(dt)

        return Response(res)

    @detail_route(methods=["get"])
    def get_prev_with_edit(self, request, *args, **kwargs):
        profile = Profile.objects.get(id=kwargs["pk"])
        extra = profile.extra
        res = profile.extra["job"] if "job" in profile.extra else {}
        return Response(res)

    @detail_route(methods=["post"])
    def post_resume_comments(self, request, *args, **kwargs):
        profile = Profile.objects.get(id=kwargs["pk"])
        pos = Position.objects.get(
            user=request.user,
            company=request.user.current_company)
        posDoc = PositionsDocument.objects.get(positionID=pos.id)
        posDoc = PositionDocumentSerializer(instance=posDoc).data
        dt = {
            'commentWritePositionID': pos.id,
            'commentWritePositionDesc': posDoc,
            'ProfileID': profile.id,
            'comment': request.data["body"]
        }
        serial = ProfileHamkariCommentsSerializer(data=dt)
        serial.is_valid(raise_exception=True)
        serial.save()
        return Response({})

    @detail_route(methods=["get"])
    def get_resume_comments(self, request, *args, **kwargs):
        profile = Profile.objects.get(id=kwargs["pk"])
        pos = Position.objects.get(
            user=request.user,
            company=request.user.current_company)
        posDoc = PositionsDocument.objects.get(positionID=pos.id)
        posDoc = PositionDocumentSerializer(instance=posDoc).data
        objs = ProfileHamkariComments.objects.filter(ProfileID=profile.id).order_by("-id")
        serial = ProfileHamkariCommentsSerializer(instance=objs, many=True).data
        return Response(serial)
