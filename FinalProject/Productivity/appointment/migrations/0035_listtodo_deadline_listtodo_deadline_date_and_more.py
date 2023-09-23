# Generated by Django 4.1.3 on 2023-09-19 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0034_dailytask_friday_dailytask_monday_dailytask_saturday_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listtodo',
            name='deadline',
            field=models.BooleanField(default=False, verbose_name='This task has a deadline?'),
        ),
        migrations.AddField(
            model_name='listtodo',
            name='deadline_date',
            field=models.DateField(default='2023-9-19', help_text='Format: year-month-day', verbose_name='When is the deadline?'),
        ),
        migrations.AlterField(
            model_name='dailytask',
            name='end_time',
            field=models.TimeField(default='19:44', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='dailytask',
            name='start_time',
            field=models.TimeField(default='19:43', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='dailytask',
            name='title',
            field=models.CharField(max_length=200, unique=True, verbose_name="Event's name"),
        ),
        migrations.AlterField(
            model_name='event',
            name='friday',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='monday',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='saturday',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='sunday',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='thursday',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='tuesday',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='wednesday',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='eventrepetiton',
            name='day',
            field=models.DateField(default='2023-9-19', help_text='Format: year-month-day', verbose_name='Day of the event'),
        ),
        migrations.AlterField(
            model_name='eventrepetiton',
            name='end_time',
            field=models.TimeField(default='19:44', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='eventrepetiton',
            name='start_time',
            field=models.TimeField(default='19:43', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='listtodo',
            name='title',
            field=models.CharField(max_length=200, unique=True, verbose_name="Event's name"),
        ),
        migrations.AlterField(
            model_name='whattodotoday',
            name='day',
            field=models.DateField(default='2023-9-19', help_text='Format: year-month-day', verbose_name="the day i (don't) have to do this"),
        ),
        migrations.AlterField(
            model_name='whattodotoday',
            name='end_time',
            field=models.TimeField(default='19:44', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='whattodotoday',
            name='start_time',
            field=models.TimeField(default='19:43', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
    ]