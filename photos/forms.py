
from django import forms

from .models import Photo

class DateInput(forms.DateInput):
    input_type = 'date'

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title','author','email','menu','link','file']
        widgets = {
            'release_date': DateInput(),
        }
