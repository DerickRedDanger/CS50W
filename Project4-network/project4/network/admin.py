from django.contrib import admin
from . import models
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username']
    search_fields = ['id','username']

class postAdmin(admin.ModelAdmin):
    list_display = ['id','owner','timestamp','privacy']
    search_fields = ['id','owner','timestamp','privacy']

class commentsAdmin(admin.ModelAdmin):
    list_display = ['id','owner','post']
    search_fields = ['id','owner','post']


admin.site.register(models.User,UserAdmin)
admin.site.register(models.post,postAdmin)
admin.site.register(models.comment,commentsAdmin)


