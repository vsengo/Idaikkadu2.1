from django.shortcuts import redirect, render
from django.views.generic import ListView
from PIL import Image
from photos.models import Photo, Album
from photos.forms import AlbumUpload, PhotoUpload
from  datetime import datetime, timedelta

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
            a = albumform.save(commit=False)

            photoform = PhotoUpload(request.POST, request.FILES)
            photos = request.FILES.getlist('files[]')
            photolist = list()
            today = datetime.now()

            if photoform.is_valid():
                fig = 1
                newHeight = 360
                newWidth = 300
                newRatio = newWidth/newHeight

                for f in photos:
                    p = Photo(file=f, album=a, figNo=fig)
                    try:
                        n = f.name.find(".")
                        nf = "photos/"+today.strftime("%Y")+"/"+f.name[:n]+"_thumb.jpg"
                        print("Thumb nail File Name : "+nf)
                        p.thumb=nf
                        if (fig == 1):
                            a.thumb = nf
                            a.save()
                        p.save()
                        img  = Image.open(f.file)
                        width,height = img.size
                        aspRatio  = width/height

                        if newRatio == aspRatio:
                           img.thumbnail((newWidth,newHeight),Image.LANCZOS)
                        else:
                            nh = round(newWidth/aspRatio)
                            img.thumbnail((newWidth,nh),Image.LANCZOS)
                            print("Old :"+str(width)+"x"+str(height)+" New :"+str(newWidth)+"x"+str(nh))

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
        return render(request, 'photos/add_photo.html', {'photo': photoform, 'album':albumform})


def ViewAlbum(request, album_id):
    if int(album_id) > 0:
        album = Album.objects.all( ).filter(id=album_id).first()
        photos = Photo.objects.all().filter(album_id=album_id)
    else:
        album = Album.objects.all( ).order_by(-release_date).first()
        photos = Photo.objects.all( ).filter(album_id=album.id)

    figNo = 1
    total = 0
    for p in photos:
        if figNo > 4:
            figNo = 1
        p.figNo = figNo
        figNo += 1
        total += 1
        print("Album ID "+album_id + " Total img:"+str(total)+ " FigNo :"+str(p.figNo) + " title "+album.title)
    return render(request,'photos/view_album.html', {'photo':photos, 'album':album})

def ShowAllAlbum(request):
    today = datetime.now()
    lastTwoYears = today - timedelta(days=2*365)

    international = Album.objects.all( ).filter(category = "international")[:20]
    srilanka = Album.objects.all( ).filter(category = "srilanka")[:20]
    idaikkadu = Album.objects.all( ).filter(category = "idaikkadu")[:20]

    return render(request,'photos/show_album.html',{'international':international, 'idaikkadu':idaikkadu,'srilanka':srilanka})
