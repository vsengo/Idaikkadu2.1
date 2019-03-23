from django.shortcuts import render
from django.views import View

from photos.models import Photo


class home(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'home.html', {'photos': photos_list})
