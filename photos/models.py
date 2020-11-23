import datetime
from django.db import models

class PhotoAlbum (models.Model):
    CATEGORY_CHOICES = (
        ('idaikkadu', 'Idaikkadu'),
        ('srilanka', 'Sri Lanka'),
        ('jaffna', 'Jaffna'),
        ('australia', 'Australia/New Zealand'),
        ('canada', 'America/Canada'),
        ('uk', 'United Kingdom'),
        ('swiss', 'Switzerland'),
        ('europe', 'Europe'),
        ('asia', 'Singapore/Asia'),
        ('middle_east', 'Middle East'),
        ('international', 'International'),
    )

    MENU_CHOICES = (
        ('O', 'Associations'),
        ('T', 'Temples'),
        ('L', 'Libraries'),
        ('W', 'Wedding'),
        ('B', 'Birthday'),
        ('F', 'Funeral'),
        ('X', 'Other Events'),
    )

    APPROVAL_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
    title = models.CharField(max_length=256, blank=True, help_text="Short Title")
    author = models.CharField(max_length=128, default='webadmin', help_text="Author of the News or Article")
    email = models.EmailField(null=True)
    category = models.CharField(max_length=32, default='idaikkadu', choices=CATEGORY_CHOICES)
    menu = models.CharField(max_length=1, default='X', choices=MENU_CHOICES)
    approved = models.CharField(max_length=1, default='N', choices=APPROVAL_CHOICES)
    countLike = models.PositiveSmallIntegerField(default=0)
    countDisLike = models.PositiveSmallIntegerField(default=0)
    imageDir = models.FileField(upload_to='Image/%Y', null=True)
    create_date = models.DateField(auto_now=True)
    release_date = models.DateField(default=datetime.date.today)
    updated_by = models.CharField(max_length=128, null=True)

    def default(self):
        return self.album.filter(default=True).first()

class Photo(models.Model):
    file = models.ImageField(upload_to='photos/', blank=True,null=True)
    album = models.ForeignKey(PhotoAlbum, related_name='album',on_delete=models.CASCADE)
    figNo = models.IntegerField(default=0)