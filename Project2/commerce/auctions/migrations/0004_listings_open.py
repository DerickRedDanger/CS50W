# Generated by Django 4.1.3 on 2022-11-18 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listings_sdescription'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='open',
            field=models.BooleanField(default=True),
        ),
    ]
