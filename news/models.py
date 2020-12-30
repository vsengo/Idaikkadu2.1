import datetime
from django.db import models
from django.contrib.auth.models import User

from web.choices import choice


class News(models.Model):
    title = models.CharField(max_length=256, blank=True, help_text="Short Title")
    content = models.TextField(max_length=10000)
    image = models.ImageField(upload_to='news/%Y', blank=True, null=True)
    author = models.CharField(max_length=128, help_text="Author of the News or Article")
    email = models.EmailField(null=True)
    region = models.CharField(max_length=32, default='idaikkadu', choices=choice.REGION_CHOICES)
    menu = models.CharField(max_length=16, default='N', choices=choice.MENU_CHOICES)
    section = models.CharField(max_length=1, default='D', choices=choice.SECTION_CHOICES)
    link = models.URLField(blank=True, null=True, help_text="Optional: any link to share")
    approved = models.CharField(max_length=1, default='N', choices=choice.APPROVAL_CHOICES)
    countLike = models.PositiveSmallIntegerField(default=0)
    countDisLike = models.PositiveSmallIntegerField(default=0)
    create_date = models.DateField(auto_now=True)
    release_date = models.DateField(default=datetime.date.today)
    updated_by = models.CharField(max_length=128, null=True)

    def number_of_likes(self):
        return self.countLike.count()


class Comment(models.Model):
    approved = models.CharField(max_length=1, default='N', choices=choice.APPROVAL_CHOICES)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    body = models.TextField(max_length=256)
    name = models.CharField(max_length=32, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.CharField(max_length=1, default='N', choices=choice.APPROVAL_CHOICES)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

