from django.conf.urls import patterns, url

from amspApp.DMS.views import DMSViewSet

urlpatterns = patterns('',
                       url(r'^page/dmsBase', DMSViewSet.as_view({'get': 'dmsBase'})), )
