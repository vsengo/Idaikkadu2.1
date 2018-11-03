from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.

def index(request):
    return render(request, "root/index.html")


def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        #serializer = NewsSerializer(form)
        #serializer.save()
        return HttpResponse("Thank you")
    else :
        form = NewsForm()
        return render(request,"news_form.html",{'form':form})