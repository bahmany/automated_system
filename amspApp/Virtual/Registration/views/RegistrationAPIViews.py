import json
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import viewsets, permissions, views
from rest_framework.response import Response
from amspApp.Virtual.Registration.forms.loginForm import RegisterationLoginForm, RegisterationHireForm


class DashboardBaseApiViewSet(views.APIView):

    def get(self, request):
        return render_to_response(
            'Virtual/Dashboard/base.html',
            {},
            context_instance=RequestContext(request))


class LoginToRegisteryApiViewSet(views.APIView):

    def get(self, request):
        form = RegisterationHireForm()
        # capchaimg = form.fields["captcha"].widget._key
        return render_to_response(
            'Virtual/Registration/base.html',
            {'form':RegisterationHireForm()},
            context_instance=RequestContext(request))

    def post(self, request):
        form = RegisterationLoginForm(request.POST)
        if self.request.is_ajax():
            if not form.is_valid():
                to_json_response = dict()
                to_json_response['status'] = 0
                to_json_response['form_errors'] = form.errors
                to_json_response['new_cptch_key'] = CaptchaStore.generate_key()
                to_json_response['new_cptch_image'] = captcha_image_url(to_json_response['new_cptch_key'])
                return HttpResponse(json.dumps(to_json_response), content_type='application/json')
        return Response({})
        # return Response(form.errors)


