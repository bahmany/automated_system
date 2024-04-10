# coding=utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework.viewsets import ViewSet


class SecondRegView(ViewSet):

    def secondregForm(self, request):
        return render_to_response('Dashboards/Supplement/Registration/Second/base.html',
                                  {},
                                  context_instance=RequestContext(request))

    def baseSupply(self, request):
        return render_to_response('Dashboards/Supplement/Registration/Supply/base.html',
                                  {},
                                  context_instance=RequestContext(request))

    def imageDialog(self, request):
        return render_to_response('Dashboards/Supplement/Registration/Supply/imageDialog.html',
                                  {},
                                  context_instance=RequestContext(request))

    def imageViewDialog(self, request):
        return render_to_response('Dashboards/Supplement/Registration/Supply/imageViewDialog.html',
                                  {},
                                  context_instance=RequestContext(request))

    def OpenCateg(self, request):
        return render_to_response('Dashboards/Supplement/Registration/Supply/catSelect.html',
                                  {},
                                  context_instance=RequestContext(request))

    def supplyItems(self, request, pk):
        return render_to_response('Dashboards/Supplement/Registration/Supply/loader.html',
                                  {"pk": pk},
                                  context_instance=RequestContext(request))
