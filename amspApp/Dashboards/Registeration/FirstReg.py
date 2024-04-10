# coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ViewSet

from amspApp.Dashboards.Registeration.FirstRegForm import FirstRegForm, ForgetPassForm


class FirstRegView(ViewSet):

    def firstregForm(self, request):
        frm = FirstRegForm()
        return render_to_response('Dashboards/Supplement/Registration/First/base.html', {"form": frm},
                                  context_instance=RequestContext(request))

    def forgetPassForm(self, request):
        frm = ForgetPassForm()
        return render_to_response('Dashboards/Supplement/ForgetPass/base.html', {"form": frm},
                                  context_instance=RequestContext(request))
