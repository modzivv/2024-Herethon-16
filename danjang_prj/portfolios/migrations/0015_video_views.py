# Generated by Django 5.0.6 on 2024-07-03 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0014_like_video_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
