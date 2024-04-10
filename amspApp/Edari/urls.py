from django.conf.urls import patterns, url, include

from amspApp.Edari.pageLoader import PageLoaderApi

from amspApp.Edari.ez import urls as ezurl
from amspApp.Edari.hz import urls as hzurl
from amspApp.Edari.Morekhasi import urls as mourl




urlpatterns = patterns(
    '',

    url(r'^', include(ezurl)),
    url(r'^', include(hzurl)),
    url(r'^', include(mourl)),

    url(r'^page/edaribasepage', PageLoaderApi.as_view({"get": "template_base"})),

    url(r'^page/edariReportBase', PageLoaderApi.as_view({"get": "template_edariReportBase"})),
    url(r'^page/edariReportTaradodMahaneh', PageLoaderApi.as_view({"get": "template_edariReportTaradodMahaneh"})),
    url(r'^page/edariReportMandehMorekhasi', PageLoaderApi.as_view({"get": "template_edariReportMandehMorekhasi"})),
    url(r'^page/edariReportMorekhsiSaati', PageLoaderApi.as_view({"get": "template_edariReportMorekhsiSaati"})),
    url(r'^page/edariReportMorekhsiRoozaneh', PageLoaderApi.as_view({"get": "template_edariReportMorekhsiRoozaneh"})),
    url(r'^page/edariEmzaKonandeha', PageLoaderApi.as_view({"get": "template_edariEmzaKonandeha"})),

)
