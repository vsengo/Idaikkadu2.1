import uuid
import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models


class Content(models.Model):
    CATEGORY_CHOICES = (
        ('international', 'International'),
        ('srilanka', 'Sri Lanka'),
        ('jaffna', 'Jaffna'),
        ('idaikkadu', 'Idaikkadu'),
        ('australia', 'Australia'),
        ('canada', 'Canada'),
        ('swiss', 'Swiss'),
        ('uk', 'UK'),
        ('europe', 'Europe'),
        ('middle_east', 'Middle East'),
    )

    MENU_CHOICES = (
        ('N', 'News'),
        ('S', 'Story'),
        ('O', 'Associations'),
        ('T', 'Temples'),
        ('L', 'Libraries'),
        ('B', 'Articles'),
        ('D', 'Obituaries'),
        ('W', 'Wedding'),
        ('I', 'Invitation'),
        ('X', 'Other'),
    )

    APPROVAL_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=128, default='webadmin',help_text="Author of the News or Article")
    email = models.EmailField(null=True)
    category = models.CharField(max_length=32, default='idaikkadu',choices=CATEGORY_CHOICES)
    menu = models.CharField(max_length=1, default='N', choices=MENU_CHOICES)
    approved = models.CharField(max_length=1, default='N',choices=APPROVAL_CHOICES)
    countLike = models.PositiveSmallIntegerField(default=0)
    countDisLike = models.PositiveSmallIntegerField(default=0)
    imageDir = models.FileField(upload_to='Image/%Y', null=True)
    link = models.URLField(blank=True, help_text="Optional : any link to share", null=True)
    create_date = models.DateField(auto_now=True)
    release_date = models.DateField(default=datetime.date.today)
    updated_by = models.CharField(max_length=128, null=True)

    #class Meta:
     #   abstract = True



class User(AbstractUser):
    first_name = models.CharField('First Name of User', blank=True, max_length=20)
    last_name = models.CharField('Last Name of User', blank=True, max_length=20)


class Meta:
    permissions = (("view_add_delete", "To provide update edit facility"),
                   ("view_add", "To provide add facility"),
                   ("view_only", "To provide update view facility"))
