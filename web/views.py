from django.urls import reverse
from django.views.generic import ListView

from news.models import News
from photos.models import Photo


class IndexView(ListView):
    #queryset = Photo.objects.order_by('-create_date')
    model = Photo
    context_object_name = 'photos'
    template_name = 'web/index.html'


    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['news'] = News.objects.all().order_by('-create_date')
        context['newsLatest'] = News.objects.all().order_by('-create_date').first().title
        context['newsInternational'] = context['news'].filter(category='international').first().title
        context['newsSrilanka'] = context['news'].filter(category='srilanka').first().title
        context['newsIdaikkadu'] = context['news'].filter(category='idaikkadu').first().title
        context['newsIdaikkaduId'] = context['news'].filter(category='idaikkadu').first().id
        return context
