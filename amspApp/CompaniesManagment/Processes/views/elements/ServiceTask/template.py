from django.views.generic import TemplateView


class ServiceTaskTemplate(TemplateView):
    template_name = "companyManagement/BPMN/designer/elements/servicetask/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['customer_information'] = Customer.objects.first()
        return context

