# Generated by Django 4.2.1 on 2023-06-23 14:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0008_task_importance_alter_event_end_time_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=200, verbose_name="Event's name")),
                ('start_time', models.TimeField(default='11:50', help_text='Format: hour:minute', verbose_name='Starting time')),
                ('end_time', models.TimeField(default='11:51', help_text='Format: hour:minute', verbose_name='Ending time')),
                ('quick_description', models.TextField(blank=True, null=True, verbose_name='quick description')),
                ('description', models.TextField(blank=True, null=True, verbose_name='detailed description')),
                ('notes', models.TextField(blank=True, help_text='Textual Notes', null=True, verbose_name="task's Notes")),
                ('urgency', models.CharField(choices=[('vh', 'very hight'), ('h', 'hight'), ('m', 'medium'), ('l', 'low')], default='m', max_length=2, verbose_name='How urgent is this task ? can it wait/be delayed?')),
                ('importance', models.CharField(choices=[('vh', 'very hight'), ('h', 'hight'), ('m', 'medium'), ('l', 'low')], default='m', max_length=2, verbose_name='How vital is this task ? will It bring great benefits if done? Great demerits if not done?')),
                ('repeat', models.CharField(choices=[('nvr', 'never'), ('wek', 'weekly'), ('mth', 'monthly'), ('yea', 'yearly'), ('wkd', 'specific weekdays')], default='nvr', max_length=3, verbose_name='Repeat ?')),
                ('weekday', models.ManyToManyField(related_name='Todaytask', to='appointment.weekday')),
            ],
        ),
        migrations.CreateModel(
            name='EventRepetiton',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField(default='2023-6-23', help_text='Format: year-month-day', verbose_name='Day of the event')),
            ],
        ),
        migrations.CreateModel(
            name='ListToDo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=200, verbose_name="Event's name")),
                ('quick_description', models.TextField(blank=True, null=True, verbose_name='quick description')),
                ('description', models.TextField(blank=True, null=True, verbose_name='detailed description')),
                ('duration', models.CharField(choices=[('mi', 'Minutes'), ('hs', 'Hours'), ('ds', 'Days'), ('wk', 'Weeks'), ('mn', 'Months'), ('ys', 'Years'), ('Pe', 'Perpetual')], default='hs', max_length=2, verbose_name='How long do you expect this to take ?')),
                ('urgency', models.CharField(choices=[('vh', 'very hight'), ('h', 'hight'), ('m', 'medium'), ('l', 'low')], default='m', max_length=2, verbose_name='How urgent is this task ? can it wait/be delayed?')),
                ('importance', models.CharField(choices=[('vh', 'very hight'), ('h', 'hight'), ('m', 'medium'), ('l', 'low')], default='m', max_length=2, verbose_name='How vital is this task ? will It bring great benefits if done? Great demerits if not done?')),
                ('Progress', models.CharField(choices=[('nt', 'Not Started'), ('st', 'Started'), ('ip', 'In Progress'), ('dn', 'Done'), ('fo', 'forgotten')], default='nt', max_length=2, verbose_name="What's the progress on this task? ")),
                ('last_update', models.DateField(auto_now=True)),
                ('steps', models.ManyToManyField(related_name='bigtask', to='appointment.listtodo')),
            ],
        ),
        migrations.CreateModel(
            name='WhatToDoToday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50, verbose_name='Name')),
                ('day', models.DateField(default='2023-6-23', help_text='Format: year-month-day', verbose_name="Day i (don't) have to do it")),
                ('need', models.CharField(choices=[('Hv', 'Have to do today'), ('Dn', "Don't have to do today"), ('Bw', 'Big Win'), ('Dl', 'Can delegate')], default='Hv', max_length=2)),
                ('start_time', models.TimeField(default='11:50', help_text='Format: hour:minute', verbose_name='Starting time')),
                ('end_time', models.TimeField(default='11:51', help_text='Format: hour:minute', verbose_name='Ending time')),
                ('done', models.BooleanField(default=False)),
                ('todo', models.ManyToManyField(related_name='days_done', to='appointment.listtodo')),
            ],
        ),
        migrations.RemoveField(
            model_name='task',
            name='weekday',
        ),
        migrations.DeleteModel(
            name='whattotoday',
        ),
        migrations.RemoveField(
            model_name='event',
            name='day',
        ),
        migrations.RemoveField(
            model_name='event',
            name='priority',
        ),
        migrations.AddField(
            model_name='event',
            name='importance',
            field=models.CharField(choices=[('vh', 'very hight'), ('h', 'hight'), ('m', 'medium'), ('l', 'low')], default='m', max_length=2, verbose_name='How vital is this event ? will It bring great benefits if done? Great demerits if not done?'),
        ),
        migrations.AddField(
            model_name='event',
            name='urgency',
            field=models.CharField(choices=[('vh', 'very hight'), ('h', 'hight'), ('m', 'medium'), ('l', 'low')], default='m', max_length=2, verbose_name='How urgent is this event ? can it wait/be delayed?'),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.TimeField(default='11:51', help_text='Format: hour:minute', verbose_name='Ending time'),
        ),
        migrations.RemoveField(
            model_name='event',
            name='repeat_wkd',
        ),
        migrations.AlterField(
            model_name='event',
            name='repeatutil',
            field=models.DateField(default='2023-6-23', help_text='Format: year-month-day', verbose_name='Repeat util'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.TimeField(default='11:50', help_text='Format: hour:minute', verbose_name='Starting time'),
        ),
        migrations.DeleteModel(
            name='task',
        ),
        migrations.AddField(
            model_name='eventrepetiton',
            name='original',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Repetitions', to='appointment.event'),
        ),
        migrations.AddField(
            model_name='event',
            name='repeat_wkd',
            field=models.ManyToManyField(blank=True, default='5', null=True, related_name='Todayevent', to='appointment.weekday'),
        ),
    ]
