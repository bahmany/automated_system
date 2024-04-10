from django.conf.urls import patterns, url

from amspApp.net.pageLoader import PageLoaderApi

urlpatterns = patterns(
    '',
    url(r'^page/net', PageLoaderApi.as_view({"get": "template_base"})),

)

