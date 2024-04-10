from asq.initiators import query
from django.http import HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from amspApp.Edari.Morekhasi.models import MorekhasiSaati
from amspApp.News.models import News
from amspApp.News.serializers.NewsSerializer import NewsSerializer
from amspApp._Share.ListPagination import DetailsPagination
from amspApp.publicViews.SelectMembers.views.GetPositionView import GetPositionViewset


class NewsViewSet(viewsets.ModelViewSet):
    lookup_field = 'id'
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    pagination_class = DetailsPagination
    pagination_class.page_size = 30

    @list_route(methods=["get"])
    def getLatest(self, request):



        new1 = self.get_queryset().filter(type=1).order_by('-id').limit(30)
        new2 = self.get_queryset().filter(type=2).order_by('-id').limit(30)
        new3 = self.get_queryset().filter(type=3).order_by('-id').limit(30)
        new4 = self.get_queryset().filter(type=4).order_by('-id').limit(30)
        new5 = self.get_queryset().filter(type=5).order_by('-id').limit(30)
        new6 = self.get_queryset().filter(type=6).order_by('-id').limit(30)
        new7 = self.get_queryset().filter(type=7).order_by('-id').limit(30)

        new1 = self.serializer_class(instance=new1, many=True).data
        new2 = self.serializer_class(instance=new2, many=True).data
        new3 = self.serializer_class(instance=new3, many=True).data
        new4 = self.serializer_class(instance=new4, many=True).data
        new5 = self.serializer_class(instance=new5, many=True).data
        new6 = self.serializer_class(instance=new6, many=True).data
        new7 = self.serializer_class(instance=new7, many=True).data

        return Response({
            'new1': new1,
            'new2': new2,
            'new3': new3,
            'new4': new4,
            'new5': new5,
            'new6': new6,
            'new7': new7,
        })

    @list_route(methods=["get"])
    def getNews(self, request):
        qtype = int(request.query_params["t"])
        defaultNews = self.queryset.filter(companyID=-1, type=qtype).limit(1)
        self.queryset = self.get_queryset().filter(type=qtype)
        thisCompanyNews = self.queryset.order_by("-id").limit(1)
        dataDefault = self.serializer_class(instance=defaultNews, many=True).data
        dataThisCompany = self.serializer_class(instance=thisCompanyNews, many=True).data
        allNews = dataDefault + dataThisCompany
        news = query(allNews).order_by_descending(lambda x: x["postDate"]).to_list()[0:1]
        return Response(news)

    @detail_route(methods=["get"])
    def read(self, request, *args, **kwargs):
        instance = News.objects.get(id=kwargs["id"])
        result = self.serializer_class(instance=instance).data
        return Response(result)

    def get_queryset(self):
        return self.queryset.filter(companyID=self.request.user.current_company_id)

    def template_view(self, request):
        return render_to_response('News/base.html', {}, context_instance=RequestContext(request))

    def template_view_blog(self, request):
        return render_to_response('News/NewsList/base.html', {}, context_instance=RequestContext(request))

    def template_view_post(self, request):
        return render_to_response('News/post.html', {}, context_instance=RequestContext(request))

    def template_view_read(self, request):
        return render_to_response('News/read.html', {}, context_instance=RequestContext(request))

    def create(self, request, *args, **kwargs):
        if not request.user.current_company.owner_user == request.user.id:
            return HttpResponseForbidden()
        request.data["companyID"] = request.user.current_company_id
        request.data["positionID"] = GetPositionViewset().GetCurrentPositionDocumentInstance(request).userID
        return super(NewsViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if not request.user.current_company.owner_user == request.user.id:
            return HttpResponseForbidden()
        request.data["companyID"] = request.user.current_company_id
        request.data["positionID"] = GetPositionViewset().GetCurrentPositionDocumentInstance(request).userID
        return super(NewsViewSet, self).update(request, *args, **kwargs)
