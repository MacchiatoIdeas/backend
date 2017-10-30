# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-30 04:56
from __future__ import unicode_literals

from django.db import migrations, models
import material.models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0004_automatedexercise_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='automatedexercise',
            name='text',
            field=models.TextField(validators=[material.models.validate_entries]),
        ),
    ]
