# Generated by Django 4.1.3 on 2022-11-18 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_bids_bid_listings_initialbid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='auction',
            field=models.ManyToManyField(blank=True, null=True, related_name='category', to='auctions.listings'),
        ),
    ]
