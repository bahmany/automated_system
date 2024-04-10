from django.conf.urls import patterns, include, url
from rest_framework.routers import SimpleRouter
from amspApp.News.views.NewsView import NewsViewSet

news_router = SimpleRouter()
news_router.register("news", NewsViewSet, base_name="news-list")

urlpatterns = patterns('',
                       url(r'^page/newsread', NewsViewSet.as_view({"get": "template_view_read"})),
                       url(r'^page/newspost', NewsViewSet.as_view({"get": "template_view_post"})),
                       url(r'^page/newsBlog', NewsViewSet.as_view({"get": "template_view_blog"})),
                       url(r'^page/news', NewsViewSet.as_view({"get": "template_view"})),
                       url(r'^api/v1/', include(news_router.urls)),
                       )
