from django.conf.urls import patterns, url, include
from rest_framework.routers import SimpleRouter




# nn = SimpleRouter()
# nn.register("ez", EZViewSet, base_name="notify")
from amspApp.Fees.pageLoader import PageLoaderApi

urlpatterns = patterns(
    '',

    url(r'^page/fees', PageLoaderApi.as_view({"get": "template_base"})),

)

