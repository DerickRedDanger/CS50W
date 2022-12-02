# Generated by Django 4.1.3 on 2022-11-22 23:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_category_listings_comments_bids'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='auction',
            field=models.ManyToManyField(blank=True, related_name='category', to='auctions.listings'),
        ),
        migrations.AddField(
            model_name='listings',
            name='followed',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listings',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]