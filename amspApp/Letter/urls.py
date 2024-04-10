from django.conf.urls import patterns, url, include
from rest_framework.routers import SimpleRouter, Route, DynamicDetailRoute
from rest_framework_nested.routers import NestedSimpleRouter
from amspApp.Letter.search.InboxSearch import  InboxSearchViewClass
from amspApp.Letter.views.InboxComposeView import InboxComposeViewSet
from amspApp.Letter.views.InboxFolderView import InboxFolderViewset
from amspApp.Letter.views.InboxForward import InboxForwardViewSet
from amspApp.Letter.views.InboxGroupView import InboxGroupViewset
from amspApp.Letter.views.InboxLabelView import InboxLabelViewset
from amspApp.Letter.views.InboxListView import InboxListViewSet
from amspApp.Letter.views.InboxPreviewView import InboxPreviewViewSet
from amspApp.Letter.views.InboxView import InboxViewSet
from amspApp.Letter.views.LetterView import LetterViewSet
from amspApp.Letter.views.Secretariate.BaseView import LetterSecretariatViewSet
from amspApp.Letter.views.Secretariate.CompanyGroupReciever import CompanyGroupsRecieverViewSet
from amspApp.Letter.views.Secretariate.CompanyRecieverView import CompanyRecieverViewSet
from amspApp.Letter.views.Secretariate.ExportImportView import ExportImportViewSet
from amspApp.Letter.views.Secretariate.ExportScannedAfterSendView import ExportScannedAfterSendViewSet
from amspApp.Letter.views.Secretariate.ExportView import SecExportViewSet
from amspApp.Letter.views.Secretariate.RecieversView import RecievedViewSet
from amspApp.Letter.views.Secretariate.TagsView import SecTagsViewSet
from amspApp.Letter.views.Secretariate.TemplatesView import ExportTemplatesViewSet


letterInboxFolder_router = SimpleRouter()
letterInboxFolder_router.register("inboxFolders", InboxFolderViewset, base_name="InboxFolderPage")

letterInboxLabel_router = SimpleRouter()
letterInboxLabel_router .register("inboxLabels", InboxLabelViewset, base_name="InboxLabelPage")

letterInboxGroup_router = SimpleRouter()
letterInboxGroup_router .register("inboxGroups", InboxGroupViewset, base_name="InboxGroupPage")

letter_router = SimpleRouter()
letter_router.register("letter", LetterViewSet, base_name="letter-detail")

# inbox_router = SimpleRouter()
# inbox_router.register("inbox", InboxListViewSet, base_name="inbox-details")

inbox_forward_router = SimpleRouter()
inbox_forward_router.register(r"forward", InboxForwardViewSet, base_name="forward")

inbox_router = SimpleRouter()
inbox_router.register(r"inbox", InboxListViewSet, base_name="inbox-details")

inbox_sec_companygroup_router = SimpleRouter()
inbox_sec_companygroup_router.register(r"company-group", CompanyGroupsRecieverViewSet, base_name="secretariat-details")

inbox_sec_company_router = SimpleRouter()
inbox_sec_company_router.register(r"company", CompanyRecieverViewSet, base_name="secretariat-details")

inbox_sec_export_router = SimpleRouter()
inbox_sec_export_router.register(r"export", SecExportViewSet, base_name="secretariat-details")

inbox_sec_export_recieved_router = SimpleRouter()
inbox_sec_export_recieved_router.register(r"recieved", RecievedViewSet, base_name="secretariat-details")

inbox_sec_export_scan_router = SimpleRouter()
inbox_sec_export_scan_router.register(r"export-scan", ExportScannedAfterSendViewSet, base_name="secretariat-details")

inbox_sec_export_templates_router = SimpleRouter()
inbox_sec_export_templates_router.register(r"export-templates", ExportTemplatesViewSet, base_name="secretariat-details")

inbox_sec_export_import_router = SimpleRouter()
inbox_sec_export_import_router.register(r"export-import", ExportImportViewSet, base_name="secretariat-details")

inbox_sec_tag_router = SimpleRouter()
inbox_sec_tag_router.register(r"tag", SecTagsViewSet, base_name="secretariat-tags")

# url_companies_chart = _routers.NestedSimpleRouter(url_companies_api, r"companies", lookup="companyID")
# url_companies_chart.register(r'chart', ChartViewSet, base_name="chart")

