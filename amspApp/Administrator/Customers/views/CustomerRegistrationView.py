from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from amspApp.Administrator.Customers.models import Billing_Customer, UserCustomer
from amspApp.Administrator.Customers.serializers.CustomersSerializer import CustomerSerializer
from amspApp.Administrator.permission.IsSuperUser import IsSuper
from amspApp.MyProfile.models import Profile
from amspApp._Share.ListPagination import ListPagination
from amspApp.amspUser.models import MyUser
from amspApp.amspUser.serializers.UserSerializer import UserSerializer

__author__ = 'mohammad'


class CustomerRegistrationViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = Billing_Customer.objects.all().order_by("-id")
    serializer_class = CustomerSerializer
    pagination_class = ListPagination
    permission_classes = (IsSuper,)

    def create(self, request, *args, **kwargs):
        request.data["userID"] = request.user.id
        if request.data["userID"] == None:
            raise Exception("Please login")

        """
        checkig if username and email does not exits
        """
        userCount = MyUser.objects.filter(username=request.data['username']).count()
        emailCount = MyUser.objects.filter(username=request.data['customerEmail']).count()

        if userCount > 0 or emailCount > 0:
            return Response({
                'status': 'Not Acceptable',
                'message': [{"fieldName": "ایمیل یا نام کاربری",
                             "message": "این ایمیل قبلا در سیستم ثبت نام کرده است - در صورت فراموشی رمز عبور دکمه ی فراموشی رمز عبور را انتخاب نمایید"}],
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

        resultCreate = super(CustomerRegistrationViewSet, self).create(request, *args, **kwargs)

        # creating user :
        dt = {}
        dt["name"] = request.data["customerName"].split(" ")[0]
        dt["family"] = request.data["customerName"].split(" ")[1] if len(
            request.data["customerName"].split(" ")) > 1 else request.data["customerName"]
        dt["username"] = request.data['username']
        dt["password"] = request.data['password']
        dt["confirm_password"] = request.data['password']
        dt["email"] = request.data['customerEmail']

        serializer = UserSerializer(data=dt)

        serializer.is_valid(raise_exception=True)

        # if serializer.is_valid():
        result = serializer.create(serializer.validated_data)
        CustomerRegistrationViewSet().addUserToCustomer(result.id,
                                                        resultCreate.data["id"])
        user = authenticate(username=dt["username"], password=dt["password"])
        # login(request, user)
        profileInstance = Profile.objects.get(userID=user.id)
        profileInstance.update(set__extra__isAllowed=True)
        profileInstance.update(set__extra__heIsAdminOfThisSubdomainAndFirstLogin=True)
        profileInstance.update(set__extra__Name=dt["name"] + " " + dt["family"])
        profileInstance.update(set__extra__job__Shenasnameh__Name=dt["name"])
        profileInstance.update(set__extra__job__Shenasnameh__Family=dt["family"])

        # return Response({})
        return resultCreate

    def GetCustomerIDFromBilling(self, request):
        domainName = ""
        host = request._request.META["HTTP_HOST"]
        if host == "127.0.0.1:8001":
            domainName = "****"

        if host == "app.****.ir":
            domainName = "****"
        if host == "192":
            domainName = "****"
        if host == "192.168.0.142":
            domainName = "****"

        if host == "127.0.0.1:8000":
            domainName = "****"

        if host == "127.0.0.1:8001":
            domainName = "****"

        if host[0:3] == "192":
            domainName = "****"

        if host[0:1].isdigit():
            domainName = "****"

        if host.find("app") != -1:
            domainName = "****"

        if host.find("local") != -1:
            domainName = "****"

        if domainName == "":
            domainName = host.split(".")[0]

        domainName = "****"
        customer = self.queryset.filter(subdomainName=domainName)

        if customer.count() != 1:
            raise Exception("Invalid domain name " + domainName)
        # print("GetCustomerIDFromBilling end")
        return customer[0].id

    def GetUserInstanceFromBilling(self, request):
        # print("GetUserInstanceFromBilling start")

        result = self.GetCustomerInstanceFromBilling(request)
        us = MyUser.objects.get(username=result.username)
        # print("GetUserInstanceFromBilling end")

        return us

    def GetCustomerInstanceFromBilling(self, request):
        # print("GetCustomerInstanceFromBilling start")

        domainName = ""
        host = request._request.META["HTTP_HOST"]
        # print(host)
        if host == "127.0.0.1:8001":
            domainName = "****"

        if host == "app.****.ir":
            domainName = "****"

        if host == "app.****.com":
            domainName = "****"

        if host == "****.com":
            domainName = "****"

        if host == "192.168.0.142":
            domainName = "****"

        if host == "192":
            domainName = "****"

        if host[0:3] == "192":
            domainName = "****"

        if host == "127.0.0.1:8001":
            domainName = "****"

        if host[0:1].isdigit():
            domainName = "****"

        if host == "127.0.0.1:8000":
            domainName = "****"

        if domainName == "":
            domainName = host.split(".")[0]

        domainName = "****"

        customer = Billing_Customer.objects.filter(subdomainName=domainName)

        if customer.count() != 1:
            raise Exception("Invalid domain name " + domainName + " " + str(customer.count()))
        # print("GetCustomerInstanceFromBilling end")

        return customer[0]

    def GetCustomerInstanceFromBilling_WSGI(self, request, host):
        # print("GetCustomerInstanceFromBilling start")

        domainName = ""
        # print(host)
        if host == "127.0.0.1:8001":
            domainName = "****"

        if host[0:1].isdigit():
            domainName = "****"

        if host == "app.****.ir":
            domainName = "****"

        if host == "****.135.133":
            domainName = "****"
        if host == "192":
            domainName = "****"
        if host == "127.0.0.1:8001":
            domainName = "****"

        if host == "127.0.0.1:8000":
            domainName = "****"

        if host == "127.0.0.1:8000":
            domainName = "****"

        if host[0:3] == "192":
            domainName = "****"

        if host == "192.168.0.142":
            domainName = "****"

        if host == "app.****.com":
            domainName = "****"

        if host.find("app") != -1:
            domainName = "****"

        if host.find("local") != -1:
            domainName = "****"

        if domainName == "":
            domainName = host.split(".")[0]

        domainName = "****"
        customer = self.queryset.filter(subdomainName=domainName)

        # if customer.count() != 1:
        #     raise Exception("Invalid domain name " + domainName)
        # # print("GetCustomerInstanceFromBilling end")

        return customer

    def addUserToCustomer(self, userID, customerID):
        try:
            UserCustomer(
                userID=userID,
                customerID=customerID
            ).save()
        except:
            pass

    def getCustomerIDFromUserID(self, userid):
        res = UserCustomer.objects.filter(userID=userid)
        if res.count() == 0:
            raise Exception("There is no UserCustomer for userID :" + userid)
        return res[0]
