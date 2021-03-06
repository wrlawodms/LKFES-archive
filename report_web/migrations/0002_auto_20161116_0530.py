# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-16 05:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report_web', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='hw_specs',
        ),
        migrations.RemoveField(
            model_name='post',
            name='sw_specs',
        ),
        migrations.AddField(
            model_name='post',
            name='desc',
            field=models.CharField(default='description', max_length=500),
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date published'),
        ),
    ]
