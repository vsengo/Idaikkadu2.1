from django.shortcuts import redirect, render
from django.views.generic import ListView
from photos.models import Photo
from photos.forms import AlbumUpload, PhotoUpload

class PhotoList(ListView):
    model = Photo

def Success(request):
    return render(request,'photos/success.html')

def AddAlbum(request):
    if request.method == "POST":
        albumform = AlbumUpload(request.POST)
        if albumform.is_valid():
            a = albumform.save()

            photoform = PhotoUpload(request.POST, request.FILES)
            photos = request.FILES.getlist('files[]')
            photolist = list()
            if photoform.is_valid():
                fig = 1
                for f in photos:
                    file_instance = Photo(file=f, album=a, figNo=fig)
                    file_instance.save()
                    photolist.append(file_instance)
                    fig += 1
                return render(request,'photos/success.html')
        else:
            return render(request, 'photos/photo_list.html', {'photo_list': photos})
    else:
        photoform = PhotoUpload()
        albumform = AlbumUpload()
        return render(request, 'photos/add_photo.html', {'photo': photoform, 'album':albumform})

