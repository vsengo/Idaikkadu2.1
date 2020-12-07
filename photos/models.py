import datetime
from django.db import models
from web.choices import choice

class Album (models.Model):
    title = models.CharField(max_length=128, blank=True, help_text="Short Title")
    description = models.TextField(max_length=1000,blank=True)
    thumb = models.ImageField(blank=True, null=True)
    author = models.CharField(max_length=128, default='webadmin', help_text="Author of the News or Article")
    email = models.EmailField(null=True)
    region = models.CharField(max_length=32, default='idaikkadu', choices=choice.REGION_CHOICES)
    menu = models.CharField(max_length=16, default='X', choices=choice.MENU_CHOICES)
    section = models.CharField(max_length=1, default='D', choices=choice.SECTION_CHOICES)
    approved = models.CharField(max_length=1, default='N', choices=choice.APPROVAL_CHOICES)
    countLike = models.PositiveSmallIntegerField(default=0)
    countDisLike = models.PositiveSmallIntegerField(default=0)
    create_date = models.DateField(auto_now=True)
    release_date = models.DateField(default=datetime.date.today)
    updated_by = models.CharField(max_length=128, null=True)

class Photo(models.Model):
    file = models.ImageField(upload_to='photos/%Y', blank=True,null=True)
    figNo = models.IntegerField(default=0)
    thumb = models.ImageField(upload_to='photos/%Y', blank=True,null=True)
    album = models.ForeignKey(Album, related_name='album', on_delete=models.CASCADE)

class Comment(models.Model):
    comment = models.TextField( )
    approved = models.CharField(max_length=1, default='N', choices=choice.APPROVAL_CHOICES)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    updated_by = models.CharField(max_length=128)
    create_date = models.DateField(auto_now=True)