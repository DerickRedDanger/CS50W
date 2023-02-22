# Generated by Django 4.1.3 on 2023-02-02 19:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_post_privacy_alter_post_owner_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Pdescription',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='owner',
            field=models.ForeignKey(default='{{ request.User.id }}', on_delete=django.db.models.deletion.CASCADE, related_name='mycomments', to=settings.AUTH_USER_MODEL),
        ),
    ]
