from django.views.generic import FormView

from news.forms import NewsForm


class AddNewsView(FormView):
    template_name = 'news/add-news.html'
    form_class = NewsForm
    success_url = '/thanks/'

    def form_valid(self, form):
        return super().form_valid(form)
