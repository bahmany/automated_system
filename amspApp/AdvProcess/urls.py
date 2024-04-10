from django.conf.urls import patterns, url

from amsp import settings
from amspApp.AdvProcess.proxyier import myProxyView
from amspApp.AdvProcess.views.AdvProcessViews import AdvProcessViewSetTempl

urlpatterns = \
    patterns('',
             url(r'^page/advProcess', AdvProcessViewSetTempl.as_view({"get": "template_view"})),
             # url(r'^activiti-app/.', AdvProcessViewSet.as_view()),
             # url(r'^app/(?P<url>.*)$', HttpProxy.as_view(base_url='http://localhost:8080/activiti-app')),
             url(r'^odoo/(?P<url>.*)$',myProxyView.as_view(base_url=settings.ODOO_HTTP_REFERER)),
             # url(r'^activiti-app/(?P<path>.*)$',RevProxyView.as_view()),

             )
