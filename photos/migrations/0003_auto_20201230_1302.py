# Generated by Django 3.1.2 on 2020-12-30 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0002_auto_20201217_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]