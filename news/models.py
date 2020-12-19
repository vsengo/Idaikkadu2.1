import datetime
from django.db import models
from django.contrib.auth.models import User

from web.choices import choice


class News(models.Model):
    title = models.CharField(max_length=256, blank=True, help_text="Short Title")
    content = models.TextField(max_length=10000)
    image = models.ImageField(upload_to='news/%Y', blank=True, null=True)
    author = models.CharField(max_length=128, default='webadmin', help_text="Author of the News or Article")
    email = models.EmailField(null=True)
    region = models.CharField(max_length=32, default='idaikkadu', choices=choice.REGION_CHOICES)
    menu = models.CharField(max_length=16, default='N', choices=choice.MENU_CHOICES)
    section = models.CharField(max_length=1, default='D', choices=choice.SECTION_CHOICES)
    link = models.URLField(blank=True, help_text="Optional: any link to share", null=True)
    approved = models.CharField(max_length=1, default='N', choices=choice.APPROVAL_CHOICES)
    countLike = models.ManyToManyField(User, related_name='blogpost_like')
    countDisLike = models.PositiveSmallIntegerField(default=0)
    create_date = models.DateField(auto_now=True)
    release_date = models.DateField(default=datetime.date.today)
    updated_by = models.CharField(max_length=128, null=True)

    def number_of_likes(self):
        return self.countLike.count()


class Comment(models.Model):
    comment = models.TextField()
    approved = models.CharField(max_length=1, default='N', choices=choice.APPROVAL_CHOICES)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    updated_by = models.CharField(max_length=128)
    create_date = models.DateField(auto_now=True)
    body = models.TextField(max_length=256)
    name = models.CharField(max_length=32, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.CharField(max_length=1, default='N', choices=choice.APPROVAL_CHOICES)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

