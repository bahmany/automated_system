from django.conf.urls import patterns, include, url
from rest_framework_mongoengine import routers

from amspApp.BPMSystem.urls import routerTableSelectedItems
from amspApp.Bpms.views import LunchedProcessView, DoneProcessArchiveView, LunchedProcessArchiveView, MessageProcessView

router = routers.SimpleRouter()
router.register(r'LunchedProcess', LunchedProcessView.LunchedProcessViewSet, base_name='LunchedProcess')

routerLunchedArchive = routers.SimpleRouter()
routerLunchedArchive.register(r'LunchedProcessArchive', LunchedProcessArchiveView.LunchedProcessArchiveViewSet, base_name='LunchedProcessArchive')

routerDoneArchive = routers.SimpleRouter()
routerDoneArchive.register(r'DoneProcessArchive', DoneProcessArchiveView.DoneProcessArchiveViewSet, base_name='DoneProcessArchive')

routerMessageArchive = routers.SimpleRouter()
routerMessageArchive.register(r'MessageProcess', MessageProcessView.MessageProcessViewSet, base_name='MessageProcess')


urlpatterns = patterns(
    '',
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/', include(routerLunchedArchive.urls)),
    url(r'^api/v1/', include(routerDoneArchive.urls)),
    url(r'^api/v1/', include(routerMessageArchive.urls)),
    url(r'^api/v1/', include(routerTableSelectedItems.urls)),
    url(r'^page/process/inbox', LunchedProcessView.LunchedProcessViewSet.as_view({'get': 'template_view_inbox'}),
        name='template_vieew_inbox'),
    url(r'^page/process/doneArchive',
        DoneProcessArchiveView.DoneProcessArchiveViewSet.as_view({'get': 'template_view'}),
        name='template_view_mexy_process'),
    url(r'^page/process/lunchedArchive',
        LunchedProcessArchiveView.LunchedProcessArchiveViewSet.as_view({'get': 'template_view'}),
        name='template_view_mey_process'),
    url(r'^page/process/trackLunchedProcess',
        LunchedProcessView.LunchedProcessViewSet.as_view({'get': 'template_view_track_lunched_process'}),
        name='template_view_track_lunched_process'),
    url(r'^page/process/trackDoneProcess',
        LunchedProcessView.LunchedProcessViewSet.as_view({'get': 'template_view_track_done_process'}),
        name='template_view_track_done_process'),
    url(r'^page/process/do', LunchedProcessView.LunchedProcessViewSet.as_view({'get': 'template_view_do_process'}),
        name='template_view_do_process'),
    url(r'^page/process/seeMessage', MessageProcessView.MessageProcessViewSet.as_view({'get': 'template_view_do_message_process'}),
        name='template_view_do_message_process'),
    url(r'^page/process/message', MessageProcessView.MessageProcessViewSet.as_view({'get': 'template_view_message_process'}),
        name='template_view_message_process'),


)
