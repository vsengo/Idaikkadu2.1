from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView


from news.models import News
from photos.models import Photo, Album


class IndexView(ListView):
    context_object_name = 'news'
    queryset = News.objects.all().order_by('-release_date')
    template_name = 'web/index.html'

    method_decorator(csrf_protect)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        news = News.objects.all().order_by('-release_date').order_by('-id')
        context['news'] = news
        context['news_latest'] = context['news'].first()
        news_latest_id = context['news'].first( ).id
        context['news_old'] = context['news'].exclude(id=news_latest_id)[:3]

        international = context['news'].exclude(id=news_latest_id).filter(category='international')
        context['international_new'] = international.first()
        context['international_old'] = international.exclude(id = context['international_new'].id)[:5]

        strilanka = context['news'].exclude(id=news_latest_id).filter(category='srilanka')
        context['srilanka_new'] = strilanka.first()
        context['srilanka_old'] = strilanka[:5]

        idaikkadu = context['news'].exclude(id=news_latest_id).filter(category='idaikkadu')
        context['idaikkadu_new'] = idaikkadu.first()
        context['idaikkadu_old'] = idaikkadu[:5]

        context['albums'] = Album.objects.all().order_by('-release_date').order_by('-id')
        context['latest_album'] = context['albums'].first()
        context['photos'] = Photo.objects.all().filter(album_id=context['latest_album'].id)

        album_old = context['albums'].exclude(id=context['latest_album'].id)[:3]
        context['album_old']  = album_old

        return context
