# coding=utf-8
import uuid
from datetime import datetime
from random import randint

from captcha.models import CaptchaStore
from django.contrib.auth import login, authenticate
from django.db.models import Q as _Q
from mongoengine import Q
from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.response import Response

from amspApp.Administrator.Customers.views.CustomerRegistrationView import CustomerRegistrationViewSet
from amspApp.Dashboards.Registeration.FirstRegForm import FirstRegForm, ForgetPassForm
from amspApp.Dashboards.Supply.models import SupplementCategories
from amspApp.Dashboards.Supply.serialization.GoodsSupplaySerializer import SupplementCategoriesSerializer
from amspApp.MyProfile.models import Profile
from amspApp.amspUser.models import MyUser, FirstReg, ForgetPassCodes
from amspApp.amspUser.serializers.UserSerializer import FirstRegSerializer, UserSerializer, ForgetPassCodesSerializer
from amspApp.tasks import sendSMS


class FirstregViewset(viewsets.ModelViewSet):

    @list_route(methods=["POST"])
    def verfCode(self, request, *args, **kwargs):
        hash = request.data["data"]
        code = request.data["verfCode"]
        if len(hash) != 96:
            return Response({"result": "error", "details": "کد اشتباه وارد شده است"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        if len(code) != 6:
            return Response({"result": "error", "details": "کد اشتباه وارد شده است"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        vf = FirstReg.objects.filter(hash=hash).count()
        if vf != 1:
            return Response({"result": "error", "details": "کد اشتباه وارد شده است"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        kf = FirstReg.objects.filter(hash=hash).first()

        if kf.verifyTry > 4:
            FirstReg.objects.filter(hash=hash).delete()
            return Response(
                {"result": "error", "details": "بیش از ۳ بار کد اشتباه وارد کردید - لطفا مجددا ثبت نام کنید"},
                status=status.HTTP_406_NOT_ACCEPTABLE)

        if vf == 1:
            vf = FirstReg.objects.filter(hash=hash, gencode=code).first()
            if vf is None:
                kf(set__verifyTry=kf.verifyTry + 1)
                return Response({"result": "error", "details": "کد اشتباه وارد شده است"},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

        dt = {
            "username": vf.cellNo.replace("+", ""),
            "first_name": "نام",
            "last_name": "نام خانوادگی",
            "email": vf.cellNo.replace("+", "") + "@tempo.com",
            "password": vf.password,
            "confirm_password": vf.password,
            "cellphone": vf.cellNo,
            "account_type": 2
        }

        serializer = UserSerializer(data=dt)
        serializer.is_valid(raise_exception=True)
        result = serializer.create(serializer.validated_data)
        CustomerRegistrationViewSet().addUserToCustomer(result.id,
                                                        CustomerRegistrationViewSet().GetCustomerIDFromBilling(
                                                            request))
        profileInstance = Profile.objects.get(userID=result.id)
        profileInstance.update(set__extra__isAllowed=False)
        profileInstance.update(set__extra__heIsUserOfThisSubdomainAndFirstLogin=False)
        profileInstance.update(set__extra__Name="نا مشخص")
        profileInstance.update(set__extra__job__Shenasnameh__Name="وارد نشده")
        profileInstance.update(set__extra__job__Shenasnameh__Family="وارد نشده")

        FirstReg.objects.filter(hash=hash).delete()

        user = authenticate(username=result.username, password=vf.password)

        login(request, user)

        sendSMS.delay(
            vf.cellNo,
            "کاربر محترم - برای شما در سامانه ما محیط اختصاصی ایجاد شد - نام کاربری شما %s و رمز عبور شما %s می باشد "
            "****.com" % (
                vf.cellNo.replace("+", ""), vf.password,))

        return Response({"result": "ok"})

    @list_route(methods=["POST"])
    def regWithCell(self, request, *args, **kwargs):

        frm = FirstRegForm(data=request.data)
        if not frm.is_valid():
            CaptchaStore.generate_key()
            return Response({"result": "error", "details": dict(frm.errors.items())},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        checkedIfCellExit = MyUser.objects.filter(cellphone=frm.data["cellNo"]).count()
        if checkedIfCellExit != 0:
            return Response({"result": "error", "details": {
                "cellNo": "این شماره قبلا استفاده شده است - در صورتی که رمز عبور خود را فراموش کرده اید به قسمت " +
                          "فراموشی رمز عبور مراجعه نمایید "
            }}, status=status.HTTP_406_NOT_ACCEPTABLE)

        checkIfCellFirstRegBefore = FirstReg.objects.filter(cellNo=request.data["cellNo"]).count()
        if checkIfCellFirstRegBefore > 0:
            lastRegInstance = FirstReg.objects.filter(cellNo=request.data["cellNo"]).first()
            if (datetime.now() - lastRegInstance.dateOfPost).total_seconds() > 360:  # user is waiting more than 360 sec
                FirstReg.objects.filter(cellNo=request.data["cellNo"]).delete()
                return Response({"result": "error", "details": {
                    "cellNo": "این شماره قبلا ثبت نام کرده و پیام کوتاه برای آن ارسال شده است ولی به نظر می رسد هنوز "
                              "پیام کوتاه را دریافت نکرده لطفا مججدا فرم رو تکمیل نمایید "
                }}, status=status.HTTP_406_NOT_ACCEPTABLE)

            if ((
                    datetime.now() - lastRegInstance.dateOfPost).total_seconds() <= 360):  # user is waiting more than 360 sec
                return Response({"result": "error", "details": {
                    "cellNo": "لطفا بمدت سه دقیقه منتظر پیام کوتاه باشید و پس از آن مجددا تلاش نمایید"
                }}, status=status.HTTP_406_NOT_ACCEPTABLE)

            return Response({"result": "error", "details": {
                "cellNo": "این شماره قبلا استفاده شده است - در صورتی که رمز عبور خود را فراموش کرده اید به قسمت " +
                          "فراموشی رمز عبور مراجعه نمایید "
            }}, status=status.HTTP_406_NOT_ACCEPTABLE)

        request.data["gencode"] = str(randint(154855, 998584))
        request.data["hash"] = uuid.uuid4().hex + uuid.uuid4().hex + uuid.uuid4().hex
        frm = FirstRegSerializer(data=request.data)

        if not frm.is_valid():
            CaptchaStore.generate_key()
            return Response({"result": "error", "details": dict(frm.errors.items())},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        frm.is_valid(raise_exception=True)
        frm.save()
        sendSMS.delay(frm.data["cellNo"], "کد فعال سازی %s" % (request.data["gencode"],))
        return Response({"result": "ok", "data": request.data["hash"]})

        # 77fdfb8869504c5f9bfb529bf18227ba32a80de1738440a99d9fdd89a72a693775dac637947845539443f6270607dde9
        # if not frm.is_valid():
        #     CaptchaStore.generate_key()
        #     return Response({"result": "error", "details": dict(frm.errors.items())},
        #                     status=status.HTTP_406_NOT_ACCEPTABLE)
        #
        # # check if mobile registered before
        # checkedIfCellExit = MyUser.objects.filter(cellphone=frm.data["cellNo"]).count()
        # if checkedIfCellExit != 0:
        #     return Response({"result": "error", "details": {
        #         "cellNo": "این شماره قبلا استفاده شده است - در صورتی که رمز عبور خود را فراموش کرده اید به قسمت " +
        #                   "فراموشی رمز عبور مراجعه نمایید "
        #     }}, status=status.HTTP_406_NOT_ACCEPTABLE)
        # dt = {}
        # dt["username"] = frm.data["cellNo"].replace("+", "")
        # dt["first_name"] = "نام"
        # dt["last_name"] = "نام خانوادگی"
        # dt["email"] = frm.data["cellNo"].replace("+", "")+"@tempo.com"
        # dt["password"] = frm.data["password"]
        # dt["confirm_password"] = frm.data["password"]
        # dt["account_type"] = 2
        # serializer = UserSerializer(data=dt)
        # serializer.is_valid(raise_exception=True)
        # result = serializer.create(serializer.validated_data)
        # CustomerRegistrationViewSet().addUserToCustomer(result.id,
        #                                                 CustomerRegistrationViewSet().GetCustomerIDFromBilling(
        #                                                     request))
        # profileInstance = Profile.objects.get(userID=result.id)
        # profileInstance.update(set__extra__isAllowed=False)
        # profileInstance.update(set__extra__heIsUserOfThisSubdomainAndFirstLogin=True)
        # profileInstance.update(set__extra__Name="نا مشخص")
        # profileInstance.update(set__extra__job__Shenasnameh__Name="وارد نشده")
        # profileInstance.update(set__extra__job__Shenasnameh__Family="وارد نشده")

    @list_route(methods=["POST"])
    def sendForgetPassVerficationCode(self, request, *args, **kwargs):
        if request.data['cellNo'][0:2] == "09":
            request.data['cellNo'] = "+989" + request.data['cellNo']
            request.data['cellNo'] = request.data['cellNo'].replace("+98909", "+989")
        if request.data['cellNo'][0:1] == "9":
            request.data['cellNo'] = "+989" + request.data['cellNo']
            request.data['cellNo'] = request.data['cellNo'].replace("+9899", "+989")
            request.data['cellNo'] = request.data['cellNo'].replace("+", "")

        firstCase = "0" + request.data['cellNo'][2:]
        secondCase = "0" + request.data['cellNo'][3:]

        frm = ForgetPassForm(request.data)
        if not frm.is_valid():
            return Response({"result": "error", "details": "شماره موبایل وارد شده یا شکل گرافیکی اشتباه است"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        checkIfUserHasAccountOrNot = MyUser.objects.filter(
            _Q(cellphone=frm.data.get('cellNo')) |
            _Q(cellphone=firstCase) |
            _Q(cellphone=secondCase)
        ).count()

        if checkIfUserHasAccountOrNot == 0:
            return Response({"result": "error", "details": "این شماره موبایل در سامانه ثبت نام نکرده است"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        ForgetPassCodes.objects.filter(
            Q(cellNo=frm.data.get('cellNo')) |
            Q(cellNo="98" + frm.data.get('cellNo')) |
            Q(cellNo="980" + frm.data.get('cellNo')) |
            Q(cellNo="+98" + frm.data.get('cellNo'))).delete()

        # checkIfThisUserRequestCodeBefore = ForgetPassCodes.objects.filter(userID=userInstance.id).count()
        #
        # if checkIfThisUserRequestCodeBefore != 0:
        #     ForgetPassCodes.objects.filter(userID=userInstance.id).delete()
        #     return Response({"result": "error",
        #                      "details": "برای شما قبلا کد ارسال شده بود - لطفا صفحه را مجددا ریفرش نموده و شماره موبایل خود را وارد نمایید"},
        #                     status=status.HTTP_406_NOT_ACCEPTABLE)

        userInstance = MyUser.objects.filter(
            _Q(cellphone=frm.data.get('cellNo')) |
            _Q(cellphone=firstCase) |
            _Q(cellphone=secondCase)
        ).order_by("-id").first()

        gencode = str(randint(154855, 998584))
        hash = uuid.uuid4().hex + uuid.uuid4().hex + uuid.uuid4().hex

        dt = {
            'cellNo': frm.data.get('cellNo'),
            'userID': userInstance.id,
            'gencode': gencode,
            'verifyTry': 0,
            'hash': hash
        }

        forgetPass = ForgetPassCodesSerializer(data=dt)
        forgetPass.is_valid(raise_exception=True)
        forgetPass.save()

        sendSMS.delay(frm.data.get('cellNo'), "کد فعال سازی %s فراموشی رمز" % (gencode,))

        return Response({"result": "ok", "data": hash})

    @list_route(methods=["POST"])
    def verifyForgetPassVerficationCode(self, request, *args, **kwargs):
        verfInstances = ForgetPassCodes.objects.filter(
            Q(hash=request.data.get("hash", "--")) & Q(gencode=request.data.get("code", "--")))
        if verfInstances.count() == 0:
            return Response({"result": "error",
                             "details": "فراموشی رمز عبور برای این کاربر معتبر نمی باشد"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        verfInstance = verfInstances.first()
        userInstance = MyUser.objects.get(id=verfInstance.userID)
        userInstance.set_password(request.data.get("code"))
        userInstance.save()
        verfInstances.delete()
        sendSMS.delay(userInstance.cellphone,
                               "رمز شما تغییر کرد به %s و نام کاربری شما نیز %s می باشد" % (
                                   request.data.get("code", "--"),
                                   userInstance.username
                               ))
        # user = authenticate(username=result.username, password=vf.password)
        user = authenticate(username=userInstance.username, password=request.data.get("code"))

        login(request, user)

        return Response({"result": "ok"})

    @list_route(methods=["POST"])
    def updateSecondReg(self, request, *args, **kwargs):
        userInsance = request.user
        userInsance.account_type = int(request.data.get("type", userInsance.account_type)) if int(
            request.data.get("type",
                             userInsance.account_type)) in [
                                                                                                  4, 5, 6,
                                                                                                  7] else userInsance.account_type
        userInsance.save()
        return Response({"ok": "ok"})

    @list_route(methods=["GET"])
    def getUserType(self, request, *args, **kwargs):
        return Response({"type": request.user.account_type})

    @list_route(methods=["GET"])
    def getCats(self, request, *args, **kwargs):
        _list = SupplementCategories.objects.filter(parent__ne = None)
        _list = SupplementCategoriesSerializer(instance=_list, many=True).data
        # parents = SupplementCategories.objects.filter(parent = None).order_by('-name')
        # parents = SupplementCategoriesSerializer(instance=parents, many=True).data

        # for p in parents:
        #     child = SupplementCategories.objects.filter(parent = p['id'])
        #     child = SupplementCategoriesSerializer(instance=child, many=True).data
        #     p['child'] = child

        for l in _list:
            if l.get("parent"):
                p = SupplementCategories.objects.get(id=l.get('parent').get("id")).name
                l["parent_name"] = p

        return Response({"res": "ok", "data": _list})
