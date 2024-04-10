from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import viewsets

from amspApp.MyProfile.models import Profile


class Home(viewsets.ViewSet):

    def index(self, request):
        if request.user.is_active:
            # getting profile of registered user
            profile = Profile.objects.get(userID=request.user.id)
            avatar = profile.extra.get('profileAvatar').get('url')
            return render_to_response('Dashboards/Supplement/index.html', {'avatar':avatar},
                                      context_instance=RequestContext(request))

        return render_to_response('Dashboards/Supplement/index_not_registered.html', {},
                                  context_instance=RequestContext(request))

    def base(self, request):
        return render_to_response('Dashboards/Supplement/base.html', {},
                                  context_instance=RequestContext(request))

    def profile(self, request):
        return render_to_response('Dashboards/Supplement/Registration/Profile/base.html', {},
                                  context_instance=RequestContext(request))

    def home(self, request):
        if request.user.is_active:
            return render_to_response('Dashboards/Supplement/home.html', {},
                                      context_instance=RequestContext(request))

        return render_to_response('Dashboards/Supplement/home_not_registered.html', {},
                                  context_instance=RequestContext(request))
