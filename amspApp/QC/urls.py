from django.conf.urls import patterns, include, url
from rest_framework.routers import SimpleRouter

from amspApp.QC.views.QCAuditShedualsViews import QCqcScheduleViewSet
from amspApp.QC.views.QCFindingViews import QCFindingViewSet
from amspApp.QC.views.QCViews import QCViewSet

qc_router = SimpleRouter()
qc_router.register("qc", QCViewSet, base_name="qc-list")

qcfinding_router = SimpleRouter()
qcfinding_router.register("qcfinding", QCFindingViewSet, base_name="qc-list")

qcschedule_router = SimpleRouter()
qcschedule_router.register("qcschedule", QCqcScheduleViewSet, base_name="qc-list")

urlpatterns = patterns('',

                       url(r'^page/qcfindingopen', QCFindingViewSet.as_view({"get": "template_view_open"})),
                       url(r'^page/qcfindingpost', QCFindingViewSet.as_view({"get": "template_view_post_read"})),
                       url(r'^page/qcfindinglist', QCFindingViewSet.as_view({"get": "template_view_list_read"})),
                       url(r'^page/qcfinding', QCFindingViewSet.as_view({"get": "template_view_read"})),
                       url(r'^page/qcmanual', QCFindingViewSet.as_view({"get": "template_qcmanual"})),
                       url(r'^page/qcschedule', QCqcScheduleViewSet.as_view({"get": "template_view_read"})),
                       url(r'^page/qc', QCViewSet.as_view({"get": "template_view_read"})),
                       url(r'^api/v1/', include(qcfinding_router.urls)),
                       url(r'^api/v1/', include(qc_router.urls)),
                       url(r'^api/v1/', include(qcschedule_router.urls)),
                       )
