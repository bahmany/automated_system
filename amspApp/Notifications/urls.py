from django.conf.urls import patterns, url, include
from rest_framework.routers import SimpleRouter

from amspApp.Notifications.views.GoogleTokenView import GoogleTokenViewSet
from amspApp.Notifications.views.NotificationView import NotificationViewSet

nn = SimpleRouter()
nn.register("notify", NotificationViewSet, base_name="notify")

gn = SimpleRouter()
gn.register("tokens", GoogleTokenViewSet, base_name="notify")

urlpatterns = patterns(
    '',
    url(r'^api/v1/', include(nn.urls)),
    url(r'^api/v1/', include(gn.urls)),

)
