# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-12 03:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0016_auto_20171012_0252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercisecomment',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
