from django import forms

from .models import Photo, PhotoAlbum
from django.forms import ClearableFileInput


class DateInput(forms.DateInput):
    input_type = 'date'

class AlbumUpload(forms.ModelForm):
    class Meta:
        model = PhotoAlbum
        fields = ['title','category', 'menu', 'author','release_date']

class PhotoUpload(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['file']
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }