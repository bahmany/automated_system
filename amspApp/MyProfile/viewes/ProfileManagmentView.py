# coding=utf-8
import base64
import os
import tempfile
import uuid
from datetime import datetime, timedelta
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from mongoengine import ValidationError
from rest_framework import status
from rest_framework.decorators import list_route, detail_route
from rest_framework_mongoengine import viewsets
from rest_framework.response import Response
from amspApp.CompaniesManagment.Charts.models import Chart
from amspApp.CompaniesManagment.CompanyProfile.models import CompanyProfile
from amspApp.CompaniesManagment.CompanyProfile.serializers.CompanyProfileSerializers import CompanyProfileSerializer
from amspApp.CompaniesManagment.Hamkari.serializers.HamkariSerializer import HamkariSerializer, HamkariJobsSerializer
from amspApp.CompaniesManagment.Positions.models import PositionsDocument
from amspApp.CompaniesManagment.models import CompanyMembersJointRequest, Company
from amspApp.CompaniesManagment.serializers.CompanyMembersJointRequestSerializers import \
    CompanyMembersJointRequestSerializer
from amspApp.FileServer.models import File
from amspApp.FileServer.views.FileUploadView import FileUploadViewSet
from amspApp.Infrustructures.Classes.PublicFilters import QuerySetFilter
from amspApp.MyProfile.models import Profile, Posts
from amspApp.MyProfile.serializers.ProfileSerializer import ProfileSerializer
from django.utils.translation import ugettext_lazy as _
from mongoengine.django.shortcuts import get_document_or_404
from amspApp._Share.ListPagination import ListPagination
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset

__author__ = 'mohammad'


class ProfileManagmentViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = ListPagination

    def get_object(self):
        try:
            obj = Profile.objects.get(userID=self.request.user.pk)
        except(Profile.DoesNotExist, ValidationError):
            obj = ProfileSerializer().create_default_profile(self.request.user)
        # self.check_object_permissions(self.request, obj)
        return obj

    # def GetAvatar(self, request):
    # try:
    #         profile = MyProfile.objects.get(userID=request.user.pk)
    #         profilePic = profile["extra"]["profileAvatar"]["url"]
    #         return Response({"addr": profilePic})
    #     except(MyProfile.DoesNotExist, ValidationError):
    #         return Response({
    #             "addr": "/static/ani-theme/images/flat-avatar.png"
    #         })
    #

    def template_view(self, request, *args, **kwargs):
        data = {
            "YearOfJoint": request.user.date_joined.year
        }
        return render_to_response(
            "myProfile/PersonProfile.html",
            data,
            context_instance=RequestContext(self.request)
        )

    def list(self, request, *args, **kwargs):
        return Response({})

    def update(self, request, *args, **kwargs):
        result = super(ProfileManagmentViewSet, self).update(request, *args, **kwargs)
        # all other historic models must be updated
        return result

    @list_route(methods=['get'])
    def getProfileByUserID(self, request, *args, **kwargs):
        profile = Profile.objects.get(userID=int(request.query_params['q']))
        prof = ProfileSerializer(instance=profile).data
        prof.pop("extra")
        return Response(prof)

    @list_route(methods=['get'])
    def getProfileByRequest(self, request, *args, **kwargs):
        profile = Profile.objects.get(userID=request.user.id)
        prof = ProfileSerializer(instance=profile).data
        return Response(prof)

    @list_route(methods=['get'])
    def getProfileAvatarByPositionID(self, request, *args, **kwargs):
        positionInstance = PositionsDocument.objects.filter(positionID=int(request.query_params['q'])).order_by(
            "-id").first()
        profile = Profile.objects.get(userID=positionInstance.userID)
        prof = ProfileSerializer(instance=profile).data
        userAvatar = profile.extra['profileAvatar']['url']

        imageAvatarName = userAvatar.split("=")[1]
        return FileUploadViewSet().getImage(imageAvatarName)

    @list_route(methods=['get'])
    def getCurrentProfileInPositionDoc(self, request, *args, **kwargs):
        positionDoc = PositionsDocument.objects.get(
            userID=request.user.id,
            companyID=request.user.current_company_id,
        )
        return Response(positionDoc.desc)

    @list_route(methods=['post'])
    def UpdateProfilePicAndCompanyPic(self, request, *args, **kwargs):
        profileInstance = self.queryset.get(userID=request.user.id)
        profileInstance.update(set__extra__profileAvatar__url=request.data['avatar'])

        companyProfile = CompanyProfile.objects.get(
            companyID=request.user.current_company_id,
            creatorUserID=request.user.id
        )

        companyProfile.update(set__extra__logo=request.data['companyLogo'])

        return Response({"result": "ok"})

    @list_route(methods=['post'])
    def FinishWelcome(self, request, *args, **kwargs):
        profileInstance = self.queryset.get(userID=request.user.id)
        profileInstance.update(set__extra__heIsAdminOfThisSubdomainAndFirstLogin=False)
        profileInstance.update(set__extra__heIsUserOfThisSubdomainAndFirstLogin=False)

        # creating new hamkari ads
        companyProfile = CompanyProfile.objects.get(
            companyID=request.user.current_company_id,
            creatorUserID=request.user.id
        )
        data = {}
        data["userID"] = profileInstance.userID
        data["startDate"] = datetime.now()
        data["endDate"] = datetime.now() + timedelta(days=600)
        data["title"] = "همکاری با ما"
        data["exp"] = "عضویت گیری در سامانه"
        data["publish"] = True
        hamkariSerial = HamkariSerializer(data=data)
        hamkariSerial.is_valid(raise_exception=True)
        hamkariInstance = hamkariSerial.save()

        data = {}
        data["hamkariID"] = hamkariInstance.id
        data["name"] = "با ما همکار شوید"
        data["exp"] = "چنانچه خواهان همکاری با ما هستیپ بروی دکمه ی ثبت نام کلیک کنید"
        data["publish"] = True
        data["positionID"] = GetPositionViewset().GetCurrentPositionDocumentInstance(request).positionID
        hamkariJobSerial = HamkariJobsSerializer(data=data)
        hamkariJobSerial.is_valid(raise_exception=True)
        hamkariJobInstance = hamkariJobSerial.save()

        return Response({"result": "ok"})

    @list_route(methods=['post'])
    def UpdateCompNameAndU(self, request, *args, **kwargs):

        companyProfile = CompanyProfile.objects.get(
            companyID=request.user.current_company_id,
            creatorUserID=request.user.id
        )

        extra = companyProfile.extra
        extra["name"] = request.data["name"]
        extra["introduction"] = request.data["intro"]

        cs = CompanyProfileSerializer(instance=companyProfile, partial=True, data={"extra": extra})
        cs.is_valid(raise_exception=True)
        cs.save()

        return Response({"result": "ok"})

    @list_route(methods=['get'])
    def SearchProfiles(self, request, *args, **kwargs):
        self.queryset = QuerySetFilter().filter(
            querySet=Profile.objects,
            kwargs=self.request.query_params
        )

        # queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(self.queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            jsonresult = serializer.data
            jsonresult = [
                {
                    "id": i["id"],
                    "Name": i["extra"]["Name"],
                    "AboutDetail": i["extra"]["AboutMe"]["detail"],
                    "AboutTitle": i["extra"]["AboutMe"]["title"],
                    "AvatarUrl": i["extra"]["profileAvatar"]["url"],
                }

                for i in jsonresult]
        return self.get_paginated_response(jsonresult)

    # @detail_route(methods=['get'])
    # def SearchProfiles(self,request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())

    @list_route(methods=["get"])
    def getIfFirstLogin(self, request):
        profileInstance = self.queryset.get(userID=request.user.id)
        result = 0
        if "heIsAdminOfThisSubdomainAndFirstLogin" in profileInstance.extra:
            result = 1 if profileInstance.extra["heIsAdminOfThisSubdomainAndFirstLogin"] else 0

        if result == 0:
            if "heIsUserOfThisSubdomainAndFirstLogin" in profileInstance.extra:
                result = 2 if profileInstance.extra["heIsUserOfThisSubdomainAndFirstLogin"] else 0

        return Response({"result": 0})

    @list_route(methods=["post"])
    def saveProfileFromCropper(self, request, *args, **kwargs):
        data = request.data.get("avatar")
        if not data:
            raise Exception("لطفا عکس را برش دهید")
        data = data.split(";")

        img = data[1].split(",")[1]
        hash = data[1].split(",")[0]
        imgType = data[0].split(":")[1].split("/")[1]

        imgdata = base64.b64decode(img)
        fileName = "myProfile." + imgType

        guid = uuid.uuid4().hex

        pathJoin = os.path.join(tempfile.gettempdir(), guid + fileName)
        with open(pathJoin, 'wb') as f:
            f.write(imgdata)

        result = FileUploadViewSet().saveImgToDB(request.user.id, fileName, pathJoin, "")

        profileInstance = self.queryset.get(userID=request.user.id)

        extra = profileInstance.extra
        extra["profileAvatar"]["url"] = '/api/v1/file/upload?q=' + result

        pfs = ProfileSerializer(instance=profileInstance, data={"extra": extra}, partial=True)

        pfs.is_valid(raise_exception=True)

        pfs.save()

        return Response({"img": result})

    @detail_route(methods=['get'])
    def GetUserInvitations(self, request, *args, **kwargs):
        if kwargs["id"] == "undefined":
            return Response({"results": []})

        senderUserProfileInstance = Profile.objects.get(userID=request.user.pk)
        recieverUserProfileInstance = Profile.objects.get(id=kwargs["id"])
        # it must shows invitations of logined user
        queryset = CompanyMembersJointRequest.objects.filter(
            receiver=recieverUserProfileInstance,
            sender=senderUserProfileInstance
        ).order_by("-dateOfPost")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CompanyMembersJointRequestSerializer(page, many=True)
            jsonResult = []
            for j in serializer.data:
                j["companyName"] = Company.objects.get(id=j["company"]).name
                j["chartName"] = Chart.objects.get(id=j["chart"]).title
                j.pop("company", None)
                j.pop("receiverName", None)
                j.pop("senderName", None)
                jsonResult.append(j)

            return self.get_paginated_response(jsonResult)

        serializer = CompanyMembersJointRequestSerializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def RemoveInvitations(self, request, *args, **kwargs):
        senderUserProfileInstance = Profile.objects.get(userID=request.user.pk)
        CompanyMembersJointRequest.objects(id=request.QUERY_PARAMS["q"],
                                           sender=str(senderUserProfileInstance.id)).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def template_view_dashboard_settings(self, request, *args, **kwargs):

        return render_to_response(
            "myProfile/DashboardSettings.html",
            {},
            context_instance=RequestContext(self.request)
        )
