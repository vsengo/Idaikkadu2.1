from django.shortcuts import render

from news import forms
from news.forms import NewsForm


def create(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = forms.NewsForm(request.POST, request.FILES)
        print("before valid")
        if form.is_valid():
            print("valid")
            form.save()

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewsForm()

    return render(request, 'index.html', {'form': form})
