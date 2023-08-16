# Generated by Django 4.1.3 on 2023-07-20 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0026_alter_dailytask_end_time_alter_dailytask_start_time_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='datetracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('day', models.DateField()),
            ],
        ),
        migrations.AlterField(
            model_name='dailytask',
            name='end_time',
            field=models.TimeField(default='19:40', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='dailytask',
            name='start_time',
            field=models.TimeField(default='19:39', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='event',
            name='day',
            field=models.DateField(default='2023-7-20', help_text='Format: year-month-day', verbose_name='Day of the event'),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.TimeField(default='19:40', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='event',
            name='repeat_wkd',
            field=models.ManyToManyField(blank=True, default='4', related_name='Todayevent', to='appointment.weekday'),
        ),
        migrations.AlterField(
            model_name='event',
            name='repeatutil',
            field=models.DateField(blank=True, default='2023-7-20', help_text='Format: year-month-day', null=True, verbose_name='Repeat util'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.TimeField(default='19:39', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='eventrepetiton',
            name='day',
            field=models.DateField(default='2023-7-20', help_text='Format: year-month-day', verbose_name='Day of the event'),
        ),
        migrations.AlterField(
            model_name='eventrepetiton',
            name='end_time',
            field=models.TimeField(default='19:40', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='eventrepetiton',
            name='start_time',
            field=models.TimeField(default='19:39', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='whattodotoday',
            name='day',
            field=models.DateField(default='2023-7-20', help_text='Format: year-month-day', verbose_name="the day i (don't) have to do this"),
        ),
        migrations.AlterField(
            model_name='whattodotoday',
            name='end_time',
            field=models.TimeField(default='19:40', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='whattodotoday',
            name='start_time',
            field=models.TimeField(default='19:39', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
    ]
