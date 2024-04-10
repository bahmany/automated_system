from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import viewsets


class PageLoaderApi(viewsets.ModelViewSet):

    def template_bibasepage(self, request):
        return render_to_response(
            'BI/base.html',
            {},
            context_instance=RequestContext(request))

    def template_bigroups(self, request):
        if request.user.groups.filter(name='bi_admin').count() == 0:
            return render_to_response('Financial/cog/noaccess.html', {}, context_instance=RequestContext(request))

        return render_to_response(
            'BI/groups/groupsBase.html',
            {},
            context_instance=RequestContext(request))

    def template_bimenus(self, request):
        if request.user.groups.filter(name='bi_admin').count() == 0:
            return render_to_response('Financial/cog/noaccess.html', {}, context_instance=RequestContext(request))

        return render_to_response(
            'BI/menus/base.html',
            {},
            context_instance=RequestContext(request))

    def template_bimenuspartialitems(self, request):
        if request.user.groups.filter(name='bi_admin').count() == 0:
            return render_to_response('Financial/cog/noaccess.html', {}, context_instance=RequestContext(request))
        return render_to_response(
            'BI/menus/partialItems.html',
            {},
            context_instance=RequestContext(request))

    def template_bigroupspartialmembers(self, request):
        if request.user.groups.filter(name='bi_admin').count() == 0:
            return render_to_response('Financial/cog/noaccess.html', {}, context_instance=RequestContext(request))
        return render_to_response(
            'BI/groups/partialMembers.html',
            {},
            context_instance=RequestContext(request))

    def template_bimenuspartialmembers(self, request):
        if request.user.groups.filter(name='bi_admin').count() == 0:
            return render_to_response('Financial/cog/noaccess.html', {}, context_instance=RequestContext(request))

        return render_to_response(
            'BI/menus/partialMembers.html',
            {},
            context_instance=RequestContext(request))

    def template_bimenuspartialmembersusers(self, request):
        if request.user.groups.filter(name='bi_admin').count() == 0:
            return render_to_response('Financial/cog/noaccess.html', {}, context_instance=RequestContext(request))

        return render_to_response(
            'BI/menus/partialMembersUsers.html',
            {},
            context_instance=RequestContext(request))

    def template_bidashboardpages(self, request):
        if request.user.groups.filter(name='bi_admin').count() == 0:
            return render_to_response('Financial/cog/noaccess.html', {}, context_instance=RequestContext(request))
        return render_to_response(
            'BI/pages/pageBase.html',
            {},
            context_instance=RequestContext(request))

    def template_bipages(self, request):
        return render_to_response(
            'BI/pages/showPages.html',
            {},
            context_instance=RequestContext(request))

    def template_bipage(self, request):
        return render_to_response(
            'BI/page/base.html',
            {},
            context_instance=RequestContext(request))

    def template_bidashboardpagesdashboard(self, request):
        if request.user.groups.filter(name='bi_admin').count() == 0:
            return render_to_response('Financial/cog/noaccess.html', {}, context_instance=RequestContext(request))
        return render_to_response(
            'BI/pages/BIPageDesign.html',
            {},
            context_instance=RequestContext(request))

    def template_bicharts(self, request):
        if request.user.groups.filter(name='bi_admin').count() == 0:
            return render_to_response('Financial/cog/noaccess.html', {}, context_instance=RequestContext(request))
        return render_to_response(
            'BI/charts/baseIBChart.html',
            {},
            context_instance=RequestContext(request))

    def template_bichartdesign(self, request):
        if request.user.groups.filter(name='bi_admin').count() == 0:
            return render_to_response('Financial/cog/noaccess.html', {}, context_instance=RequestContext(request))
        return render_to_response(
            'BI/charts/BIChartDesign.html',
            {},
            context_instance=RequestContext(request))

    def template_bidatasources(self, request):
        if request.user.groups.filter(name='bi_admin').count() == 0:
            return render_to_response('Financial/cog/noaccess.html', {}, context_instance=RequestContext(request))
        return render_to_response(
            'BI/datasources/BIDatasources.html',
            {},
            context_instance=RequestContext(request))

    def template_bidatasourcesdesign(self, request):
        if request.user.groups.filter(name='bi_admin').count() == 0:
            return render_to_response('Financial/cog/noaccess.html', {}, context_instance=RequestContext(request))
        return render_to_response(
            'BI/datasources/BIDatasourcesDesign.html',
            {},
            context_instance=RequestContext(request))

    def template_bidatasourcesmodal(self, request):
        if request.user.groups.filter(name='bi_admin').count() == 0:
            return render_to_response('Financial/cog/noaccess.html', {}, context_instance=RequestContext(request))
        return render_to_response(
            'BI/datasources/BIModalAddConnection.html',
            {},
            context_instance=RequestContext(request))

    def template_bisqlsbase(self, request):
        if request.user.groups.filter(name='bi_admin').count() == 0:
            return render_to_response('Financial/cog/noaccess.html', {}, context_instance=RequestContext(request))
        return render_to_response(
            'BI/sqls/BISqlsBase.html',
            {},
            context_instance=RequestContext(request))

    def template_bisql(self, request):
        if request.user.groups.filter(name='bi_admin').count() == 0:
            return render_to_response('Financial/cog/noaccess.html', {}, context_instance=RequestContext(request))
        return render_to_response(
            'BI/sqls/BISqlDesign.html',
            {},
            context_instance=RequestContext(request))

    def template_bi_sample_page_for_ceo(self, request):
        return render_to_response(
            'BI/SamplePageForCEO/base.html',
            {},
            context_instance=RequestContext(request))

    def template_amareroozaneh(self, request):
        return render_to_response(
            'BI/pages/special/BIAmarehRoozaneh.html',
            {},
            context_instance=RequestContext(request))
