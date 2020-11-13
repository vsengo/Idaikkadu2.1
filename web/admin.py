from django.contrib import admin
from news.models import News
from photos.models import Photo, PhotoAlbum

# Register your models here.
admin.site.register(News)
admin.site.register(Photo)
admin.site.register(PhotoAlbum)