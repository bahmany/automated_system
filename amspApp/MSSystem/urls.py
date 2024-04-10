from django.conf.urls import patterns, include, url
from rest_framework_mongoengine import routers
from amspApp.MSSystem.views import MStatisticsTemplateView
from amspApp.MSSystem.views import MStatisticsDataView


router = routers.SimpleRouter()
router2 = routers.SimpleRouter()
router.register(r'statistics', MStatisticsTemplateView.MStatisticsTemplateViewSet, base_name='MStatisticsTemplateViewSet')
router2.register(r'dataForMS', MStatisticsDataView.MStatisticsDataViewSet, base_name='MStatisticsDataViewSet')


urlpatterns = patterns(
    '',
    # ... URLs
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/', include(router2.urls)),

    url(r'^page/statisticsBase', MStatisticsTemplateView.MStatisticsTemplateViewSet.as_view({'get': 'template_view_statistics_base'}),
        name='template_vieew_inbox'),
    url(r'^page/statistics/new', MStatisticsTemplateView.MStatisticsTemplateViewSet.as_view({'get': 'template_view_statistics_new'}),
        name='template_view_new_inbox'),
    url(r'^page/statistics/edit', MStatisticsTemplateView.MStatisticsTemplateViewSet.as_view({'get': 'template_view_statistics_edit'}),
        name='template_view_edit_inbox'),

    url(r'^page/statistics/share', MStatisticsTemplateView.MStatisticsTemplateViewSet.as_view({'get': 'template_view_statistics_share'}),
        name='template_view_statistics_share'),

    url(r'^page/statistics/publish', MStatisticsTemplateView.MStatisticsTemplateViewSet.as_view({'get': 'template_view_statistics_publish'}),
        name='publishhhhh'),

    url(r'^page/statistics/data', MStatisticsDataView.MStatisticsDataViewSet.as_view({'get': 'template_view_statistics_data'}),
        name='template_view_data_inbox'),

)
