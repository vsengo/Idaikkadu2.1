from django import forms
from tempus_dominus.widgets import DatePicker
from news.models import News

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'region', 'menu', 'author','release_date', 'image']

    def clean(self):
        super(NewsForm,self).clean()

        region = self.cleaned_data.get('region')
        if region == 'idaikkadu':
            self.instance.section = 'I'
        elif region == 'jaffna' or region == 'srilanka':
            self.instance.section = 'S'
        else:
            self.instance.section ='F'

