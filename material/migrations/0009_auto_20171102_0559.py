# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-02 08:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0008_auto_20171101_2220'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='guideitem',
            unique_together=set([]),
        ),
    ]
