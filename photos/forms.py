from django import forms

from .models import Photo
from django.forms import ClearableFileInput


class DateInput(forms.DateInput):
    input_type = 'date'


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['file']
        widgets = {
            'release_date': DateInput(),
        }


class PhotoUpload(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['file', 'album']
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }