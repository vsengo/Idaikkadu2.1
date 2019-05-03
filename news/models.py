from django.db import models


class News(models.Model):
    title = models.CharField(max_length=255, unique=True, default='default')
    content = models.CharField(max_length=10000)
    # image = models.FileField(upload_to='news/')
    create_date = models.DateField(auto_now=True)
