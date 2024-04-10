from django.conf.urls import patterns, include, url
from rest_framework_mongoengine import routers
from amspApp.BPMSystem.views import LunchedProcessView, DoneProcessArchiveView, LunchedProcessArchiveView, \
    MessageProcessView, BigArchiveView
from amspApp.BPMSystem.views.DataModelerViews import DataModelerViewSet
from amspApp.BPMSystem.views.SqlTableSelectedItemsView import SqlTableSelectedItemsViewSet
from amspApp.BPMSystem.views.TableSelectedItemsView import TableSelectedItemsViewSet

routerTableSelectedItems = routers.SimpleRouter()
routerTableSelectedItems.register(r'TableSelectedItems', TableSelectedItemsViewSet, base_name='MessageProcess')

routerSqlTableSelectedItems = routers.SimpleRouter()
routerSqlTableSelectedItems.register(r'SqlTableSelectedItems', SqlTableSelectedItemsViewSet, base_name='MessageProcess')

router = routers.SimpleRouter()
router.register(r'LunchedProcess', LunchedProcessView.LunchedProcessViewSet, base_name='LunchedProcess')

routerLunchedArchive = routers.SimpleRouter()
routerLunchedArchive.register(r'LunchedProcessArchive', LunchedProcessArchiveView.LunchedProcessArchiveViewSet,
                              base_name='LunchedProcessArchive')

routerDoneArchive = routers.SimpleRouter()
routerDoneArchive.register(r'DoneProcessArchive', DoneProcessArchiveView.DoneProcessArchiveViewSet,
                           base_name='DoneProcessArchive')

routerMessageArchive = routers.SimpleRouter()
routerMessageArchive.register(r'MessageProcess', MessageProcessView.MessageProcessViewSet, base_name='MessageProcess')

routerBigArchive = routers.SimpleRouter()
routerBigArchive.register(r'bpms-archive', BigArchiveView.BigArchiveViewSet, base_name='bpmsArchive')

routerDataModel = routers.SimpleRouter()
routerDataModel.register(r'datamodelmngr', DataModelerViewSet, base_name='bpmsArchive')

urlpatterns = patterns(
    '',
    # ... URLs

    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/', include(routerLunchedArchive.urls)),
    url(r'^api/v1/', include(routerDoneArchive.urls)),
    url(r'^api/v1/', include(routerMessageArchive.urls)),
    url(r'^api/v1/', include(routerBigArchive.urls)),
    url(r'^api/v1/', include(routerTableSelectedItems.urls)),
    url(r'^api/v1/', include(routerDataModel.urls)),
    url(r'^api/v1/', include(routerSqlTableSelectedItems.urls)),

    url(r'^page/processBase', LunchedProcessView.LunchedProcessViewSet.as_view({'get': 'template_view_process_base'}),
        name='template_vieew_inbox'),
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
    url(r'^page/process/new', LunchedProcessView.LunchedProcessViewSet.as_view({'get': 'template_view_new_process'}),
        name='template_view_new_process'),
    url(r'^page/process/diagram',
        LunchedProcessView.LunchedProcessViewSet.as_view({'get': 'template_view_diagram_process'}),
        name='template_view_diagram_process'),
    url(r'^page/process/seeMessage',
        MessageProcessView.MessageProcessViewSet.as_view({'get': 'template_view_do_message_process'}),
        name='template_view_do_message_process'),
    url(r'^page/process/message',
        MessageProcessView.MessageProcessViewSet.as_view({'get': 'template_view_message_process'}),
        name='template_view_message_process'),

    url(r'^page/process/datamodel',
        DataModelerViewSet.as_view({'get': 'template_view'}),
        name='template_view'),

)
