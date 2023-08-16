# Generated by Django 4.1.3 on 2023-07-22 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0028_alter_dailytask_end_time_alter_dailytask_importance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailytask',
            name='end_time',
            field=models.TimeField(default='21:45', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='dailytask',
            name='start_time',
            field=models.TimeField(default='21:44', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='dailytask',
            name='urgency',
            field=models.CharField(choices=[('vh', 'Very Close'), ('h', 'close'), ('m', 'Medium'), ('l', 'far'), ('vl', 'Very far')], default='m', max_length=2, verbose_name='How urgent is this task ? Can it wait/be delayed?'),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.TimeField(default='21:45', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.TimeField(default='21:44', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='eventrepetiton',
            name='end_time',
            field=models.TimeField(default='21:45', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='eventrepetiton',
            name='start_time',
            field=models.TimeField(default='21:44', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
        migrations.AlterField(
            model_name='listtodo',
            name='urgency',
            field=models.CharField(choices=[('vh', 'Very Close'), ('h', 'close'), ('m', 'Medium'), ('l', 'far'), ('vl', 'Very far')], default='m', max_length=2, verbose_name='How urgent is this task ? can it wait/be delayed?'),
        ),
        migrations.AlterField(
            model_name='whattodotoday',
            name='end_time',
            field=models.TimeField(default='21:45', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='whattodotoday',
            name='start_time',
            field=models.TimeField(default='21:44', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
    ]
