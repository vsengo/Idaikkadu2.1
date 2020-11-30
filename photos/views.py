from django.shortcuts import redirect, render
from django.views.generic import ListView
from PIL import Image
from photos.models import Photo, Album
from photos.forms import AlbumUpload, PhotoUpload
import datetime

class PhotoList(ListView):
    model = Album
    context_object_name = 'latest_alum'
    queryset = Album.objects.all().order_by('-release_date')
    template_name = 'photos/photo_list.html'

    def get_context_data(self, **kwargs):
        context = super(PhotoList, self).get_context_data(**kwargs)
        context['album'] = Album.objects.all().order_by('-release_date').first()

        latestAlbum = Album.objects.all().order_by('-release_date').first()
        context['photos'] = Photo.objects.all().filter(album=latestAlbum)
        context['title'] = latestAlbum.title
        return context


def AddAlbum(request):
    if request.method == "POST":
        albumform = AlbumUpload(request.POST)
        if albumform.is_valid():
            a = albumform.save()

            photoform = PhotoUpload(request.POST, request.FILES)
            photos = request.FILES.getlist('files[]')
            photolist = list()
            today = datetime.datetime.now()

            if photoform.is_valid():
                fig = 1
                for f in photos:
                    p = Photo(file=f, album=a, figNo=fig)
                    try:
                        n = f.name.find(".")
                        nf = "photos/"+today.strftime("%Y")+"/"+f.name[:n]+"_thumb.jpg"
                        print("Thum nail File Name : "+nf)
                        p.thumb=nf
                        p.save()
                        img  = Image.open(f.file)
                        img.thumbnail((90,90))

                        img.save("media/"+nf)

                        photolist.append(p)
                        fig += 1
                    except IOError:
                        pass
                return render(request,'photos/success.html', {'album':a})
        else:
            return render(request, 'photos/failed.html')
    else:
        photoform = PhotoUpload()
        albumform = AlbumUpload()
        print("DEBUG")
        return render(request, 'photos/add_photo.html', {'photo': photoform, 'album':albumform})

