# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0005_auto_20150730_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='users',
            field=models.ManyToManyField(related_name='users', to=settings.AUTH_USER_MODEL),
        ),
    ]
