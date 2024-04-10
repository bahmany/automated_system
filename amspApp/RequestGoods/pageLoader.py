from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework_mongoengine import viewsets

from amsp import settings
from amspApp._Share.odoo_connect import odoo_instance


class RGPageLoaderApi(viewsets.ModelViewSet):
    def index(self, request):
        return render_to_response(
            'RequestGoods/base.html',
            {},
            context_instance=RequestContext(request))

    def talkToAnbar(self, request):
        odoo_ins = odoo_instance()
        odoo_ins.check_user_if_not_create(request.user.username)
        odooUrl = settings.ODOO_HTTP_REFERER

        return render_to_response(
            'RequestGoods/talkToAnbar.html',

            {"odooURL": odooUrl,
             'username':request.user.username+"@****.com",
             # "session":session_id
             },
            context_instance=RequestContext(request))

    def RGItem(self, request):
        return render_to_response(
            'RequestGoods/item.html',
            {},
            context_instance=RequestContext(request))

    def helpRG(self, request):
        return render_to_response(
            'RequestGoods/helpRG.html',
            {},
            context_instance=RequestContext(request))

    def RGgoods(self, request):
        return render_to_response(
            'RequestGoods/goodsList.html',
            {},
            context_instance=RequestContext(request))

    def template_view_showSignBodyPrc(self, request):
        return render_to_response('Sales/sign/signBody.html', {},
                                  context_instance=RequestContext(request))
