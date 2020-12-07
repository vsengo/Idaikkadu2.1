from django import forms

from .models import Photo, Album
from django.forms import ClearableFileInput


class AlbumUpload(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title','description','region', 'menu', 'author','release_date']

    def clean(self):
        super(AlbumUpload,self).clean()

        region = self.cleaned_data.get('region')
        if region == 'idaikkadu':
            self.instance.section = 'I'
        elif region == 'jaffna' or region == 'srilanka':
            self.instance.section = 'S'
        else:
            self.instance.section ='F'


class PhotoUpload(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['file']
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }