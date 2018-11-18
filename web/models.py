import uuid
from django.db import models

class Content(models.Model):
    MENU_CHOICES = (
        ('A', 'Australia'),
        ('C', 'Canada'),
        ('W', 'Swiss'),
        ('U', 'UK'),
        ('E', 'Europe'),
        ('U', 'Middle East'),
        ('S', 'School'),
        ('O', 'Associations'),
        ('T', 'Temples'),
        ('l', 'Libraries'),
        ('B', 'Articles'),
        ('D', 'Obituaries'),
        ('X', 'Other'),
    )

    APPROVAL_CHOICES = (
        ('Y','Yes'),
        ('N','No'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title  = models.CharField(max_length=256)
    author = models.CharField(max_length=128, help_text="Author of the News or Article" )
    email = models.EmailField()
    menu   = models.CharField(max_length=1,choices=MENU_CHOICES)
    approved = models.CharField(max_length=1, choices=APPROVAL_CHOICES,default='N')
    countLike = models.PositiveSmallIntegerField(default=0)
    countDisLike = models.PositiveSmallIntegerField(default=0)
    imageDir = models.FileField(blank=True,upload_to='Image/%Y/')
    link = models.URLField(blank=True, help_text="Optional : any link to share")
    content= models.TextField()
    document = models.FileField(blank=True,help_text="Optional : Any document in .pdf format")
    create_date = models.DateField(auto_now=True)
    release_date = models.DateField()
    updated_by   = models.CharField(max_length=128)



class Comment(models.Model):
    APPROVAL_CHOICES = (
        ('Y','Yes'),
        ('N','No'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment =  models.TextField()
    updated_by   = models.CharField(max_length=128)
    create_date = models.DateField(auto_now=True)
    approved = models.CharField(max_length=1, choices=APPROVAL_CHOICES,default='Y')
    content =   models.ForeignKey(Content,on_delete=models.CASCADE)
