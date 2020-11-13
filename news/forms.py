from django import forms
from tempus_dominus.widgets import DatePicker
from news.models import News


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'category', 'menu', 'author','release_date', 'image']