urlpatterns = patterns(
    '',
    url(r'^api/v1/', include(letterInboxFolder_router.urls)),
    url(r'^api/v1/', include(letterInboxLabel_router.urls)),
    url(r'^api/v1/', include(letterInboxGroup_router.urls)),
    url(r'^api/v1/', include(letter_router.urls)),
    url(r'^api/v1/', include(inbox_router.urls)),
    url(r'^api/v1/inbox/', include(inbox_forward_router.urls)),

    url(r'^api/v1/letter/sec/', include(inbox_sec_companygroup_router.urls)),
    url(r'^api/v1/letter/sec/', include(inbox_sec_company_router.urls)),
    url(r'^api/v1/letter/sec/', include(inbox_sec_export_router.urls)),
    url(r'^api/v1/letter/sec/', include(inbox_sec_export_recieved_router.urls)),
    url(r'^api/v1/letter/sec/', include(inbox_sec_export_scan_router.urls)),
    url(r'^api/v1/letter/sec/', include(inbox_sec_export_templates_router.urls)),
    url(r'^api/v1/letter/sec/', include(inbox_sec_export_import_router.urls)),
    url(r'^api/v1/letter/sec/', include(inbox_sec_tag_router.urls)),

    url(r'^page/letterBase', InboxViewSet.as_view({"get":"template_view_base"})),
    url(r'^page/letter/inboxParts', InboxViewSet.as_view({"get":"template_view_inboxParts"})),
    url(r'^page/letter/inbox', InboxListViewSet.as_view({"get":"template_view"})),
    url(r'^page/letter/listinbox', InboxListViewSet.as_view({"get":"template_view_list"})),
    url(r'^page/letter/sidebar', InboxListViewSet.as_view({"get":"template_view_sidebar"})),
    url(r'^page/letter/compose', InboxComposeViewSet.as_view({"get":"template_view"})),
    # url(r'^page/letter/forward', InboxForwardViewSet.as_view({"get":"template_view"})),
    url(r'^page/letter/basecompose', InboxComposeViewSet.as_view({"get":"template_view_basecompose"})),
    url(r'^page/letter/baseprev', InboxPreviewViewSet.as_view({"get":"template_view_base"})),
    url(r'^page/letter/prev', InboxPreviewViewSet.as_view({"get":"template_view"})),


    url(r'^page/letter/secBase', LetterSecretariatViewSet.as_view({"get":"template_view_base"})),
    url(r'^page/letter/secSideBar', LetterSecretariatViewSet.as_view({"get":"template_view_secSideBarbase"})),
    url(r'^page/letter/sec/company-groupBase', CompanyGroupsRecieverViewSet.as_view({"get":"template_view_company_group"})),
    url(r'^page/letter/sec/companyBase', CompanyRecieverViewSet.as_view({"get":"template_view_company"})),
    url(r'^page/letter/sec/exportBase', SecExportViewSet.as_view({"get":"template_view"})),
    url(r'^page/letter/sec/sidebar', SecExportViewSet.as_view({"get":"template_view_sidebar"})),
    url(r'^page/letter/sec/importPrev', SecExportViewSet.as_view({"get":"template_view_export_import_preview"})),
    url(r'^page/letter/sec/importList', SecExportViewSet.as_view({"get":"template_view_export_export_import_list"})),
    # url(r'^page/letter/sec/ExportList', SecExportViewSet.as_view({"get":"template_view_export_list"})),
    url(r'^page/letter/sec/exportList', SecExportViewSet.as_view({"get":"template_view_export_list"})),
    url(r'^page/letter/sec/export-prev', SecExportViewSet.as_view({"get":"template_view_export_prev"})),
    url(r'^page/letter/sec/export-recieved', SecExportViewSet.as_view({"get":"template_view_export_recieved"})),
    url(r'^page/letter/sec/export-scan', SecExportViewSet.as_view({"get":"template_view_export_scan"})),
    url(r'^page/letter/sec/export-templates', SecExportViewSet.as_view({"get":"template_view_export_templates"})),
    url(r'^page/letter/sec/importNew', SecExportViewSet.as_view({"get":"template_view_import_templates"})),

    url(r'^search/inbox', InboxSearchViewClass.as_view(), name="inbox-list"),



)