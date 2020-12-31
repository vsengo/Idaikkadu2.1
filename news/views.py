from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.urls import  reverse
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from  datetime import datetime
import os
from PIL import Image, ExifTags
from news.forms import NewsForm, CommentForm
from news.models import News, Comment
from photos.views import apply_orientation
from web.utils    import mail_approval

class NewsList(ListView):
    model = News
    template_name = 'news/news_update.html'
    def get_queryset(self):
        return News.objects.filter().order_by('-id').order_by('-release_date')[:20]

class AddNewsView(CreateView):
    template_name = 'news/add_news.html'
    form_class = NewsForm
    success_url = 'success-news'

    def form_valid(self, form):
        response = super().form_valid(form)
        news = form.instance

        if news.image:
            today = datetime.now()
            twidth, theight = 600, 800
            fname, ext = os.path.splitext(news.image.name)

            opath = fname + ext
            npath = "news/" + today.strftime("%Y") + "/" + today.strftime("%m%dT%H%M%S") + ext
            try:
                img = Image.open("media/" + opath)
                width, height = img.size
                if (width > twidth):
                    img = apply_orientation(img)
                    img.thumbnail((twidth, theight), Image.HAMMING)
                    img.save("media/" + opath)

                os.rename("media/" + opath, "media/" + npath)
                news.image.name = npath
                news.save(update_fields=["image"])

            except IOError as err:
                print("Exception file processing image {0}".format(err))
                pass

        mail_approval(news.id,'News', self.request)

        return response

class NewsUpdate(UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news/add_news.html'

    success_url = reverse_lazy('news:success-news')

    def get_queryset(self):
        return News.objects.filter(id=self.kwargs['pk'])


def DeleteNews(request, pk):
    news = News.objects.filter(id=pk).first()
    news.delete()
    return render(request, 'news/news_status.html', {'news': news})


def ApproveNews(request, pk):
    news = News.objects.filter(id=pk).first()
    news.approved = 'Y'
    news.save()
    return render(request, 'news/news_status.html', {'news': news})


def SuccessNews(request):
    return render(request, 'news/success.html')


class NewsReject(DeleteView):
    model = News
    success_url = reverse_lazy('news:news_list')


class DetailNewsView(DetailView):
    model = News
    template_name = 'news/news_detail.html'

    def get_template_names(self):
        if self.object.menu == 'Obituary':
            return  ['news/news_obituary.html']
        else:
            return ['news/news_detail.html']

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['news'] = News.objects.all().filter(id=self.kwargs['pk']).first()
        context['comments'] = Comment.objects.all().filter(news_id=self.kwargs['pk']).order_by('-id').order_by('-created_on')
        return context


def getDetailNews(request, news_id=2):
    news = News.objects.all().filter(id=news_id)
    return render(request, 'news/news_detail.html', {'news_latest': news})


class IdaikkaduNewsView(ListView):
    model = News

    def get_queryset(self):
        return News.objects.filter(section='I').filter(approved='Y').order_by('-id').order_by('-release_date')


class SrilankaNewsView(ListView):
    model = News

    def get_queryset(self):
        return News.objects.filter(section='S').filter(approved='Y').order_by('-id').order_by('-release_date')


class InternationalNewsView(ListView):
    model = News

    def get_queryset(self):
        return News.objects.filter(section='F').filter(approved='Y').order_by('-id').order_by('-release_date')


def BlogPostLike(request, pk):
    print("id = "+str(pk))
    news = get_object_or_404(News, id=pk)
    news.countLike +=1
    news.save()
    return HttpResponseRedirect(reverse('news:detail-news', args=[str(pk)]))


def PostComment(request, pk):
    template_name = 'news/news_comment.html'
    post = get_object_or_404(News, id=pk)
    comments = Comment.objects.all().filter(news_id=pk).filter(approved='Y')
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        member = User.objects.all().filter(username=request.user.username).first()

        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.news_id = pk
            if member:
                new_comment.name = member.first_name
                new_comment.approved='Y'
            # Save the comment to the database
            new_comment.save()
        else:
            print("Could not save comment by {}".format(request.user.username))
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})

class ApproveCommentList(ListView):
    model = Comment
    template_name = 'news/news_comment_approve.html'

    def get_queryset(self):
       return Comment.objects.filter(approved='N').order_by('-created_on')

def DeleteComment(request, pk):
    comment = Comment.objects.filter(id=pk).first()
    comment.delete()
    return HttpResponseRedirect(reverse('news:comment-approvelist'))


def ApproveComment(request, pk):
    comment = Comment.objects.filter(id=pk).first()
    comment.approved = 'Y'
    comment.save()
    return HttpResponseRedirect(reverse('news:comment-approvelist'))