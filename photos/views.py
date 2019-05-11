import time

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView

from .forms import PhotoForm
from .models import Photo


class PhotoList(ListView):
    model = Photo


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
