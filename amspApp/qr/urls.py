from django.conf.urls import patterns, url, include
from rest_framework.routers import SimpleRouter



# qr_router = SimpleRouter()
# qr_router.register("qr", QrViewSet, base_name="news-list")
from amspApp.qr.views.QrView import qr_template_view

urlpatterns = patterns('',
                       # url(r'^api/v1/', include(qr_router.urls)),
                       url(r"(?P<ID>)/", qr_template_view),
                       )
