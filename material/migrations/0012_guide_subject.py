# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-14 05:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0011_auto_20170914_0513'),
    ]

    operations = [
        migrations.AddField(
            model_name='guide',
            name='subject',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='material.Subject'),
            preserve_default=False,
        ),
    ]
