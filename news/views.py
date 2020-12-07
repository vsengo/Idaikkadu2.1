from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from news.forms import NewsForm
from news.models import News


class NewsList(ListView):
    model = News
    def get_queryset(self):
        return News.objects.filter()[:20]

class AddNewsView(CreateView):
    template_name = 'news/add-news.html'
    form_class = NewsForm
    success_url = 'detail-news'

    def form_valid(self, form):
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news/add-news.html'
    success_url = reverse_lazy('news:news_list')

    def get_queryset(self):
        return News.objects.filter(id=self.kwargs['pk'])


def DeleteNews(request, pk):
        news=News.objects.filter(id=pk).first()
        news.approved='N'
        news.save()
        return render(request, 'news/news_status.html', {'news': news})

def ApproveNews(request, pk):
        news=News.objects.filter(id=pk).first()
        news.approved='Y'
        news.save()
        return  render(request,'news/news_status.html',{'news':news})


class NewsReject(DeleteView):
    model = News
    success_url = reverse_lazy('news:news_list')

class DetailNewsView(DetailView):
    model = News
    template_name = 'news/news_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailNewsView, self).get_context_data(**kwargs)
        return context

def getDetailNews(request, news_id=2):
        news = News.objects.all().filter(id=news_id)
        return render(request,'news/news_detail.html',{'news_latest':news})

class IdaikkaduNewsView(ListView):
    model = News

    def get_queryset(self):
        return News.objects.filter(section='I')


class SrilankaNewsView(ListView):
    model = News

    def get_queryset(self):
        return News.objects.filter(section='S')


class InternationalNewsView(ListView):
    model = News

    def get_queryset(self):
        return News.objects.filter(section='F')
