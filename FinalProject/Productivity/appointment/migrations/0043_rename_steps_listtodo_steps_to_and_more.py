# Generated by Django 4.1.3 on 2023-09-22 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0042_alter_dailytask_end_time_alter_dailytask_start_time_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listtodo',
            old_name='steps',
            new_name='steps_to',
        ),
        migrations.AlterField(
            model_name='dailytask',
            name='end_time',
            field=models.TimeField(default='17:57', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='dailytask',
            name='start_time',
            field=models.TimeField(default='17:56', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='eventrepetiton',
            name='day',
            field=models.DateField(default='2023-9-22', help_text='Format: year-month-day', verbose_name='Day of the event'),
        ),
        migrations.AlterField(
            model_name='eventrepetiton',
            name='end_time',
            field=models.TimeField(default='17:57', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='eventrepetiton',
            name='start_time',
            field=models.TimeField(default='17:56', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='whattodotoday',
            name='day',
            field=models.DateField(default='2023-9-22', help_text='Format: year-month-day', verbose_name="the day i (don't) have to do this"),
        ),
        migrations.AlterField(
            model_name='whattodotoday',
            name='end_time',
            field=models.TimeField(default='17:57', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='whattodotoday',
            name='start_time',
            field=models.TimeField(default='17:56', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
    ]
