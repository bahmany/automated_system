from django.conf.urls import patterns, include, url
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers as _routers

from amspApp.CompaniesManagment.BAM.views.BAMView import BAMViewSet
from amspApp.CompaniesManagment.Charts.viewes.ChartSearchViews import ChartSearchViews
from amspApp.CompaniesManagment.Charts.viewes.ChartViews import ChartViewSet
from amspApp.CompaniesManagment.Charts.viewes.ZoneSearchViews import ChartZoneSearchViews
from amspApp.CompaniesManagment.Charts.viewes.ZonesViews import ZoneViewSet
from amspApp.CompaniesManagment.CompanyProfile.views.CompanyProfileViews import CompanyProfileViewSet
from amspApp.CompaniesManagment.Connections.viewes.ConnectionsPoolViews import ConnectionPoolsViewSet
from amspApp.CompaniesManagment.Connections.viewes.ConnectionsViews import ConnectionsViewSet
from amspApp.CompaniesManagment.DMSManagement.viewes.DMSManagementViews import DMSManagementViewSet
from amspApp.CompaniesManagment.Hamkari.views.HamkariJobItemsView import HamkariJobItemViewSet
from amspApp.CompaniesManagment.Hamkari.views.HamkariRequestHamkariViewSet import HamkariRequestHamkariViewSet
from amspApp.CompaniesManagment.Hamkari.views.apiViews import HamkariViewSet
from amspApp.CompaniesManagment.Hamkari.views.hamkariJobsView import HamkariJobsViewSet
from amspApp.CompaniesManagment.Positions.views.PositionViews import PositionViewSet
from amspApp.CompaniesManagment.Processes.views.BpmnModelerView import BpmnViewSet
from amspApp.CompaniesManagment.Processes.views.elements.ServiceTask.template import ServiceTaskTemplate
from amspApp.CompaniesManagment.Products.views.ProductView import CompanyProductionsViewSet
from amspApp.CompaniesManagment.Secretariat.viewes.SecretariatsViews import SecretariatsViewSet
from amspApp.CompaniesManagment.members.views.MemberView import MemberViewSet, MemberViewSetMongo, \
    MemberViewSetMongoWithCustomePaging, ListAllMemberViews, SearchAllRegisteredUsers
from amspApp.CompaniesManagment.views.CompaniesManagmentView import CompaniesManagmentViewSet
from amspApp.CompaniesManagment.views.CompanyMembersJointRequestView import CompanyMembersJointRequestViewset
from amspApp.Letter.views.InboxMembersGroupSearchView import MemberGroupSearchViews

url_companies_api = SimpleRouter()
url_companies_api.register(r'companies', CompaniesManagmentViewSet, base_name="companies", )

url_companies_profile = _routers.NestedSimpleRouter(url_companies_api, r"companies", lookup="companyID")
url_companies_profile.register(r'profile', CompanyProfileViewSet, base_name="profile")

url_companies_process = _routers.NestedSimpleRouter(url_companies_api, r"companies", lookup="companyID")
url_companies_process.register(r'process', BpmnViewSet, base_name="process")

url_companies_bam = _routers.NestedSimpleRouter(url_companies_api, r"companies", lookup="companyID")
url_companies_bam.register(r'BAM', BAMViewSet, base_name="BAM")

url_companies_dms= _routers.NestedSimpleRouter(url_companies_api, r"companies", lookup="companyID")
url_companies_dms.register(r'dms', DMSManagementViewSet, base_name="dms")


url_companies_products = _routers.NestedSimpleRouter(url_companies_api, r"companies", lookup="companyID")
url_companies_products.register(r'products', CompanyProductionsViewSet, base_name="products")

url_companies_chart = _routers.NestedSimpleRouter(url_companies_api, r"companies", lookup="companyID")
url_companies_chart.register(r'chart', ChartViewSet, base_name="chart")

url_companies_zones = _routers.NestedSimpleRouter(url_companies_api, r"companies", lookup="companyID")
url_companies_zones.register(r'chart-zone', ZoneViewSet, base_name="zones")

url_companies_positions = _routers.NestedSimpleRouter(url_companies_api, r"companies", lookup="companyID")
url_companies_positions.register(r'positions', PositionViewSet, base_name="position", )

