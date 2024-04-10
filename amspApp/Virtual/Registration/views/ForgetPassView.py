import uuid
from datetime import datetime

from django.shortcuts import redirect
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer
from rest_framework.response import Response

from amsp import settings
from amspApp.Infrustructures.Classes.SendMail import sendMail
from amspApp.Virtual.Registration.forms.loginForm import ForgetForm, ResetForm
from amspApp.amspUser.models import MyUser
from amspApp.amspUser.serializers.UserSerializer import UserSerializer


class ForgetPassView(viewsets.ModelViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'email'
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    renderer_classes = (JSONRenderer, BrowsableAPIRenderer, HTMLFormRenderer)

    def create(self, request, *args, **kwargs):
        frm = ForgetForm(data = request.data)
        if not frm.is_valid():
            return Response({"message": "لطفا شکل خواسته شده به درستی تکمیل نمایید", "status": "Unauthorized"},
                            status=status.HTTP_401_UNAUTHORIZED)
        # getting user instance by username or email
        # first email
        instance = MyUser.objects.filter(email=request.data["name"])
        found = 0
        if instance.count() == 1:
            found = 1
        if found == 0:
            instance = MyUser.objects.filter(username=request.data["name"])
            if instance.count() == 1:
                found = 2
        if found == 0:
            return Response({"message": "نام کاربری یا ایمیل در سیستم قبت نشده است لطفا ثبت نام نمایید", "status": "Unauthorized"},
                            status=status.HTTP_401_UNAUTHORIZED)

        requestedUser = instance[0]
        guidFirst = uuid.uuid4().hex
        guidSeccond = uuid.uuid4().hex
        guidThird = uuid.uuid4().hex
        finalGuid = guidFirst + guidSeccond + guidThird
        requestedUser.password_reset = finalGuid
        requestedUser.password_reset_post_date = datetime.now()
        requestedUser.save()
        addressOfThisHost = "http://%s/reg/#/%s/reset" % (
            request._request.META['HTTP_REFERER'].split("//")[1].split("/")[0],
            finalGuid)
        subject = "Password Reset Link from Morabaa"
        message = """
        Dear user,
        You have been requested password reset link from morabaa,
        This link is available for 48 hours.
        click here to to reset your password : %s
        if this link sent without your request, please left it alone, it will be deleted in next 48 hours


        Morabaa - A new generation of Virtual Society


         best regards
         Morabaa...
        """ % addressOfThisHost
        addresses = [requestedUser.email]
        sendMail(subject, message, addresses)
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        # key = request.query_params["q"]
        # self.queryset = MyUser.objects.filter(password_reset = key)
        return redirect("/#/ResetPassword/" + request.query_params["q"] + "/")

    @list_route(methods=["POST"])
    def reset(self, request):

        frm = ResetForm(data = request.data)
        if not frm.is_valid():
            return Response({"message": "لطفا اطلاعات خواسته شده به درستی تکمیل نمایید", "status": "Unauthorized"},
                            status=status.HTTP_401_UNAUTHORIZED)

        key = request.data["uid"]


        userInstance = MyUser.objects.filter(password_reset=key)

        if userInstance.count() != 1:
            return Response({
                'status': 'Unauthorized',
                'message': 'User not found !!'
            }, status=status.HTTP_400_BAD_REQUEST)

        userInstance = userInstance[0]
        userInstance.set_password(request.data["password"])
        userInstance.password_reset = ""
        userInstance.save()
        return Response({})