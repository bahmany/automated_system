from django.conf.urls import patterns, include, url
from rest_framework.routers import SimpleRouter

from amspApp.Virtual.Registration.views.ForgetPassView import ForgetPassView
from amspApp.Virtual.Registration.views.JobsView import JobsViewSet
from amspApp.Virtual.Registration.views.LoginView import LoginViewSet
from amspApp.Virtual.pageLoader import PageLoaderApi



login_router = SimpleRouter()
login_router.register(r"login", LoginViewSet, base_name="secretariat-details")

jobs_router = SimpleRouter()
jobs_router.register(r"jobs", JobsViewSet, base_name="jobs-details")

routerForget = SimpleRouter()
routerForget.register(r'forgetpass', ForgetPassView, base_name="ForgetPassword")



urlpatterns = patterns(
    '',
    # page loaders

    # ------------------------------

    url(r'^page/base', PageLoaderApi.as_view({"get": "base"})),
    url(r'^page/login', PageLoaderApi.as_view({"get": "login"})),
    url(r'^page/forget', PageLoaderApi.as_view({"get": "forget"})),
    url(r'^page/reset', PageLoaderApi.as_view({"get": "reset"})),
    url(r'^page/register', PageLoaderApi.as_view({"get": "register"})),
    url(r'^page/home', PageLoaderApi.as_view({"get": "home"})),
    url(r'^page/profile', PageLoaderApi.as_view({"get": "profile"})),
    url(r'^page/introduction', PageLoaderApi.as_view({"get": "introduction"})),
    url(r'^page/hamkariDetailsItemModal', PageLoaderApi.as_view({"get": "hamkariDetailsItemModal"})),
    url(r'^page/hamkariDetails', PageLoaderApi.as_view({"get": "hamkariDetails"})),
    url(r'^page/goodsSupplay', PageLoaderApi.as_view({"get": "goodsSupplay"})),

    url(r'^page/step10', PageLoaderApi.as_view({"get": "selectJob"})),
    url(r'^page/step11', PageLoaderApi.as_view({"get": "resultJob"})),
    url(r'^page/step1', PageLoaderApi.as_view({"get": "step1"})),
    url(r'^page/step2', PageLoaderApi.as_view({"get": "step2"})),
    url(r'^page/step3', PageLoaderApi.as_view({"get": "step3"})),
    url(r'^page/step4', PageLoaderApi.as_view({"get": "step4"})),
    url(r'^page/step5', PageLoaderApi.as_view({"get": "step5"})),
    url(r'^page/step6', PageLoaderApi.as_view({"get": "step6"})),
    url(r'^page/step7', PageLoaderApi.as_view({"get": "step7"})),
    url(r'^page/step8', PageLoaderApi.as_view({"get": "step8"})),
    url(r'^page/step9', PageLoaderApi.as_view({"get": "preview"})),

    # url(r'^page/profile', PageLoaderApi.as_view({"get":"get_base"})),
    # url(r'^page/register', PageLoaderApi.as_view({"get":"get_base"})),
    # url(r'^page/forget', PageLoaderApi.as_view({"get":"get_base"})),

    # url(r'^api/v1/register-to-hire/', RegistryToHireApiViewSet.as_view()),
    url(r'^api/v1/', include(login_router.urls)),
    url(r'^api/v1/', include(jobs_router.urls)),
    url(r'^api/v1/', include(routerForget.urls)),

    url('', PageLoaderApi.as_view({"get": "index"})),
)
