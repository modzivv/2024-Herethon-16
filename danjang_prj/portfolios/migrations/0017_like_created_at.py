# Generated by Django 4.2.5 on 2024-07-04 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolios', '0016_watchhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
