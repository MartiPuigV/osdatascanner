# Generated by Django 3.2.11 on 2023-05-30 14:02

from django.db import migrations, models
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ('os2datascanner_report', '0075_remove_documentreport_temp_organization_uuid'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='documentreport',
            index=models.Index(django.db.models.functions.text.Upper('owner'), name='alias_creation_query_idx'),
        ),
    ]
