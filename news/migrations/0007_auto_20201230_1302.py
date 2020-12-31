# Generated by Django 3.1.2 on 2020-12-30 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_auto_20201225_2339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='create_date',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='updated_by',
        ),
        migrations.AlterField(
            model_name='news',
            name='author',
            field=models.CharField(help_text='Author of the News or Article', max_length=128),
        ),
    ]