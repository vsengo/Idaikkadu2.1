import uuid
from django.db import models


class Photo(models.Model):
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
        ('Y', 'Yes'),
        ('N', 'No'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=128, help_text="Author of the News or Article")
    email = models.EmailField()
    menu = models.CharField(max_length=1, choices=MENU_CHOICES)
    approved = models.CharField(max_length=1, choices=APPROVAL_CHOICES)
    countLike = models.PositiveSmallIntegerField()
    countDisLike = models.PositiveSmallIntegerField()
    imageDir = models.FileField(upload_to='Image/%Y')
    link = models.URLField(blank=True, help_text="Optional : any link to share")
    file = models.FileField(upload_to='photos/')
    create_date = models.DateField(auto_now=True)
    release_date = models.DateField()
    updated_by = models.CharField(max_length=128)

    def __init__(self):
        self.countLike = 0
        self.countDisLike = 0
        self.approved = 'N'
