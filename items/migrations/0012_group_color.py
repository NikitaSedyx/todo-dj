# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0011_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='color',
            field=models.CharField(default=b'white', max_length=6, choices=[(b'red', b'red'), (b'green', b'green'), (b'blue', b'blue'), (b'orange', b'orange'), (b'white', b'white'), (b'yellow', b'yellow')]),
        ),
    ]
