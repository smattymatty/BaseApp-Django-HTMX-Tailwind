# Generated by Django 4.2.6 on 2024-05-22 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0005_blogpost_title_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='intro_length',
            field=models.IntegerField(default=0),
        ),
    ]
