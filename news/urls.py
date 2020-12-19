from django.conf.urls import url
from django.urls import path
from django.contrib.auth.decorators import permission_required

from news.views import AddNewsView
from . import views

app_name = 'news'

urlpatterns = [
    url(r'^add-news', permission_required('user.view_add_delete')(views.AddNewsView.as_view()), name='add-news'),
    url(r'^update-news', views.NewsList.as_view(), name='update-news'),
    url(r'^detail-news/(?P<pk>\d)', views.DetailNewsView.as_view(), name='detail-news'),
    url(r'^idaikkadu-news', views.IdaikkaduNewsView.as_view(), name='idaikkadu-news'),
    url(r'^srilanka-news', views.SrilankaNewsView.as_view(), name='srilanka-news'),
    url(r'^international-news', views.InternationalNewsView.as_view(), name='international-news'),
    url(r'^edit-news/(?P<pk>\d+)', views.NewsUpdate.as_view(), name='edit-news'),
    url(r'^delete-news/(?P<pk>\d+)', views.DeleteNews, name='delete-news'),
    url(r'^approve-news/(?P<pk>\d+)', views.ApproveNews, name='approve-news'),
    url(r'^success-news', views.SuccessNews, name='success-news'),
    url(r'^like-news/(?P<pk>\d)', views.BlogPostLike, name='like-news'),
]
