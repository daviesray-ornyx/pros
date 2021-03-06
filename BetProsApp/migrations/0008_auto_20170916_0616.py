# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-16 06:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BetProsApp', '0007_auto_20170916_0610'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=250, verbose_name='Name')),
                ('description', models.TextField(max_length=500, verbose_name='Description')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='BetProsApp.Region', verbose_name='Region')),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.AddField(
            model_name='club',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='BetProsApp.Country', verbose_name='Country'),
        ),
    ]
