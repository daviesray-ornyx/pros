# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-16 05:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BetProsApp', '0003_sport_sport_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sport',
            name='sport_image',
        ),
    ]
