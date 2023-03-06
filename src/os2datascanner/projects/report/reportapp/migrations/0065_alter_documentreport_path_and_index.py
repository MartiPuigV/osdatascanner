# Generated by Django 3.2.11 on 2023-02-10 09:15

import django.contrib.postgres.indexes
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('os2datascanner_report', '0064_alter_documentreport_number_of_matches'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentreport',
            name='path',
            field=models.TextField(verbose_name='path'),
        ),
        migrations.AddIndex(
            model_name='documentreport',
            index=django.contrib.postgres.indexes.HashIndex(fields=['path'], name='pc_update_query'),
        ),
    ]
