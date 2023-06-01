# Generated by Django 4.1.3 on 2022-11-30 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0020_alter_listings_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='Sdescription',
            field=models.CharField(max_length=500, verbose_name='Short description'),
        ),
        migrations.AlterField(
            model_name='listings',
            name='cImage',
            field=models.URLField(blank=True, null=True, verbose_name='Caution image'),
        ),
        migrations.AlterField(
            model_name='listings',
            name='caution',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Caution message'),
        ),
    ]