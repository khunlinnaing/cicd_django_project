from django.contrib import admin
from main.models import *
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display= ['title', 'content']
