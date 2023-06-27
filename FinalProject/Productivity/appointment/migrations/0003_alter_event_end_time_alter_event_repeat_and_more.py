# Generated by Django 4.2.1 on 2023-06-16 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0002_weekday_remove_event_repeattimes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.TimeField(default='18:25', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='event',
            name='repeat',
            field=models.CharField(choices=[('nvr', 'never'), ('day', 'daily'), ('wek', 'weekly'), ('mth', 'monthly'), ('yea', 'yearly'), ('wkd', 'specific weekdays'), ('edv', 'every days')], default='nvr', max_length=3, verbose_name='when to repeat ?'),
        ),
        migrations.AlterField(
            model_name='event',
            name='repeatd',
            field=models.CharField(choices=[('frv', 'Forever'), ('spc', 'Specific number of times'), ('utl', 'Util')], default='frv', max_length=3, verbose_name='How many times ?'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.TimeField(default='18:24', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='task',
            name='end_time',
            field=models.TimeField(default='18:25', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='task',
            name='start_time',
            field=models.TimeField(default='18:24', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
    ]