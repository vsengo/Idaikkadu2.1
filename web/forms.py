from django import forms
from django.forms import ModelForm

from web.models import News, Album, Comment


class DateInput(forms.DateInput):
    input_type = 'date'




class AlbumForm(ModelForm):

    class Meta:
        model = Album
        fields = ['title','author','email','menu','link','photos']
        widgets = {
            'release_date': DateInput(),
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'updated_by']
