from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets
from amspApp.Administrator.Customers.views.CustomerRegistrationView import CustomerRegistrationViewSet
from amspApp.CompaniesManagment.Charts.models import Chart
from amspApp.CompaniesManagment.Positions.models import Position
from amspApp.CompaniesManagment.Positions.serializers.PositionSerializer import PositionSerializer
from amspApp.CompaniesManagment.members.serializers.MemberSerializer import MembersSerializer
from amspApp.CompaniesManagment.models import CompanyMembersJointRequest, Company
from amspApp.CompaniesManagment.serializers.CompanyMembersJointRequestSerializers import \
    CompanyMembersJointRequestSerializer
from amspApp.MyProfile.models import Profile
from amspApp.MyProfile.serializers.ProfileSerializer import ProfileSerializer
from amspApp._Share.ListPagination import ListPagination
from amspApp.amspUser.models import MyUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

__author__ = 'mohammad'


class CompanyMembersJointRequestViewset(viewsets.ModelViewSet):
    lookup_field = "id"
    # currentUsername = None
    queryset = CompanyMembersJointRequest.objects.all()
    serializer_class = CompanyMembersJointRequestSerializer
    pagination_class = ListPagination

    @list_route(methods=['post'])
    def suspend(self, request, *args, **kwargs):
        self = self
        pass

    """
    there is two types of invitation accept

    1: is to approve invitation by CEO
    2: approve invitation by reciever

    """

    @list_route(methods=['post'])
    def DoInvite(self, request, *args, **kwargs):
        # =================================================================================
        # we need to check billing completely
        # from paymanet i have to get payment amount and date of pay
        # from billingStrategy i have to get every thing
        # getting billing properties
        subdomainInstance = CustomerRegistrationViewSet().GetCustomerInstanceFromBilling(request)
        latestPayment = subdomainInstance.billing_payments_set.all().order_by("-id")
        # billing disabled for enterprise purposes
        # 961114
        if latestPayment.count() == 0:
            pass
            # raise Exception("This subdomain does not have any paymanet")
        latestPayment = latestPayment[0]
        billingStrategy = latestPayment.billingStrategyLink
        finishingDate = latestPayment.dateOfPost + timedelta(days=billingStrategy.days)

        # billing disabled for enterprise purposes
        # 961114
        if finishingDate < timezone.now():
            pass
            # raise Exception("This subdomain payment has been expired please recharge to continue")
            # raise Exception("This subdomain payment has been expired please recharge to continue")

        # getting all position counts in all companies
        user = MyUser.objects.get(username=subdomainInstance.username)
        companies = Company.objects.all().filter(owner_user=user.id)
        positionsCount = Position.objects.filter(company__in=companies).values_list("chart_id").distinct().count()

        # some time it raise divistion by zero because of billing strategy
        divOfPersons = int(latestPayment.loadedPrice / billingStrategy.CostPerUser)

        # billing disabled for enterprise purposes
        # 961114
        if positionsCount >= divOfPersons:
            pass
            # raise Exception("You requested positions more than your charge, please recharge to continue (%s of %s )" % (
            # divOfPersons, positionsCount))

        # =================================================================================
        # =================================================================================
        # =================================================================================
        # =================================================================================
        # =================================================================================

        currentUserInstance = request.user
        # checking if current is user is CEO or reciever
        invitationInstance = self.queryset.get(id=request.data['invitationID'])
        chartInstance = Chart.objects.get(id=invitationInstance.chart)
        companyInstance = Company.objects.get(id=invitationInstance.company)
        recieverProfileInstance = invitationInstance.receiver
        senderProfileInstance = invitationInstance.sender
        recieverUserInstance = MyUser.objects.get(id=recieverProfileInstance.userID)
        senderUserInstance = MyUser.objects.get(id=senderProfileInstance.userID)

        isCurrentUserApproveAsReciever = recieverUserInstance == currentUserInstance
        isCurrentUserApproveAsCEO = senderUserInstance == currentUserInstance

        if not isCurrentUserApproveAsCEO and not isCurrentUserApproveAsReciever:
            return Response({"message": _("You are not allowed to perform this operation")},
                            status=status.HTTP_401_UNAUTHORIZED)

        # partial update is here
        # it means we have to update an position
        # if "emptyPositionID" in request.data:
        #     if request.data["emptyPositionID"]:
        #         positionInstance
        if invitationInstance.isEmpty:
            positionInstance = Position.objects.get(id=invitationInstance.positionID)
            updated = {
                "user": recieverUserInstance.id,
                "post_date": datetime.now()
            }

            posSerializer = MembersSerializer(instance=positionInstance, data=updated, partial=True)
            posSerializer.is_valid(raise_exception=True)
            posSerializer.update(instance=positionInstance, validated_data=posSerializer.validated_data)
            invitationInstance.delete()
            # updating profile Name
            profileInstance = Profile.objects.get(userID=recieverUserInstance.id)

            profileName = ""
            if "job" in profileInstance.extra:
                if "Shenasnameh" in profileInstance.extra["job"]:
                    if "Name" in profileInstance.extra["job"]["Shenasnameh"]:
                        if "Family" in profileInstance.extra["job"]["Shenasnameh"]:
                            profileName = profileInstance.extra["job"]["Shenasnameh"]["Name"] + " " + \
                                          profileInstance.extra["job"]["Shenasnameh"]["Family"]

            profileInstance.update(set__extra__Name=profileName)
            profileInstance.update(set__extra__isAllowed=True)
            # extra = profileInstance.extra
            # profSerial = ProfileSerializer(instance=profileInstance, data={"extra": {}}, partial=True)
            # profSerial.is_valid(raise_exception=True)
            # profileInstance = profSerial.update(instance=profileInstance, validated_data={"extra": {}})
            # profSerial2 = ProfileSerializer(instance=profileInstance, data={"extra": extra}, partial=True)
            # profSerial2.is_valid(raise_exception=True)
            # ProfileSerializer.update(instance=profileInstance, validated_data={"extra": extra})

            return Response({}, status=status.HTTP_200_OK)

        newMember = {
            "company": companyInstance.id,
            "chart": chartInstance.id,
            "user": recieverUserInstance.id
        }
        # userinstance
        selectedUserInstance = MyUser.objects.get(id=newMember.get('user', None))
        selectedUserInstance.current_company_id = 700
        selectedUserInstance.save()

        # creating new position with new inboxes
        posSerializer = MembersSerializer(data=newMember)
        posSerializer.is_valid(raise_exception=True)
        posSerializer.create(posSerializer.validated_data)
        invitationInstance.delete()
        # updating profile Name
        profileInstance = Profile.objects.get(userID=recieverUserInstance.id)

        profileName = ""
        if "job" in profileInstance.extra:
            if "Shenasnameh" in profileInstance.extra["job"]:
                if "Name" in profileInstance.extra["job"]["Shenasnameh"]:
                    if "Family" in profileInstance.extra["job"]["Shenasnameh"]:
                        profileName = profileInstance.extra["job"]["Shenasnameh"]["Name"] + " " + \
                                      profileInstance.extra["job"]["Shenasnameh"]["Family"]

        profileInstance.update(set__extra__Name=profileName)

        return Response({}, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):

        # checking if for selected profile is currently active or not
        companyInstance = Company.objects.get(id=int(kwargs['companyID_id']))
        profileIntance = Profile.objects.get(id=request.data['receiver'])
        hasThisPersonActivePositionInCurrentInstance = Position.objects.filter(company=companyInstance,
                                                                               user=profileIntance.userID)

        # if hasThisPersonActivePositionInCurrentInstance.count() > 1:
        #     hasThisPersonActivePositionInCurrentInstance.order_by("-id")

        if hasThisPersonActivePositionInCurrentInstance.count() > 0:
            raise Exception(
                "این پرسنل همکنون در همین شرکت مشغول فعالیت می باشد - ابتدا آنرا تعلیق و پس از آن سمت دهی نمایید")
            # return Response(status=status.HTTP_403_FORBIDDEN, data={"msg": "این پرسنل همکنون در همین شرکت مشغول فعالیت می باشد - ابتدا آنرا تعلیق و پس از آن سمت دهی نمایید"})

        # ------------------

        CompanyMembersJointRequest.objects.filter(
            company=kwargs["companyID_id"],
            chart=request.data['chart']
        ).delete()
        if request.data["selected"] == False:
            return Response({})

        request.data["seen"] = False
        request.data["company"] = int(kwargs['companyID_id'])
        request.data["sender"] = Profile.objects.get(userID=request.user.id).id
        request.data["receiver"] = Profile.objects.get(id=request.data["receiver"]).id
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        # return super(CompanyMembersJointRequestViewset, self).create(request, *args, **kwargs)
