from django import forms
from django.forms import ModelForm

from news.models import News


class NewsForm(forms.ModelForm):
    title = forms.CharField()
    content = forms.CharField()

    class Meta:
        model = News
        fields = ('title', 'content', 'image', )
