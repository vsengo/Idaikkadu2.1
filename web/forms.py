from django.db import models
from django import forms
from django.forms import ModelForm
from web.models import Content,Comment

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class DateInput(forms.DateInput):
    input_type = 'date'


class ContentForm(ModelForm):
    class Meta:
        model = Content
        exclude = ['countLike', 'countDisLike','approved']
        widgets = {
            'release_date': DateInput(),
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'updated_by']
