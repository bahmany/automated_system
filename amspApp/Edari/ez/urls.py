from django.conf.urls import patterns, url, include
from rest_framework.routers import SimpleRouter

from amspApp.Edari.ez.pageLoader import PageLoaderApi
from amspApp.Edari.ez.views.EZViewSet import EZViewSet


nn = SimpleRouter()
nn.register("ez", EZViewSet, base_name="notify")


urlpatterns = patterns(
    '',
    url(r'^api/v1/', include(nn.urls)),
    url(r'^page/ez-item', PageLoaderApi.as_view({"get": "template_base_ez_item"})),
    url(r'^page/ez-list', PageLoaderApi.as_view({"get": "template_base_ez_list"})),
    url(r'^page/ez-report', PageLoaderApi.as_view({"get": "template_base_ez_report"})),
    url(r'^page/ez', PageLoaderApi.as_view({"get": "template_base"})),

)

