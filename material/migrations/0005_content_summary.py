# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-10 06:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0004_content_html_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='summary',
            field=models.CharField(default='', max_length=150),
            preserve_default=False,
        ),
    ]