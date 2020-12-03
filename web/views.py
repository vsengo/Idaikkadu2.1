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

        news_latest_id = context['news'].first().id

        context['news_international'] = context['news'].filter(category='international').first()
        context['news_srilanka'] = context['news'].filter(category='srilanka').first()
        context['news_idaikkadu'] = context['news'].filter(category='idaikkadu').first()


        news_old = context['news'].exclude(id=news_latest_id)[:3]
        #context['news_international'] = news_old.filter(category='international').first()
        #context['news_srilanka'] = news_old.filter(category='srilanka').first()
        context['news_old'] = news_old

        context['albums'] = Album.objects.all().order_by('-release_date').order_by('-id')
        context['latest_album'] = context['albums'].first()
        context['photos'] = Photo.objects.all().filter(album_id=context['latest_album'].id)

        album_old = context['albums'].exclude(id=context['latest_album'].id)[:3]
        context['album_old']  = album_old

        return context
