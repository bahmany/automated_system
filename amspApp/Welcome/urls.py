from django.conf.urls import patterns, url

from amspApp.Welcome.views.PageLoader import welcomeBase, welcomeSelectPics, welcomeSelectNames, welcomeCompleted
from amspApp.Welcome.views.PageLoader import welcomePage

urlpatterns = patterns('',
                       url(r'^page/welcomeBase', welcomeBase.as_view()),
                       url(r'^page/welcomePage', welcomePage.as_view()),
                       url(r'^page/welcomeSelectPics', welcomeSelectPics.as_view()),
                       url(r'^page/welcomeSelectNames', welcomeSelectNames.as_view()),
                       url(r'^page/welcomeCompleted', welcomeCompleted.as_view()),
)

