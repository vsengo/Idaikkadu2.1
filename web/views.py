from django.views.generic import ListView

from news.models import News
from photos.models import Photo


class IndexView(ListView):
    # queryset = Photo.objects.order_by('-create_date')
    model = Photo
    context_object_name = 'photos'
    template_name = 'web/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['news'] = News.objects.all().order_by('-create_date')
        context['news_latest'] = News.objects.all().order_by('-create_date').first()
        context['news_international'] = context['news'].filter(category='international').first()
        context['news_srilanka'] = context['news'].filter(category='srilanka').first()
        context['news_jaffna'] = context['news'].filter(category='jaffna').first()
        return context
