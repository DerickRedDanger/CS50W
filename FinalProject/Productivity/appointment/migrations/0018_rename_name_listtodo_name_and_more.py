# Generated by Django 4.2.1 on 2023-06-27 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0017_remove_weekday_todaytask_dailytask_weekday_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listtodo',
            old_name='Name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='listtodo',
            old_name='Progress',
            new_name='progress',
        ),
        migrations.AddField(
            model_name='listtodo',
            name='notes',
            field=models.TextField(blank=True, help_text='Textual Notes', null=True, verbose_name="task's Notes"),
        ),
        migrations.AlterField(
            model_name='dailytask',
            name='end_time',
            field=models.TimeField(default='17:52', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='dailytask',
            name='start_time',
            field=models.TimeField(default='17:51', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.TimeField(default='17:52', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.TimeField(default='17:51', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='whattodotoday',
            name='end_time',
            field=models.TimeField(default='17:52', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='whattodotoday',
            name='start_time',
            field=models.TimeField(default='17:51', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
    ]
