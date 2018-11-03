import time

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.views import View
import logging


from .forms import PhotoForm
from .forms import AlbumForm
from .models import Photo
from .models import Album

logger = logging.getLogger(__name__)


class PhotoView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'photos/progress_bar_upload/photoupload.html',{'photos':photos_list})

    def post(self, request):
        time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.

        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

class AlbumView(View):
    def get(self, request):
        albumform = AlbumForm()
        return render(request, 'photos/progress_bar_upload/index.html', {'albumform':albumform})

    def post(self,request):
        albumform = AlbumForm(request.POST)
        if albumform.is_valid():
            album=albumform.save()

        return render(request, 'photos/progress_bar_upload/index.html', {'albumform': albumform})

def get_description(request):
        albumform = AlbumForm()
        return render(request, 'photos/progress_bar_upload/index.html', {'albumform': albumform})