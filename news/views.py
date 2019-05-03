from django.http import HttpResponseRedirect
from django.shortcuts import render
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
