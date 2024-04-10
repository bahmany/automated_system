from django.conf.urls import patterns, include, url
from rest_framework.routers import SimpleRouter
from amspApp.Administrator.Base.Views.DashboardBaseApiView import IndexApiViewSet, DashboardBaseApiViewSet
from amspApp.Administrator.Base.Views.HomepageApiView import HomepageApiViewSet
from amspApp.Administrator.Billings.views.ApiView import BillingRegisterApiViewSet, BillingBaseApiViewSet, \
    PaymentApiViewSet, PaymentBaseApiViewSet
from amspApp.Administrator.Billings.views.BillingRegistrationView import BillingRegistrationViewSet, PaymentViewSet
from amspApp.Administrator.Customers.views.ApiView import CustomersRegisterApiViewSet, CustomersBaseApiViewSet
from amspApp.Administrator.Customers.views.CustomerRegistrationView import CustomerRegistrationViewSet
from amspApp.Administrator.Languages.views.ApiView import LanguagesBaseApiViewSet, LanguagesApiViewSet
from amspApp.Administrator.Languages.views.LanguagesView import LanguagesRegistrationViewSet


url_customer_api = SimpleRouter()
url_customer_api.register(r'customer', CustomerRegistrationViewSet, base_name="companies", )

url_billing_api = SimpleRouter()
url_billing_api.register(r'billing', BillingRegistrationViewSet, base_name="companies", )

url_payment_api = SimpleRouter()
url_payment_api.register(r'payment', PaymentViewSet, base_name="companies", )

url_langs_api = SimpleRouter()
url_langs_api .register(r'languages', LanguagesRegistrationViewSet, base_name="companies", )



urlpatterns = patterns(
    '',
    url(r'^page/base', DashboardBaseApiViewSet.as_view()),
    url(r'^page/home', HomepageApiViewSet.as_view()),

    url(r'^page/customer/register', CustomersRegisterApiViewSet.as_view()),
    url(r'^page/customer', CustomersBaseApiViewSet.as_view()),

    url(r'^page/billing/payment/register', PaymentApiViewSet.as_view()),
    url(r'^page/billing/payment', PaymentBaseApiViewSet.as_view()),

    url(r'^page/languages/register', LanguagesBaseApiViewSet.as_view()),
    url(r'^page/languages', LanguagesApiViewSet.as_view()),

    url(r'^page/billing/register', BillingRegisterApiViewSet.as_view()),
    url(r'^page/billing', BillingBaseApiViewSet.as_view()),






    url(r'^api/v1/', include(url_customer_api.urls)),
    url(r'^api/v1/', include(url_billing_api.urls)),
    url(r'^api/v1/', include(url_payment_api.urls)),
    url(r'^api/v1/', include(url_langs_api.urls)),

    url('', IndexApiViewSet.as_view()),

)
