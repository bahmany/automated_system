from django.conf.urls import patterns, url, include
from rest_framework.routers import SimpleRouter

from amspApp.Edari.hz.pageLoader import PageLoaderApi
from amspApp.Edari.hz.views.HZViewSet import HZViewSet

nn = SimpleRouter()
nn.register("hz", HZViewSet, base_name="notify")

urlpatterns = patterns(
    '',
    url(r'^api/v1/', include(nn.urls)),
    url(r'^page/hz', PageLoaderApi.as_view({"get": "template_base"})),

)

