
from django import forms

from .models import Photo
from .models import Album

class DateInput(forms.DateInput):
    input_type = 'date'

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title','author','email','menu','release_date']
        widgets = {
            'release_date': DateInput(),
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('file', )
