# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-12 02:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0013_exercisecomment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercisecomment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
