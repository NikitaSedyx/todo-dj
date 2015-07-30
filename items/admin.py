from django.contrib import admin

from .models import Item, Group

admin.site.register(Item)
admin.site.register(Group)