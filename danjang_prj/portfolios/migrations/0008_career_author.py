# Generated by Django 4.2.5 on 2024-07-01 20:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portfolios', '0007_career'),
    ]

    operations = [
        migrations.AddField(
            model_name='career',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='careers', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
