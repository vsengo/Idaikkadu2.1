import time
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
import logging


from .forms import PhotoForm
from .forms import AlbumForm
from .models import Photo
from .models import Album

logger = logging.getLogger(__name__)


def load_photoform(request):
    photos_list = Photo.objects.filter(album_id__isnull=True)
    return render(request, 'photos/progress_bar_upload/photoupload.html', {'photos': photos_list})

class AlbumView(View):
    def get(self, request):
        albumform = AlbumForm()
        return render(self.request, 'photos/progress_bar_upload/createalbum.html', {'albumform':albumform})

    def post(self,request):
        photos_list = Photo.objects.filter(album_id__isnull=True)
        if "cancel" in request.POST:
            return render(request, 'photos/progress_bar_upload/photoupload.html', {'photos': photos_list})
        else:
            albumform = AlbumForm(request.POST)
            if albumform.is_valid():
                album=albumform.save()
                count = 0
                for photo in photos_list:
                    photo.album = album
                    photo.save()
                    count +=1
                return HttpResponse("Alnum is saved with " +str(count) + " Photos")

def choose_album(request):
    album_list = Album.objects.filter()
    return render(request, 'photos/progress_bar_upload/choosealbum.html', {'albums': album_list})

def add_to_album(request):
    albumid = request.POST.get("AlbumID","empty")
    photos_list = Photo.objects.filter(album_id__isnull=True)

    albumList = Album.objects.filter(id=albumid)
    if len(albumList) > 0:
        album=albumList[0]
        count =0
        for photo in photos_list:
            photo.album = album
            photo.save()
            count += 1
        return HttpResponse(str(count)+" Photos saved to Album "+ album.title)
    else:
        return HttpResponse("Could not find Album in the Database")

def get_description(request):
    albumform = AlbumForm()
    return render(request, 'photos/progress_bar_upload/createalbum.html', {'albumform': albumform})

class ProgressBarUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.filter(album_id__isnull=True)
        return render(self.request, 'photos/progress_bar_upload/createalbum.html', {'photos': photos_list})

    def post(self, request):
        time.sleep(100)
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

def clear_database(request):
        for photo in Photo.objects.filter(album_id__isnull=True):
            photo.file.delete()
            photo.delete()
        return redirect(request.POST.get('next'))