url_companies_members = _routers.NestedSimpleRouter(url_companies_api, r"companies", lookup="companyID")
url_companies_members.register(r'members', MemberViewSet, base_name="position", )

url_companies_hamkari = _routers.NestedSimpleRouter(url_companies_api, r"companies", lookup="companyID")
url_companies_hamkari.register(r'hamkari', HamkariViewSet, base_name="position", )

url_companies_hamkari_jobs = _routers.NestedSimpleRouter(url_companies_hamkari, r"hamkari", lookup="hamkariID")
url_companies_hamkari_jobs.register(r'job', HamkariJobItemViewSet, base_name="position", )


url_companies_hamkari_jobs_registered = _routers.NestedSimpleRouter(url_companies_hamkari, r"hamkari", lookup="hamkariID")
url_companies_hamkari_jobs_registered.register(r'registeredToHire', HamkariRequestHamkariViewSet, base_name="position", )


url_companies_connections = _routers.NestedSimpleRouter(url_companies_api, r"companies", lookup="companyID")
url_companies_connections.register(r'connections', ConnectionsViewSet, base_name="position", )

url_companies_connections_pools = _routers.NestedSimpleRouter(url_companies_connections, r"connections", lookup="connectionID")
url_companies_connections_pools.register(r'pools', ConnectionPoolsViewSet, base_name="position", )

url_companies_hamkarijobs = _routers.NestedSimpleRouter(url_companies_api, r"companies", lookup="companyID")
url_companies_hamkarijobs.register(r'hamkarijobs', HamkariJobsViewSet, base_name="position", )

url_companies_search_members = SimpleRouter()
url_companies_search_members.register(r'members-search', MemberViewSetMongoWithCustomePaging, base_name="members-search", )

# url_companies_search_members = SimpleRouter()
# url_companies_search_members.register(r'members-search', MemberViewSetMongoWithCustomePaging, base_name="members-search", )

url_companies_secretariats = _routers.NestedSimpleRouter(url_companies_api, r"companies", lookup="companyID")
url_companies_secretariats.register(r'secretariats', SecretariatsViewSet, base_name="secretariats", )

url_companies_invite = _routers.NestedSimpleRouter(url_companies_api, r"companies", lookup="companyID")
url_companies_invite.register(r'invite', CompanyMembersJointRequestViewset, base_name="invite", )

