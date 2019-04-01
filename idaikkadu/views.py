from django.shortcuts import render
from django.views import View

from news.models import News
from photos.models import Photo


class home(View):
    def get(self, request):
        photos_list = Photo.objects.all().order_by('-create_date')
        news_list = News.objects.all().order_by('-create_date').first()
        return render(self.request, 'home.html', {'photos': photos_list, 'news': news_list})
