from django.db import models
from django import forms
from django.forms import ModelForm
from web.models import News, Album, Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class DateInput(forms.DateInput):
    input_type = 'date'


class NewsForm(ModelForm):
    class Meta:
        model = News
        exclude = ['countLike', 'countDisLike','imageDir','approved']
        widgets = {
            'release_date': DateInput(),
        }

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
