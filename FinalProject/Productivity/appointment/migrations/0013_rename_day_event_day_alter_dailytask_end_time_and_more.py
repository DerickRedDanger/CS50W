# Generated by Django 4.2.1 on 2023-06-23 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0012_event_day_alter_dailytask_end_time_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='Day',
            new_name='day',
        ),
        migrations.AlterField(
            model_name='dailytask',
            name='end_time',
            field=models.TimeField(default='14:55', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='dailytask',
            name='start_time',
            field=models.TimeField(default='14:54', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.TimeField(default='14:55', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='event',
            name='repeatutil',
            field=models.DateField(default='2023-6-23', help_text='Format: year-month-day', verbose_name='Repeat util'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.TimeField(default='14:54', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='whattodotoday',
            name='day',
            field=models.DateField(default='2023-6-23', help_text='Format: year-month-day', verbose_name="the day i (don't) have to do this"),
        ),
        migrations.AlterField(
            model_name='whattodotoday',
            name='end_time',
            field=models.TimeField(default='14:55', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='whattodotoday',
            name='start_time',
            field=models.TimeField(default='14:54', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
    ]