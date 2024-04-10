from django.conf.urls import patterns, include, url
from rest_framework_mongoengine import routers

from amspApp.BI.DataTables.viewer.DataTableValuesViews import DataTableValuesViewSet
from amspApp.BI.DataTables.viewer.DataTableViews import DataTableViewSet

router = routers.SimpleRouter()
router.register(r'datatable', DataTableViewSet, base_name='MStatisticsTemplateViewSet')
router.register(r'datatablevalues', DataTableValuesViewSet, base_name='MStatisticsTemplateViewSet')


urlpatterns = patterns(
    '',
    # ... URLs
    url(r'^api/v1/', include(router.urls)),

    url(r'^page/datatables/script', DataTableViewSet.as_view({'get': 'template_view_script'}),name='template_vieew_inbox'),
    url(r'^page/datatables/value', DataTableViewSet.as_view({'get': 'template_view_value'}),name='template_vieew_inbox'),
    url(r'^page/datatables/share', DataTableViewSet.as_view({'get': 'template_view_share'}),name='template_vieew_inbox'),
    url(r'^page/datatables/new', DataTableViewSet.as_view({'get': 'template_view_edit'}),name='template_vieew_inbox'),
    url(r'^page/datatables', DataTableViewSet.as_view({'get': 'template_view'}),name='template_vieew_inbox'))

