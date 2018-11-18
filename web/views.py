from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from  web.forms  import ContentForm
from  web.models import Content
import logging

logger = logging.getLogger(__name__)

def add_news(request):
    if request.method == 'POST':
        form = ContentForm(request.POST,request.FILES)
        files = request.POST.get('imageDir','')
        form.imageDir = files

        logger.info("image DIR "+form.imageDir)

        if  form.is_valid():
           news=form.save()
           return HttpResponse("Thank you. News "+news.title + " is aaved to Database")
        else:
            response = form.errors.as_json()
            return JsonResponse(form.errors)

    else :
        form = ContentForm()
        return render(request,"web/news_form.html",{'form':form})