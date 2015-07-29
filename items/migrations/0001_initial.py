# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import tastypie.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(default=b'', max_length=150)),
                ('is_completed', models.BooleanField(default=False)),
                ('deadline', models.DateTimeField(default=tastypie.utils.timezone.now)),
                ('user', models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['is_completed', 'deadline'],
                'db_table': 'todo_items',
            },
            bases=(models.Model,),
        ),
    ]
