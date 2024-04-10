from amspApp.Administrator.Customers.views.CustomerRegistrationView import CustomerRegistrationViewSet
from amspApp.amspUser.models import MyUser

__author__ = 'mohammad'


class SubdomainHandle(object):
    default_subdomain = "****"

    def process_request(self, request):
        hostname = request.META["HTTP_HOST"]
        domainName = "****"
        if (len(hostname.split(".")) == 3):
            domainName = hostname.split(".")[0]
            if domainName == "192":
                domainName = "****"

        if hostname.find("app") != -1:
            domainName = "****"
        if hostname.find("localhost") != -1:
            hostname = "****"

        reg = CustomerRegistrationViewSet().GetCustomerInstanceFromBilling_WSGI(request, hostname)
        if reg.count() == 1 or 2:
            request.subdomain = reg[0]
            request.owner_subdomain_user = MyUser.objects.get(username=reg[0].username)
        else:
            request.subdomain = None

            # print(hostname)
