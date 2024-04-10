from django.conf.urls import patterns, url, include
from rest_framework.routers import SimpleRouter

from amspApp.Edari.Morekhasi.views.MorekhasiRoozanehViews import MorekhasiRoozanehiViewSet
from amspApp.Edari.Morekhasi.views.MorekhasiSaatiViews import MorekhasiSaatiViewSet

mc = SimpleRouter()
mc.register("morekhasi_saati", MorekhasiSaatiViewSet, base_name="notify")

urlpatterns = patterns(
    '',

    url(r'^page/morekhasisaatiBase', MorekhasiSaatiViewSet.as_view({"get": "template_base"})),
    url(r'^page/morekhasisaatiAdd', MorekhasiSaatiViewSet.as_view({"get": "template_add"})),
    url(r'^page/morekhasisaatiList', MorekhasiSaatiViewSet.as_view({"get": "template_list"})),
    url(r'^page/morekhasisaatiMyMorekhasi', MorekhasiSaatiViewSet.as_view({"get": "template_MyMorekhasi"})),
    url(r'^page/morekhasisaatiEzamat', MorekhasiSaatiViewSet.as_view({"get": "template_MorekhasisaatiEzamat"})),
    url(r'^page/morekhasisaatiEdari', MorekhasiSaatiViewSet.as_view({"get": "template_MorekhasisaatiEdari"})),
    url(r'^page/morekhasiroozanehRoozanehBase', MorekhasiRoozanehiViewSet.as_view({"get": "template_base"})),

    url(r'^api/v1/', include(mc.urls)),


)
