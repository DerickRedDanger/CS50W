# Generated by Django 4.1.3 on 2023-01-10 20:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='follow',
            field=models.ManyToManyField(blank=True, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.TextField()),
                ('image', models.URLField(blank=True, max_length=300)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('like', models.ManyToManyField(blank=True, related_name='liked', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(default='{{ request.user}}', on_delete=django.db.models.deletion.CASCADE, related_name='myposts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]