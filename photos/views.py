from django.contrib.auth.models import User
from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView
from django.conf import settings

from PIL import Image, ExifTags
import os
from photos.models import Photo, Album, Comment
from photos.forms import AlbumUpload, PhotoUpload, CommentForm
from  datetime import datetime, timedelta

from web.utils import mail_approval
def flip_horizontal(im): return im.transpose(Image.FLIP_LEFT_RIGHT)
def flip_vertical(im): return im.transpose(Image.FLIP_TOP_BOTTOM)
def rotate_180(im): return im.transpose(Image.ROTATE_180)
def rotate_90(im): return im.transpose(Image.ROTATE_90)
def rotate_270(im): return im.transpose(Image.ROTATE_270)
def transpose(im): return rotate_90(flip_horizontal(im))
def transverse(im): return rotate_90(flip_vertical(im))
orientation_funcs = [None,
                 lambda x: x,
                 flip_horizontal,
                 rotate_180,
                 flip_vertical,
                 transpose,
                 rotate_270,
                 transverse,
                 rotate_90
                ]
def apply_orientation(im):
    """
    Extract the oritentation EXIF tag from the image, which should be a PIL Image instance,
    and if there is an orientation tag that would rotate the image, apply that rotation to
    the Image instance given to do an in-place rotation.

    :param Image im: Image instance to inspect
    :return: A possibly transposed image instance
    """

    try:
        kOrientationEXIFTag = 0x0112
        if hasattr(im, '_getexif'): # only present in JPEGs
            e = im._getexif()       # returns None if no EXIF data
            if e is not None:
                #log.info('EXIF data found: %r', e)
                orientation = e[kOrientationEXIFTag]
                f = orientation_funcs[orientation]
                return f(im)
    except:
        # We'd be here with an invalid orientation value or some random error?
        pass # log.exception("Error applying EXIF Orientation tag")
    return im

class PhotoList(ListView):
    model = Album
    context_object_name = 'latest_alum'
    queryset = Album.objects.all().order_by('-id').order_by('-release_date')
    template_name = 'photos/photo_list.html'

    def get_context_data(self, **kwargs):
        context = super(PhotoList, self).get_context_data(**kwargs)
        context['album'] = Album.objects.all().filter(approved='Y').order_by('-id').order_by('-release_date').first()

        latestAlbum = Album.objects.all().filter(approved='Y').order_by('-id').order_by('-release_date').first()
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
            tWidth, tHeight  = 300,200
            pWidth, pHeight = 1200,800

            if photoform.is_valid():
                fig = 1
                albumPath = os.path.join(settings.MEDIA_ROOT,"photos")
                for f in photos:
                    p = Photo(file=f, album=a, figNo=fig)
                    try:
                        fname,ext = os.path.splitext(p.file.name)
                        nfname = today.strftime("%m%dT%H%M%S")+"_"+str(fig)
                        nfthumb = "photos/" + today.strftime("%Y") + "/" + nfname + "_thumb" + ext
                        p.thumb = nfthumb
                        if (fig == 1):
                            a.thumb = nfthumb
                            a.save()

                        p.save()
                        #Rename
                        opath = os.path.join(settings.MEDIA_ROOT,p.file.name)
                        nfname = today.strftime("%Y")+"/"+nfname+ext
                        npath = os.path.join(albumPath,nfname)

                        os.rename(opath, npath)

                        img = Image.open(npath)
                        width, height = img.size
                        if (width > pWidth):
                            nWidth  = pWidth
                            nHeight = pHeight
                            img = apply_orientation(img)
                            img.thumbnail((nWidth, nHeight), Image.HAMMING)
                            img.save(npath)

                        p.file.name = "photos/"+nfname
                        p.save(update_fields=["file"])

                        img.thumbnail((tWidth, tHeight), Image.LANCZOS)
                        tpath=os.path.join(settings.MEDIA_ROOT,nfthumb)
                        img.save(tpath)
                        print("Saved Thumb file" + tpath + " size " + str(tWidth) + "x" + str(tHeight))

                        photolist.append(p)

                        fig += 1
                    except IOError as err:
                        print("Exception file processing album {0}".format(err))
                        pass
                    mail_approval(a.id, 'Album', request)
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

    comments = Comment.objects.all().filter(album_id=album_id).filter(approved='Y').order_by('-id').order_by('-created_on')
    return render(request,'photos/view_album.html', {'photo':photos, 'album':album, 'comments':comments})

def ShowAllAlbum(request):
    today = datetime.now()
    lastTwoYears = today - timedelta(days=2*365)

    international = Album.objects.all( ).filter(section="F").filter(approved='Y').order_by('-id').order_by('-release_date')[:10]
    srilanka = Album.objects.all( ).filter(section="S").filter(approved='Y').order_by('-id').order_by('-release_date')[:10]
    idaikkadu = Album.objects.all( ).filter(section="I").filter(approved='Y').order_by('-id').order_by('-release_date')[:10]

    return render(request,'photos/show_album.html',{'international':international, 'idaikkadu':idaikkadu,'srilanka':srilanka})

def UpdateAlbum(request):
    albums = Album.objects.all( )[:20]
    return render(request,'photos/update_albums.html',{'albums':albums})

def ApproveAlbum(request, album_id):
        album = Album.objects.filter(id=album_id).first( )
        album.approved = 'Y'
        album.save( )
        return render(request, 'photos/album_status.html', {'album': album})

def DeleteAlbum(request, album_id):
    album = Album.objects.filter(id=album_id).first( )
    album.delete( )
    return render(request, 'photos/album_status.html', {'album': album})

def PostComment(request, pk):
    template_name = 'photos/album_comment.html'
    post = get_object_or_404(Album, id=pk)
    comments = Comment.objects.all().filter(album_id=pk).filter(approved='Y')
    new_comment = None

    badWords = ["http", "sex", "fuck"]
    # Comment posted

    if request.method == 'POST':
        member = User.objects.all( ).filter(username=request.user.username).first( )
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.album_id = pk
            save = True
            if member:
                new_comment.name = member.first_name
                new_comment.approved='Y'
            else:
                for str in badWords:
                    if str in new_comment.body:
                        print("WARN : Ignored bad comment from "+new_comment.name+". Comment had bad word:"+str)
                        save  = False
                        break

           # Save the comment to the database
            if save:
               new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post_id': post.id,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})

def LikeAlbum(request, pk):
    album = get_object_or_404(Album, id=pk)
    album.countLike +=1
    album.save()
    return HttpResponseRedirect(reverse('photos:view-album',args=[str(pk)]))

class ApproveCommentList(ListView):
    model = Comment
    template_name = 'photos/album_comment_approve.html'

    def get_queryset(self):
       return Comment.objects.filter(approved='N').order_by('-created_on')

def DeleteComment(request, pk):
    comment = Comment.objects.filter(id=pk).first()
    comment.delete()
    return HttpResponseRedirect(reverse('photos:comment-album-approvelist'))

def ApproveComment(request, pk):
    comment = Comment.objects.filter(id=pk).first()
    comment.approved = 'Y'
    comment.save()
    return HttpResponseRedirect(reverse('photos:comment-album-approvelist'))
