from django.contrib import admin
from .import models

# Register your models here.

admin.site.register(models.Event)
admin.site.register(models.DailyTask)
admin.site.register(models.WeekDay)
admin.site.register(models.EventRepetiton)
admin.site.register(models.ListToDo)
admin.site.register(models.WhatToDoToday)
admin.site.register(models.datetracking)