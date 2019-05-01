from django.http import HttpResponse
from django.shortcuts import render

from photos.models import Photo
from web.forms import NewsForm


# Create your views here.


def index(request):
    photos_list = Photo.objects.all().order_by('-create_date')
    # news_list = News.objects.all().order_by('-create_date').first()
    return render(request, 'web/index.html', {'photos': photos_list})


def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        # serializer = NewsSerializer(form)
        # serializer.save()
        return HttpResponse("Thank you")
    else:
        form = NewsForm()
        return render(request, "news_form.html", {'form': form})

# def add_album(request):
#     if request.method == 'POST':
#         form = AlbumForm(self.request.POST, self.request.FILES)
#         if form.is_valid():
#             photo = form.save()
#             data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
#         else:
#             data = {'is_valid': False}
#         return JsonResponse(data)
#     else:
#         photos_list = Album.objects.all()
#         return render(request, 'album/index.html', {'photos': photos_list})
#
#
# class ProgressBarUploadView(View):
#     def get(self, request):
#         photos_list = Album.objects.all()
#         return render(self.request, 'album/index.html', {'album': photos_list})
#
#     def post(self, request):
#         time.sleep(
#             1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
#         form = AlbumForm(self.request.POST, self.request.FILES)
#         if form.is_valid():
#             photo = form.save()
#             data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
#         else:
#             data = {'is_valid': False}
#         return JsonResponse(data)
