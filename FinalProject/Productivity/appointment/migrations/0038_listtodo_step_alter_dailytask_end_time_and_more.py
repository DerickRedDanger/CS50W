# Generated by Django 4.1.3 on 2023-09-19 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0037_alter_dailytask_end_time_alter_dailytask_start_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listtodo',
            name='step',
            field=models.BooleanField(default=False, verbose_name='This task is one of the steps to another one?'),
        ),
        migrations.AlterField(
            model_name='dailytask',
            name='end_time',
            field=models.TimeField(default='20:16', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='dailytask',
            name='start_time',
            field=models.TimeField(default='20:15', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='eventrepetiton',
            name='end_time',
            field=models.TimeField(default='20:16', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='eventrepetiton',
            name='start_time',
            field=models.TimeField(default='20:15', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='whattodotoday',
            name='end_time',
            field=models.TimeField(default='20:16', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='whattodotoday',
            name='start_time',
            field=models.TimeField(default='20:15', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
    ]
