from django import forms
from tempus_dominus.widgets import DatePicker
from news.models import News

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'category', 'menu', 'author','release_date', 'image']

    def clean(self):
        super(NewsForm,self).clean()

        category = self.cleaned_data.get('category')
        if category == 'idaikkadu':
            self.instance.section = 'I'
        elif category == 'jaffna' or category == 'srilanka':
            self.instance.section = 'S'
        else:
            self.instance.section ='F'

