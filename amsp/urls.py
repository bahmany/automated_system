from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView
from amspApp import views
from amspApp.AdvProcess import urls as advProcessUrl
from amspApp.BPMSystem import urls as taskUrl
from amspApp.BPMSystem.BPMReport import urls as processReportsUrl
from amspApp.Calendar import urls as calendarUrl
from amspApp.CompaniesManagment import urls as companyUrl
from amspApp.Contacts import urls as contacsUrl
from amspApp.ControlProject import urls as ControlProjectUrl
from amspApp.BI.DataTables import urls as dataTable
from amspApp.FileServer import urls as fileUrl
from amspApp.Friends import urls as FrndUrl
from amspApp.Infrustructures import urls as InfrUrl
from amspApp.Letter import urls as letterInboxUrl
from amspApp.MSSystem import urls as MSSystemUrl
from amspApp.MyProfile import urls as profileUrl
from amspApp.News import urls as newsUrl
from amspApp.Notifications import urls as notifyUrl
from amspApp.Sales import urls as salesUrl
from amspApp.Sales.views.PreviewHavaleh import prevHavaleh
from amspApp.SpecialApps import urls as specialApp
from amspApp.UserSettings import urls as USettingUrl
from amspApp.Virtual import urls as virtualUrl
from amspApp.Welcome import urls as welcomeUrl
from amspApp.amspUser import urls as amspUserUrls
from amspApp.amspUser.views.StatisticsView import GetStaticsViewSet
from amspApp.dashboard import urls as dashboardUrls
from amspApp.publicViews import urls as shareUrl
from amspApp.QC import urls as qcUrl
from amspApp.Chat import urls as chatUrl
from amspApp.DMS import urls as dmsUrl
from amspApp.apps.imageUploaderCropper import urls as imgUploaderUrl
from amspApp.Financial import urls as financialUrl
from amspApp.Dashboards import urls as DashboardsUrl
from amspApp.Trace import urls as TraceUrl
from amspApp.qr import urls as QrCodeUrl
from amspApp.RequestGoods import urls as RG
from amspApp.Material import urls as MT
from amspApp.Edari.hz import urls as HZ
from amspApp.net import urls as NET
from amspApp.Edari.ez import urls as EZ
from amspApp.Edari import urls as Eda
from amspApp.Fees import urls as fz
from amspApp.Edari.Morekhasi import urls as mrkh
from amspApp.BI import urls as biurl

from amspApp.views import IndexView, TranslateUknown, Language
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^reg/', include(virtualUrl)),
    url(r'^SpecialApps/', include(specialApp)),
    # url(r'^administrator/', include(adminUrl)),
    # url(r'^docs/', include('puput.urls')),
    url(r'^Financial/', include(financialUrl)),
    url(r'^dashboards/', include(DashboardsUrl)),
    url(r'^qr/', include(QrCodeUrl)),

    # url(r'^ControlProject/', ControlProjectIndexView.as_view()),
    url(r'^xt/', prevHavaleh),

    # login and logout stuff ------------

    # -----------------------------------

    url(r'^admin/', include(admin.site.urls)),
    (r'^admin/defender/', include('amspApp.middlewares.defender.urls')),  # defender admin
    url(r'^page/base', views.base),
    url(r'^page/home', views.home),
    url(r'^page/control_project', views.control_project),
    # url(r'^page/freeRahsoon', views.freeRahsoon),

    # url(r'^page/selectpics', views.selectpics),
    # url(r'^page/selectnames', views.selectnames),
    # url(r'^page/welcomePage', views.welcomePage),
    # url(r'^page/welcomeCompleted', views.welcomeCompleted),
    url(r'^page/oldAmsp', views.oldAmsp),
    url(r'^page/erp_control_project', views.erp_control_project),

    url(r'^api/v1/translate', TranslateUknown.as_view()),
    url(r'^api/v1/language', Language.as_view()),

    url(r'^', include(amspUserUrls)),
    url(r'^', include(dashboardUrls)),
    url(r'^', include(companyUrl)),
    url(r'^', include(taskUrl)),
    url(r'^', include(processReportsUrl)),
    url(r'^', include(profileUrl)),
    url(r'^', include(letterInboxUrl)),
    url(r'^', include(fileUrl)),
    url(r'^', include(InfrUrl)),
    url(r'^', include(FrndUrl)),
    url(r'^', include(USettingUrl)),
    url(r'^', include(MSSystemUrl)),
    url(r'^', include(shareUrl)),
    url(r'^', include(notifyUrl)),
    url(r'^', include(contacsUrl)),
    url(r'^', include(dataTable)),
    url(r'^', include(calendarUrl)),
    url(r'^', include(newsUrl)),
    url(r'^', include(advProcessUrl)),
    url(r'^', include(ControlProjectUrl)),
    url(r'^', include(salesUrl)),
    url(r'^', include(welcomeUrl)),
    url(r'^', include(qcUrl)),
    url(r'^', include(chatUrl)),
    url(r'^', include(imgUploaderUrl)),
    url(r'^', include(dmsUrl)),
    url(r'^', include(TraceUrl)),
    url(r'^', include(RG)),
    url(r'^', include(MT)),
    url(r'^', include(HZ)),
    url(r'^', include(NET)),
    url(r'^', include(Eda)),

    url(r'^', include(EZ)),
    url(r'^', include(mrkh)),

    url(r'^', include(fz)),
    url(r'^', include(biurl)),

    url(r'^page/_dash', views._dash),
    url(r'^page/dashboard', views.dashboard),
    # url(r'^page/dashboard', views.dashboard),
    url(r'^page/generic/upload', views.upload),
    url(r'^page/generic/selectPosition', views.selectPosition),
    url(r'^page/generic/showBpmnStepData', views.showBpmnStepData),
    url(r'^getCurrent', views.getCurrent),

    url(r'^getStatistcs', GetStaticsViewSet.as_view(), name='getStatistics'),
    url(r'^getInboxStatistics', GetStaticsViewSet().getInboxStatistics),
    url(r'^getFirstTimeInboxStatistics', GetStaticsViewSet().getFirstTimeInboxStatistics),
    url(r'^getInboxFoldersStatistics', GetStaticsViewSet().getInboxFoldersStatistics),
    url(r'^getInboxLabelsStatistics', GetStaticsViewSet().getInboxLabelsStatistics),
    url(r'^UpdateStatics', GetStaticsViewSet().UpdateStatics),
    url('^.*$', IndexView.as_view(), name='index'),
) + staticfiles_urlpatterns()

from django.conf import settings

if settings.DEBUG:
    import os
    from django.conf.urls import patterns
    from django.conf.urls.static import static
    from django.views.generic.base import RedirectView
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()  # tell gunicorn where static files are in dev mode
    urlpatterns += static(settings.MEDIA_URL + 'images/', document_root=os.path.join(settings.MEDIA_ROOT, 'images'))
    urlpatterns += patterns('',
                            (r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'images/favicon.ico'))
                            )
    urlpatterns += staticfiles_urlpatterns()
