# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-14 02:26
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0005_auto_20170913_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='automatedexercise',
            name='difficulty',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)]),
        ),
    ]