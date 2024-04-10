




from django.conf.urls import patterns, include, url
from rest_framework_mongoengine import routers
from rest_framework_nested.routers import NestedSimpleRouter

from amspApp.ControlProject.views.ControlProjectBaseViews import ControlProjectBaseTemplateView
from amspApp.ControlProject.views.ControlProjectIncomeTypeViews import ControlProjectIncomeTypeTemplate, ControlProjectIncomeTypeViewSet
from amspApp.ControlProject.views.ControlProjectOutcomeTypeViews import ControlProjectOutcomeTypeTemplate, ControlProjectOutcomeTypeViewSet
from amspApp.ControlProject.views.ControlProjectYearsShareViews import ControlProjectYearsShareTemplateView, ControlProjectYearsShareViewSet
from amspApp.ControlProject.views.ControlProjectYearsViews import ControlProjectYearsTemplateView, ControlProjectYearsViewSet
from amspApp.ControlProject.views.Projects.ControlProjectProjectView import ControlProjectProjectTemplateView, ControlProjectProjectViewSet, \
    ControlProjectFrameProjectTemplateView
from amspApp.ControlProject.views.subProjects.ControlProjectSubProjectView import ControlProjectSubProjectViewSet, \
    ControlProjectSubProjectTemplateView

ControlProjectYear = routers.SimpleRouter()
ControlProjectYear.register(r'Year', ControlProjectYearsViewSet, base_name='MStatisticsTemplateViewSet')


ControlProjectYearShare = NestedSimpleRouter(ControlProjectYear, r"Year", lookup="Year")
ControlProjectYearShare.register(r'Share', ControlProjectYearsShareViewSet, base_name="profile")

outcomeTypes = routers.SimpleRouter()
outcomeTypes.register(r'outcomeTypes', ControlProjectOutcomeTypeViewSet, base_name='MStatisticsTemplateViewSet')

incomeTypes = routers.SimpleRouter()
incomeTypes.register(r'incomeTypes', ControlProjectIncomeTypeViewSet, base_name='MStatisticsTemplateViewSet')

incomeTypes = routers.SimpleRouter()
incomeTypes.register(r'incomeTypes', ControlProjectIncomeTypeViewSet, base_name='MStatisticsTemplateViewSet')

Projects = NestedSimpleRouter(ControlProjectYear, r"Year", lookup="yearID")
Projects.register(r'projects', ControlProjectProjectViewSet, base_name="projects")

SubProjects = NestedSimpleRouter(ControlProjectYear, r"Year", lookup="yearID")
SubProjects.register(r'subProjects', ControlProjectSubProjectViewSet, base_name="subProjects")


# ControlProjectYearShare = routers.SimpleRouter()
# ControlProjectYearShare.register(r'ShareYear', ControlProjectYearsShareViewSet, base_name='MStatisticsTemplateViewSet')


urlpatterns = patterns(
    '',

    url(r'^api/v1/ControlProject/', include(ControlProjectYear.urls)),
    url(r'^api/v1/ControlProject/', include(ControlProjectYearShare.urls)),
    url(r'^api/v1/ControlProject/', include(outcomeTypes.urls)),
    url(r'^api/v1/ControlProject/', include(incomeTypes.urls)),
    url(r'^api/v1/ControlProject/', include(SubProjects.urls)),
    url(r'^api/v1/ControlProject/', include(Projects.urls)),

    # url(r'^page/datatables/share', DataTableViewSet.as_view({'get': 'template_view_share'}),name='template_vieew_inbox'),
    # url(r'^page/datatables/new', DataTableViewSet.as_view({'get': 'template_view_edit'}),name='template_vieew_inbox'),
    # url(r'^page/datatables', DataTableViewSet.as_view({'get': 'template_view'}),name='template_vieew_inbox')
    url(r'^page/ControlProject/Projects', ControlProjectProjectTemplateView.as_view(), name='template_view_cost_cal'),
    # url(r'^page/ControlProject/IFrameProjects', ControlProjectFrameProjectTemplateView.as_view(), name='template_view_IFrameProjects'),
    url(r'^page/ControlProject/SubProjects', ControlProjectSubProjectTemplateView.as_view(), name='template_view_cost_cal'),
    url(r'^page/ControlProject/Income', ControlProjectIncomeTypeTemplate.as_view(), name='template_view_cost_cal'),
    url(r'^page/ControlProject/Outcome', ControlProjectOutcomeTypeTemplate.as_view(), name='template_view_cost_cal'),
    url(r'^page/ControlProject/Year/Share', ControlProjectYearsShareTemplateView.as_view(), name='template_view_cost_cal'),
    url(r'^page/ControlProject/Year', ControlProjectYearsTemplateView.as_view(), name='template_view_cost_cal'),
    url(r'^page/ControlProject', ControlProjectBaseTemplateView.as_view(), name='template_view_cost_cal'),

)

