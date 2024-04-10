from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework_mongoengine import viewsets


class LetterSecretariatViewSet(viewsets.ModelViewSet):
    def template_view_base(self, request, *args, **kwargs):
        return render_to_response("letter/Secretariat/base.html",
                                  {}, context_instance=RequestContext(request))

    def template_view_secSideBarbase(self, request, *args, **kwargs):
        return render_to_response("letter/Secretariat/sidebar/base.html",
                                  {}, context_instance=RequestContext(request))
