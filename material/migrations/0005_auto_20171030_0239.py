# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-30 05:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0004_auto_20171030_0023'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='moment',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='guide',
            name='moment',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
