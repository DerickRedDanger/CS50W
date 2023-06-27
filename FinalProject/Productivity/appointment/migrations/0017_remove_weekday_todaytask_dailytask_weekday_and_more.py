# Generated by Django 4.2.1 on 2023-06-27 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0016_remove_dailytask_repeat_remove_dailytask_weekday_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weekday',
            name='todaytask',
        ),
        migrations.AddField(
            model_name='dailytask',
            name='weekday',
            field=models.ManyToManyField(blank=True, related_name='Todaytask', to='appointment.weekday'),
        ),
        migrations.AlterField(
            model_name='dailytask',
            name='end_time',
            field=models.TimeField(default='12:18', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='dailytask',
            name='start_time',
            field=models.TimeField(default='12:17', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.TimeField(default='12:18', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.TimeField(default='12:17', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='whattodotoday',
            name='end_time',
            field=models.TimeField(default='12:18', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='whattodotoday',
            name='start_time',
            field=models.TimeField(default='12:17', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
    ]