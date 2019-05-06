from django.views.generic import ListView, CreateView

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


class DetailNewsView(ListView):
    model = News
    def get_queryset(self):
        return News.objects.filter(id=self.kwargs['pk'])

class JaffnaNewsView(ListView):
    model = News
    def get_queryset(self):
        return News.objects.filter(category = 'jaffna')

class SrilankaNewsView(ListView):
    model = News
    def get_queryset(self):
        return News.objects.filter(category = 'srilanka')

class InternationalNewsView(ListView):
    model = News
    def get_queryset(self):
        return News.objects.filter(category = 'international')
