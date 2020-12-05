import uuid
import datetime
from django.db import models

class News(models.Model):
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
        ('News', 'News'),
        ('Obituary', 'Obituary'),
        ('Story', 'Story'),
        ('Association', 'Association'),
        ('Article', 'Articles'),
        ('Thankyou', 'Thankyou'),
        ('Temple', 'Temple'),
        ('Library', 'Library'),
        ('Wedding', 'Wedding'),
        ('Invitation', 'Invitation'),
        ('Other', 'Other'),
    )

    APPROVAL_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )

    title = models.CharField(max_length=256, blank=True, help_text="Short Title")
    content = models.TextField(max_length=10000)
    #image = models.ImageField(upload_to='news/%Y',blank=True)
    image = models.ImageField()
    author = models.CharField(max_length=128, default='webadmin', help_text="Author of the News or Article")
    email = models.EmailField(null=True)
    category = models.CharField(max_length=32, default='idaikkadu', choices=CATEGORY_CHOICES)
    menu = models.CharField(max_length=16, default='N', choices=MENU_CHOICES)
    link = models.URLField(blank=True, help_text="Optional: any link to share", null=True)
    approved = models.CharField(max_length=1, default='N', choices=APPROVAL_CHOICES)
    countLike = models.PositiveSmallIntegerField(default=0)
    countDisLike = models.PositiveSmallIntegerField(default=0)
    create_date = models.DateField(auto_now=True)
    release_date = models.DateField(default=datetime.date.today)
    updated_by = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.get_menu_display()


class Comment(models.Model):
     comment = models.TextField()
     news = models.ForeignKey(News, on_delete=models.CASCADE)
     updated_by = models.CharField(max_length=128)
     create_date = models.DateField(auto_now=True)
