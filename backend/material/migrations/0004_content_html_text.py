# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-10 04:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0003_auto_20170809_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='html_text',
            field=models.TextField(default='<h1>Placeholder</h1>'),
            preserve_default=False,
        ),
    ]