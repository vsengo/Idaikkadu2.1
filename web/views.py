from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from web.models import News, Album, Comment
from web.forms import NewsForm, AlbumForm

# Create your views here.

def index(request):
    return render(request, "root/index.html")


def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        #serializer = NewsSerializer(form)
        #serializer.save()
        return HttpResponse("Thank you")
    else :
        form = NewsForm()
        return render(request,"news_form.html",{'form':form})

def add_album (request):
    if request.method == 'POST':
       form = AlbumForm(self.request.POST, self.request.FILES)
       if form.is_valid():
           photo = form.save()
           data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
       else:
           data = {'is_valid': False}
       return JsonResponse(data)
    else :
        photos_list = Album.objects.all()
        return render(request, 'album/index.html', {'photos': photos_list})

class ProgressBarUploadView(View):
        def get(self, request):
            photos_list = Album.objects.all()
            return render(self.request, 'album/index.html', {'album': photos_list})

        def post(self, request):
            time.sleep(
                1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
            form = AlbumForm(self.request.POST, self.request.FILES)
            if form.is_valid():
                photo = form.save()
                data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
            else:
                data = {'is_valid': False}
            return JsonResponse(data)