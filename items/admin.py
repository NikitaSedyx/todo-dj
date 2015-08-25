from django.contrib import admin

from .models import Item, Group, File

admin.site.register(Item)
admin.site.register(Group)
admin.site.register(File)
