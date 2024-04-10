from django.conf.urls import patterns, include, url
from rest_framework_mongoengine import routers
from amspApp.BPMSystem.BPMReport.views import ReportsView


router = routers.SimpleRouter()
router.register(r'reports', ReportsView.ReportsViewSet, base_name='ReportsViewSet')

urlpatterns = patterns(
    '',
    # ... URLs
    url(r'^api/v1/', include(router.urls)),
    url(r'^page/process/reports', ReportsView.ReportsViewSet.as_view({'get': 'template_view_reports_base'})),
    url(r'^page/process/search', ReportsView.ReportsViewSet.as_view({'get': 'template_view_search_base'}),
        name='template_views'),
)
