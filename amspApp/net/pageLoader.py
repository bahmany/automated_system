from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import viewsets

from amsp import settings
from amspApp.Infrustructures.Classes.DateConvertors import getCurrentYearShamsi, \
    getCurrentMonthShamsi
from amspApp._Share.odoo_connect import odoo_instance


class PageLoaderApi(viewsets.ModelViewSet):

    def template_base(self, request):
        odoo_ins = odoo_instance()
        odoo_ins.check_user_if_not_create(request.user.username)
        odooUrl = settings.ODOO_Platform+settings.ODOO_NET

        return render_to_response(
            'NET/base.html',
            {"odooURL": odooUrl,
             'username': request.user.username + "@****.com",
             # "session":session_id
             }
            ,
            context_instance=RequestContext(request))
