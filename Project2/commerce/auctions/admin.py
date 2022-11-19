from django.contrib import admin
from . import models

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','hostedAuction']
    search_fields = ['first_name','last_name','hostedAuction']

class listingsAdmin(admin.ModelAdmin):
    list_display = ['title','open','hBid','initialBid']
    search_fields = ['title','open','initialBid','owner','category']

class bidsAdmin(admin.ModelAdmin):
    list_display = ['auction','bid','bidders']
    search_fields = ['auction','bid','bidders']

class commentsAdmin(admin.ModelAdmin):
    list_display = ['comment','auction']
    search_fields = ['auction','users']

class categoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']

admin.site.register(models.User,UserAdmin)
admin.site.register(models.listings,listingsAdmin)
admin.site.register(models.bids,bidsAdmin)
admin.site.register(models.comments,commentsAdmin)
admin.site.register(models.category,categoryAdmin)

