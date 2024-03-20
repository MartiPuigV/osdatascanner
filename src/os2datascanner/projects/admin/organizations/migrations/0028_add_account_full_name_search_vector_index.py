# Generated by Django 3.2.11 on 2024-03-19 06:30

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0027_organization_onedrive_delete_permission'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={},
        ),
        migrations.AddIndex(
            model_name='account',
            index=django.contrib.postgres.indexes.GinIndex(django.contrib.postgres.search.SearchVector('username', 'first_name', 'last_name', config='english'), name='full_name_search'),
        ),
    ]
