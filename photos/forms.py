from django import forms

from .models import Photo, Album
from django.forms import ClearableFileInput


class AlbumUpload(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title','description','category', 'menu', 'author','release_date']

class PhotoUpload(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['file']
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }