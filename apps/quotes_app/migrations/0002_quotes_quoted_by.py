# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-21 21:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotes',
            name='quoted_by',
            field=models.CharField(default='some person', max_length=255),
            preserve_default=False,
        ),
    ]
