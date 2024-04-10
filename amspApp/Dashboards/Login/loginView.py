from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets

from amspApp.Dashboards.Login.forms.loginForm import LoginForm


class LoginView(viewsets.ViewSet):

    @csrf_exempt
    def loginForm(self, request):
        frm = LoginForm()
        return render_to_response('Dashboards/Supplement/Login/login.html', {
            "form": frm}, context_instance=RequestContext(request))
