from django.conf.urls import patterns, url

# from amspApp.Welcome.views.PageLoader import welcomeBase, welcomeSelectPics, welcomeSelectNames, welcomeCompleted
# from amspApp.Welcome.views.PageLoader import welcomePage
from amspApp.apps.imageUploaderCropper import views


urlStart = "api/v1/apps/imageUploaderCrop"

urlpatterns = patterns('',
                       url(r'^page/apps/imageUploadCrop/home', views.home),
)

