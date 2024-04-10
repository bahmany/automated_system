from random import randint

from django.contrib.auth.hashers import make_password
from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp._Share.ListPagination import ListPagination
from amspApp.tasks import sendSMS


class ChangeViewSet(viewsets.ModelViewSet):
    pagination_class = ListPagination

    # lookup_field = "id"
    # serializer_class = InboxSerializer

    def template_view(self, request, *args, **kwargs):
        return render_to_response(
            "settings/publics/change.html",
            {"email": request.user.email}, context_instance=RequestContext(request))

    @list_route(methods=["post"])
    def changepassword(self, request):
        if not (request.user.check_password(request.data["current"])):
            return Response({"error": ""})
        if request.data["new"] == request.data["newConfirm"]:
            request.user.set_password(request.data["new"])
            request.user.save()
        else:
            return Response({"error": ""})
        return Response({})

    @list_route(methods=["post"])
    def changeSignPass(self, request):
        if request.data["new"] == request.data["newConfirm"]:

            if not request.user.cellphone:
                return Response({"error": "هنوز شماره موبایلی برای شما تعریف نشده ، لطفا با مدیر سیستم مشورت کنید"})

            hashed_pwd = make_password(request.data["new"])
            request.user.sign_password_before_confirm = hashed_pwd
            request.user.is_sign_pass_correct = False
            request.user.sign_password_confirmsms = str(randint(3258425, 9289929))
            sms = " رمز صحت سنجی %s می باشد این کد بمدت ۵ دقیقه معتبر است" % (request.user.sign_password_confirmsms,)
            sendSMS.delay(request.user.cellphone, sms)
            request.user.save(force_update=True)
        else:
            return Response({"error": "رمز امضا مطابقت ندارد"})
        return Response({"ok": "ok"})

    @list_route(methods=["post"])
    def changeSignVerifySMS(self, request):
        if not request.user.cellphone:
            return Response({"error": "هنوز شماره موبایلی برای شما تعریف نشده ، لطفا با مدیر سیستم مشورت کنید"})

        if not request.user.sign_password_before_confirm:
            return Response({"error": "شما قبلا رمز دوم تریف نکرده اید"})

        vr = request.data["smsCode"]
        if not vr:
            return Response({"error": "کدی وارد نکرده اید"})

        if vr == "undefined":
            return Response({"error": "کدی وارد نکرده اید"})

        if vr != request.user.sign_password_confirmsms:
            return Response({"error": "کد وارد شده اشتباه است"})

        # here we have security bug for sending unlimited requests for checking verified code

        request.user.sign_password = request.user.sign_password_before_confirm
        request.user.sign_password_before_confirm = ""
        request.user.is_sign_pass_correct = True
        request.user.sign_password_confirmsms = ""
        sendSMS.delay(request.user.cellphone, "رمز دوم شما تعیین شد  سپاس گذاریم")
        request.user.save(force_update=True)
        return Response({"ok": "ok"})

    @list_route(methods=["post"])
    def changeemail(self, request):
        if not (request.user.email == request.data["current"]):
            return Response({"error": ""})
        if request.data["new"] == request.data["newConfirm"]:
            request.user.email = request.data["new"]
            request.user.save()
        else:
            return Response({"error": ""})
        return Response({})
