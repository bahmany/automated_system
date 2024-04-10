from django.conf.urls import patterns, include, url
from rest_framework_mongoengine import routers
from amspApp.Chat.views.ChatViews import ChatViewSet

router = routers.SimpleRouter()
router.register(r'chat', ChatViewSet, base_name='LunchedProcess')

urlpatterns = patterns(
    '',
    url(r'^api/v1/', include(router.urls)),
)
