from django.db import models

CATEGORY_CHOICES = (
    ('international','International'),
    ('srilanka', 'Sri Lanka'),
    ('idaikkadu','Idaikkadu'),
)

class News(models.Model):
    title = models.CharField(max_length=255, unique=True, default='default')
    content = models.CharField(max_length=10000)
    image = models.FileField(upload_to='news/', default='null')
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, default='international')
    create_date = models.DateField(auto_now=True)
