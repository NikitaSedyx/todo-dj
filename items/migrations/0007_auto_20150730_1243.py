# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0006_auto_20150730_0852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='items',
        ),
        migrations.RemoveField(
            model_name='item',
            name='users',
        ),
        migrations.AddField(
            model_name='item',
            name='group',
            field=models.ForeignKey(default=2, to='items.Group'),
            preserve_default=False,
        ),
    ]
