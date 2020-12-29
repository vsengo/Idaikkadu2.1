from django import forms
from news.models import News, Comment

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'region', 'menu', 'author','release_date', 'image', 'link']

    def clean(self):

        cleaned_data = super(NewsForm,self).clean()
        region = cleaned_data.get('region')
        if region == 'idaikkadu':
            self.instance.section = 'I'
        elif region == 'jaffna' or region == 'srilanka':
            self.instance.section = 'S'
        else:
            self.instance.section = 'F'
        return cleaned_data

class CommentForm(forms.ModelForm):
        class Meta:
            model = Comment
            fields = ('name', 'body')

