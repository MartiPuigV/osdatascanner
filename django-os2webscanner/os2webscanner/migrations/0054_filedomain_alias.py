# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-02-15 13:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('os2webscanner', '0053_auto_20190206_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='filedomain',
            name='alias',
            field=models.CharField(max_length=64, null=True, verbose_name='Drevbogstav'),
        ),
    ]