urlpatterns = patterns(
    '',

    url(r'^page/companies', CompaniesManagmentViewSet.as_view({'get': 'template_page'})),
    url(r'^page/comopbase', CompaniesManagmentViewSet.as_view({'get': 'template_page_base'})),
    url(r'^page/company/profile', CompanyProfileViewSet.as_view({'get': 'template_page'})),
    url(r'^page/company/chart', ChartViewSet.as_view({'get': 'template_page'})),

    # url(r'^page/company/baseDms', DMSManagementViewSet.as_view({'get': 'template_page_base'})),
    # url(r'^page/company/newDms', DMSManagementViewSet.as_view({'get': 'template_page_new'})),
    # url(r'^page/company/editDms', DMSManagementViewSet.as_view({'get': 'template_page_edit'})),
    # url(r'^page/dmsBase', DMSManagementViewSet.as_view({'get': 'dmsBase'})),

    # url(r'^page/company/members', CompanyProfileViewSet.as_view({'get':'template_page'})),
    url(r'^page/company/products', CompanyProductionsViewSet.as_view({'get': 'template_page'})),

    url(r'^page/company/hamkarijobs', HamkariJobsViewSet.as_view({'get': 'template_page'})),

    url(r'^page/company/previewResume', HamkariJobsViewSet.as_view({'get': 'template_page_preview'})),

    url(r'^page/company/Connections', ConnectionsViewSet.as_view({'get': 'template_page'})),

    url(r'^page/company/hamkari', HamkariViewSet.as_view({'get': 'template_page'})),
    url(r'^page/company/postJob', HamkariViewSet.as_view({'get': 'template_postJob'})),
    url(r'^page/company/jobItems', HamkariViewSet.as_view({'get': 'template_JobItems'})),
    url(r'^page/company/requestHamkari', HamkariViewSet.as_view({'get': 'template_RequestHamkariItems'})),
    url(r'^page/company/AddEditJobItems', HamkariViewSet.as_view({'get': 'template_AddEditJobItems'})),



    url(r'^page/company/members', MemberViewSet.as_view({'get': 'template_page'})),
    url(r'^page/company/secretariats', SecretariatsViewSet.as_view({'get': 'template_page'})),
    url(r'^page/company/bam', BAMViewSet.as_view({'get': 'template_view'}),name='BAMViewTemplate'),
    url(r'^page/company/dashboardBam', BAMViewSet.as_view({'get': 'template_view_dashboard'}),name='template_view_dashboard'),
    url(r'^page/company/newBam', BAMViewSet.as_view({'get': 'template_view_new'}),name='template_view_new'),
    url(r'^page/company/shakhesBam', BAMViewSet.as_view({'get': 'template_view_shakhes'}),name='template_view_shakhes'),
    url(r'^page/company/editBam', BAMViewSet.as_view({'get': 'template_view_shakhes_edit'}),name='template_view_shakhes_edit'),


    url(r'^page/company/process', BpmnViewSet.as_view({'get': 'template_view'}),name='BpmnModelerViewTemplate'),
    url(r'^page/company/newProcess', BpmnViewSet.as_view({'get': 'template_view_new'}),
        name='template_view_newww'),
    url(r'^page/company/setupProcess', BpmnViewSet.as_view({'get': 'template_view_setup'}),
        name='template_view_setupp'),
    url(r'^page/company/publishBpmn', BpmnViewSet.as_view({'get': 'template_view_publish'}),
        name='template_view_publishs'),
    url(r'^page/company/validateBpmn', BpmnViewSet.as_view({'get': 'template_view_validate'}),
        name='template_view_validates'),
    url(r'^page/company/process/element/service_task', ServiceTaskTemplate.as_view()),


    url(r'^search/company/members', MemberViewSetMongo.as_view(), name="members-list"),
    url(r'^search/charts/members', ChartSearchViews.as_view(), name="charts-list"),
    url(r'^search/zones/members', ChartZoneSearchViews.as_view(), name="zones-list"),
    url(r'^search/groups/members', MemberGroupSearchViews.as_view(), name="groups-list"),
    url(r'^search/company/complex-members', ListAllMemberViews.as_view(), name="members-complex-list"),
    url(r'^search/bulk-user-search', SearchAllRegisteredUsers.as_view(), name="bulk-user-search"),
    # url(r'^search/company/complex-members/getAll', ListAllMemberViews.as_view(), name="members-complex-list"),


    url(r'^api/v1/', include(url_companies_api.urls)),
    url(r'^api/v1/', include(url_companies_profile.urls)),
    url(r'^api/v1/', include(url_companies_products.urls)),
    url(r'^api/v1/', include(url_companies_chart.urls)),
    url(r'^api/v1/', include(url_companies_zones.urls)),
    url(r'^api/v1/', include(url_companies_process.urls)),
    url(r'^api/v1/', include(url_companies_bam.urls)),
    url(r'^api/v1/', include(url_companies_positions.urls), name="position"),
    url(r'^api/v1/', include(url_companies_dms.urls), name="dms"),
    url(r'^api/v1/', include(url_companies_members.urls), name="members"),
    url(r'^api/v1/', include(url_companies_search_members.urls), name="members-search"),
    url(r'^api/v1/', include(url_companies_secretariats.urls), name="secretariats"),
    url(r'^api/v1/', include(url_companies_invite.urls), name="invite"),
    url(r'^api/v1/', include(url_companies_hamkari.urls), name="hamkari"),
    url(r'^api/v1/', include(url_companies_hamkari_jobs.urls), name="hamkari"),
    url(r'^api/v1/', include(url_companies_hamkarijobs.urls), name="hamkarijobs"),
    url(r'^api/v1/', include(url_companies_hamkari_jobs_registered.urls), name="hamkarijobs"),
    url(r'^api/v1/', include(url_companies_connections.urls), name="connections"),
    url(r'^api/v1/', include(url_companies_connections_pools.urls), name="connections"),
)


