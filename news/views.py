from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from  datetime import datetime
import os
from PIL import Image, ExifTags
from news.forms import NewsForm
from news.models import News
from photos.views import apply_orientation


class NewsList(ListView):
    model = News
    template_name = 'news/news_update.html'
    def get_queryset(self):
        return News.objects.filter()[:20]

class AddNewsView(CreateView):
    template_name = 'news/add_news.html'
    form_class = NewsForm
    success_url = 'success-news'

    def form_valid(self, form):
        response = super().form_valid(form)
        news = form.instance

        today = datetime.now( )
        twidth, theight = 300, 300
        fname, ext = os.path.splitext(news.image.name)

        opath = fname + ext
        npath = "news/" + today.strftime("%Y") + "/" + today.strftime("%m%d%H%M") + ext
        try:
            img = Image.open("media/" + opath)
            width, height = img.size
            if (width > twidth):
                img = apply_orientation(img)
                img.thumbnail((twidth, theight), Image.HAMMING)
                img.save("media/" + opath)

            os.rename("media/" + opath, "media/"+npath)
            news.image.name=npath
            news.save(update_fields=["image"])
            print("Updated opath " + opath + " to " + npath)
        except IOError as err:
            print("Exception file processing image {0}".format(err))
            pass
        return response

class NewsUpdate(UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news/add_news.html'
    success_url = reverse_lazy('news:success-news')

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

def SuccessNews(request):
    return render(request, 'news/Success.html')

class NewsReject(DeleteView):
    model = News
    success_url = reverse_lazy('news:news_list')

def getDetailNews(request, pk=2):
        dnews = News.objects.all().filter(id=pk).first()
        return render(request,'news/news_detail.html',{'news':dnews})

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
