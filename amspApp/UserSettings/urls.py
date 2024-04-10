from django.conf.urls import patterns, url, include
from rest_framework.routers import SimpleRouter
from amspApp.UserSettings.Views.AccessToSecratariatView import AccessToSecratariatViewSet
from amspApp.UserSettings.Views.ChangeView import ChangeViewSet
from amspApp.UserSettings.Views.UserSettingsView import UserSettingsViewSet

__author__ = 'mohammad'

sec_router = SimpleRouter()
sec_router.register(r'secratariat', AccessToSecratariatViewSet, base_name="AccessToSec")

change_router = SimpleRouter()
change_router.register(r'change', ChangeViewSet, base_name="AccessToChange")

urlpatterns = patterns(


    '',


    url(r'^api/v1/settings/', include(sec_router.urls)),
    url(r'^api/v1/settings/', include(change_router.urls)),


    url('page/settings/AccessToSecratariat', AccessToSecratariatViewSet.as_view({"get": "template_view"})),
    url('page/settings/Change', ChangeViewSet.as_view({"get": "template_view"})),
    url('page/settings', UserSettingsViewSet.as_view({"get": "template_view"})),


)