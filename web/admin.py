from django.contrib import admin
from news.models import News, Comment
from photos.models import Photo, Album

# Register your models here.
admin.site.register(News)
admin.site.register(Photo)
admin.site.register(Album)
admin.site.register(Comment)
