# Generated by Django 5.2.3 on 2025-07-05 10:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_comment_created_on'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='already_liked',
            field=models.ManyToManyField(related_name='already_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
