# Generated by Django 5.0.6 on 2024-07-02 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0012_video_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='career',
            old_name='author',
            new_name='user',
        ),
    ]
