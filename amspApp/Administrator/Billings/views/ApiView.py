from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import viewsets, permissions, views
from rest_framework.response import Response
from amspApp.Administrator.Billings.forms.BillingStrategyFormValidation import BillingStrategyForm, PaymentForm
from amspApp.Administrator.permission.IsSuperUser import IsSuper


class BillingRegisterApiViewSet(views.APIView):
    permission_classes = (IsSuper,)

    def get(self, request):
        return render_to_response(
            'Administrator/Billing/NewBilling.html',
            {
                "form": BillingStrategyForm(scope_prefix="Billing")
            },
            context_instance=RequestContext(request))


class BillingBaseApiViewSet(views.APIView):
    permission_classes = (IsSuper,)

    def get(self, request):
        return render_to_response(
            'Administrator/Billing/base.html',
            {
            },
            context_instance=RequestContext(request))


class PaymentApiViewSet(views.APIView):
    permission_classes = (IsSuper,)

    def get(self, request):
        return render_to_response(
            'Administrator/Billing/payment/NewPayment.html',
            {
                "form": PaymentForm(scope_prefix="Payment")
            },
            context_instance=RequestContext(request))


class PaymentBaseApiViewSet(views.APIView):
    permission_classes = (IsSuper,)

    def get(self, request):
        return render_to_response(
            'Administrator/Billing/payment/base.html',
            {

            },
            context_instance=RequestContext(request))
