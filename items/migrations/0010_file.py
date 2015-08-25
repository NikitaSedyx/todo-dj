# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0009_group_creator'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(default=b'', max_length=150)),
                ('file', models.FileField(null=True, upload_to=b'./')),
                ('group', models.ForeignKey(to='items.Group')),
            ],
            options={
                'db_table': 'todo_files',
            },
        ),
    ]
