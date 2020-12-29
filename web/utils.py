from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from news.models import News

from photos.models import Album


def mail_approval(id, newsType, request):
    approvers = User.objects.filter(is_staff=1)
    contributor = User.objects.filter(username=request.user).first()
    siteName = "http://"+request.get_host()

    subject="Idaikkadu.com News Approval Request"
    if approvers.exists():
        toList = list()
        for user in approvers:
            toList.append(user.email)

        if newsType == 'News':
            news = News.objects.filter(id = id)[0]
            c = {
                "contentType": "News",
                "title": news.title,
                "content" : news.content,
                'author': news.author,
                'updatedBy' : contributor.first_name +" " + contributor.last_name,
                'release_date':news.release_date,
                "detail_url" : siteName
            }

        if newsType == 'Album':
            album = Album.objects.filter(id=id)[0]
            c = {
                "contentType" :"Album",
                "title": album.title,
                "content": album.description,
                'author': album.author,
                'updatedBy' : contributor.first_name +" " + contributor.last_name,
                'release_date': album.release_date,
                "detail_url": siteName
            }

        text_msg = render_to_string('web/approval_mail.txt',c)
        html_msg = render_to_string('web/approval_mail.html',c)
        try:
                send_mail(subject, text_msg, 'accounts@idaikkadu.com', toList, fail_silently=False,html_message=html_msg)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')

