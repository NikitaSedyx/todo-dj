# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_auto_20150730_0757'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='user',
            new_name='users',
        ),
        migrations.AlterField(
            model_name='group',
            name='users',
            field=models.ManyToManyField(related_name='user_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
