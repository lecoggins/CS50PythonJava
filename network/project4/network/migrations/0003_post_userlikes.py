# Generated by Django 4.1.7 on 2023-05-16 12:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_user_image_user_posts_post_follower'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='userLikes',
            field=models.ManyToManyField(related_name='user_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
