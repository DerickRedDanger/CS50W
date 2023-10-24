# Generated by Django 4.1.3 on 2023-10-23 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0045_event_short_description_alter_dailytask_end_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailytask',
            name='end_time',
            field=models.TimeField(default='20:4', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='dailytask',
            name='importance',
            field=models.CharField(choices=[('5', 'Essential'), ('4', 'important'), ('3', 'circumstantial'), ('2', 'desirable'), ('1', 'Curiosity/interest'), ('0', 'trivial')], default='3', max_length=2, verbose_name='How vital is this task ? Will It bring great benefits if done? Great demerits if not done?'),
        ),
        migrations.AlterField(
            model_name='dailytask',
            name='start_time',
            field=models.TimeField(default='20:3', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='dailytask',
            name='urgency',
            field=models.CharField(choices=[('5', 'Very Close'), ('4', 'close'), ('3', 'Medium'), ('2', 'far'), ('1', 'Very far')], default='3', max_length=2, verbose_name='How urgent is this task ? Can it wait/be delayed?'),
        ),
        migrations.AlterField(
            model_name='event',
            name='importance',
            field=models.CharField(choices=[('5', 'Essential'), ('4', 'important'), ('3', 'circumstantial'), ('2', 'desirable'), ('1', 'Curiosity/interest'), ('0', 'trivial')], default='3', max_length=2, verbose_name='How vital is this event? will It bring great benefits if done? Great demerits if not done?'),
        ),
        migrations.AlterField(
            model_name='event',
            name='short_description',
            field=models.TextField(blank=True, null=True, verbose_name='A quick description of the Event'),
        ),
        migrations.AlterField(
            model_name='eventrepetiton',
            name='day',
            field=models.DateField(default='2023-10-23', help_text='Format: year-month-day', verbose_name='Day of the event'),
        ),
        migrations.AlterField(
            model_name='eventrepetiton',
            name='end_time',
            field=models.TimeField(default='20:4', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='eventrepetiton',
            name='start_time',
            field=models.TimeField(default='20:3', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='listtodo',
            name='importance',
            field=models.CharField(choices=[('5', 'Essential'), ('4', 'important'), ('3', 'circumstantial'), ('2', 'desirable'), ('1', 'Curiosity/interest'), ('0', 'trivial')], default='3', max_length=2, verbose_name='How vital is this task? Will It bring great benefits if done? Great demerits if not done?'),
        ),
        migrations.AlterField(
            model_name='listtodo',
            name='urgency',
            field=models.CharField(choices=[('5', 'Very Close'), ('4', 'close'), ('3', 'Medium'), ('2', 'far'), ('1', 'Very far')], default='3', max_length=2, verbose_name='How urgent is this task? can it wait/be delayed?'),
        ),
        migrations.AlterField(
            model_name='whattodotoday',
            name='day',
            field=models.DateField(default='2023-10-23', help_text='Format: year-month-day', verbose_name="the day i (don't) have to do this"),
        ),
        migrations.AlterField(
            model_name='whattodotoday',
            name='end_time',
            field=models.TimeField(default='20:4', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='whattodotoday',
            name='need',
            field=models.CharField(choices=[('4', 'Have to do today'), ('3', "Don't have to do today"), ('5', 'Big Win'), ('2', 'Can delegate'), ('1', 'If enough time')], default='4', max_length=2),
        ),
        migrations.AlterField(
            model_name='whattodotoday',
            name='start_time',
            field=models.TimeField(default='20:3', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
    ]
