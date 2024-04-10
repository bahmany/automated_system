from django.conf.urls import patterns, include, url
from rest_framework_mongoengine import routers
from amspApp.Bpms.views import LunchedProcessView, MessageProcessView
from amspApp.Calendar.views.CalendarItemsViews import CalendarItemsViewSet

router = routers.SimpleRouter()
router.register(r'calendarItem', CalendarItemsViewSet, base_name='LunchedProcess')

urlpatterns = patterns(
    '',


    url(r'^api/v1/', include(router.urls)),


)
