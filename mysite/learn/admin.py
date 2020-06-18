from django.contrib import admin

# Register your models here.
from .models import Newslinks

class NewslinksAdmin(admin.ModelAdmin):
    list_display = ('id','title','date','url','keywords')

admin.site.register(Newslinks,NewslinksAdmin)
