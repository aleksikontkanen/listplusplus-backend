# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-20 10:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20171020_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='list_items',
            field=models.ManyToManyField(to='api.ListItem'),
        ),
    ]
