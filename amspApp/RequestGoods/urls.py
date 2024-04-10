from django.conf.urls import patterns, url, include
from rest_framework.routers import SimpleRouter

from amspApp.RequestGoods.pageLoader import RGPageLoaderApi
from amspApp.RequestGoods.views.rgView import RequestGoodViewSet

nn = SimpleRouter()
nn.register("rg", RequestGoodViewSet, base_name="notify")

urlpatterns = patterns(

    '',
    url(r'^api/v1/', include(nn.urls)),
    url(r'^page/rgShowSignBodyPrc/', RGPageLoaderApi.as_view({"get": "template_view_showSignBodyPrc"})),

    url(r'^page/RGIndex', RGPageLoaderApi.as_view({"get": "index"})),
    url(r'^page/talkToAnbar', RGPageLoaderApi.as_view({"get": "talkToAnbar"})),
    url(r'^page/RGItem', RGPageLoaderApi.as_view({"get": "RGItem"})),
    url(r'^page/helpRG', RGPageLoaderApi.as_view({"get": "helpRG"})),
    url(r'^page/RGgoods', RGPageLoaderApi.as_view({"get": "RGgoods"})),

)
