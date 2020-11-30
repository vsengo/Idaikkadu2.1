from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from news.forms import NewsForm
from news.models import News


class NewsList(ListView):
    model = News


class AddNewsView(CreateView):
    template_name = 'news/add-news.html'
    form_class = NewsForm
    success_url = 'view-news'

    def form_valid(self, form):
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news/add-news.html'
    success_url = reverse_lazy('news:news_list')

    def get_queryset(self):
        return News.objects.filter(id=self.kwargs['pk'])


class NewsDelete(DeleteView):
    model = News
    success_url = reverse_lazy('news:news_list')


class DetailNewsView(DetailView):
    model = News
    template_name = 'news/news_detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailNewsView, self).get_context_data(**kwargs)
        context['news_detail'] = News.objects.all().filter(id=self.kwargs['pk'])
        context['news_title'] = context['news_detail'].first().title
        context['news_content'] = context['news_detail'].first().content
        context['news_category'] = context['news_detail'].first().category
        return context

class JaffnaNewsView(ListView):
    model = News

    def get_queryset(self):
        return News.objects.filter(category='jaffna')


class SrilankaNewsView(ListView):
    model = News

    def get_queryset(self):
        return News.objects.filter(category='srilanka')


class InternationalNewsView(ListView):
    model = News

    def get_queryset(self):
        return News.objects.filter(category='international')
