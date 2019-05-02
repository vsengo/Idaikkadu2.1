from django.views.generic import ListView
from photos.models import Photo


class IndexView(ListView):
    queryset = Photo.objects.order_by('-create_date')
    context_object_name = 'photos'
    template_name = 'web/index.html'
