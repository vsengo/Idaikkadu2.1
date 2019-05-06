# Generated by Django 2.2.1 on 2019-05-06 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='default', max_length=255, unique=True)),
                ('content', models.CharField(max_length=10000)),
                ('image', models.FileField(default='null', upload_to='news/')),
                ('category', models.CharField(choices=[('international', 'International'), ('srilanka', 'Sri Lanka'), ('jaffna', 'Jaffna')], default='international', max_length=255)),
                ('create_date', models.DateField(auto_now=True)),
            ],
        ),
    ]
