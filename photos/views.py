import time

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView

from .forms import PhotoForm, PhotoUpload, AlbumUpload
from .models import Photo


class PhotoList(ListView):
    model = Photo

def upload_photos2(request):
    if request.method == "POST":
        albumform = AlbumUpload(request.POST)
        if albumform.is_valid():
            a = albumform.save()

            photoform = PhotoUpload(request.POST, request.FILES)
            photos = request.FILES.getlist('file')
            if photoform.is_valid():
                for f in photos:
                    file_instance = Photo(file=f, album=a)
                    file_instance.save()
        return redirect('upload-photos')
    else:
        photoform = PhotoUpload()
        albumform = AlbumUpload()
        return render(request, 'photos/add_photo.html', {'photo': photoform, 'album':albumform})

class UploadPhotosView(View):

    def get(self, request):
        return render(self.request, 'photos/upload-photos.html')

    def post(self, request):
        time.sleep(1)
        form = PhotoForm(self.request.POST, self.request.FILES)
        print("before form")
        if form.is_valid():
            print("after form")
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
            print("success")
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


def clear_database(request):
    for photo in Photo.objects.all():
        photo.file.delete()
        photo.delete()
    return redirect(request.POST.get('next'))
