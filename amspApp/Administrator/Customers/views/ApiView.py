from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import viewsets, permissions, views
from rest_framework.response import Response
from amspApp.Administrator.Customers.forms.CustomerRegistrationFormValidation import CustomerRegistrationForm
from amspApp.Administrator.permission.IsSuperUser import IsSuper


class CustomersRegisterApiViewSet(views.APIView):
    permission_classes = (IsSuper,)
    def get(self, request):
        return render_to_response(
            'Administrator/Customers/Register.html',
            {
                "form": CustomerRegistrationForm(scope_prefix="Customer")

            },
            context_instance=RequestContext(request))


class CustomersBaseApiViewSet(views.APIView):
    permission_classes = (IsSuper,)
    def get(self, request):
        return render_to_response(
            'Administrator/Customers/base.html',
            {
            },
            context_instance=RequestContext(request))
