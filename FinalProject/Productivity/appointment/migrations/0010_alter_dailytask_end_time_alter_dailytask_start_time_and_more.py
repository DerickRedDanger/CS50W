# Generated by Django 4.2.1 on 2023-06-23 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0009_dailytask_eventrepetiton_listtodo_whattodotoday_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailytask',
            name='end_time',
            field=models.TimeField(default='12:3', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='dailytask',
            name='start_time',
            field=models.TimeField(default='12:2', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.TimeField(default='12:3', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.TimeField(default='12:2', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='whattodotoday',
            name='end_time',
            field=models.TimeField(default='12:3', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='whattodotoday',
            name='start_time',
            field=models.TimeField(default='12:2', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
    ]