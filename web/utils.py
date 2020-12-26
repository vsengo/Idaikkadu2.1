from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from news.models import News

from photos.models import Album


def mail_approval(id, newsType):
    approvers = User.objects.filter(is_staff=1)
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
                'release_date':news.release_date,
                "detail_url" : "http://localhost:8000/news/update-news/"
            }

        if newsType == 'Album':
            album = Album.objects.filter(id=id)[0]
            c = {
                "contentType" :"Album",
                "title": album.title,
                "content": album.description,
                'author': album.author,
                'release_date': album.release_date,
                "detail_url": "http://localhost:8000/photos/update-album/"
            }

        text_msg = render_to_string('web/approval_mail.txt',c)
        html_msg = render_to_string('web/approval_mail.html',c)
        try:
                send_mail(subject, text_msg, 'accounts@idaikkadu.com', toList, fail_silently=False,html_message=html_msg)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')

