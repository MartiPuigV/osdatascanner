# Generated by Django 3.2.11 on 2022-02-02 09:14

from django.db import migrations, models
import django.db.models.expressions


mapping = {
    "scan_tag": "raw_scan_tag",
    "matches": "raw_matches",
    "problem": "raw_problem",
    "metadata": "raw_metadata"
}


def split_data(apps, schema_editor):
    DocumentReport = apps.get_model("os2datascanner_report", "DocumentReport")

    for dr in DocumentReport.objects.iterator():
        for old_key, new_field in mapping.items():
            value = dr.data.get(old_key)
            if value:
                setattr(dr, new_field, value)
        dr.data = None
        dr.save()


def unsplit_data(apps, schema_editor):
    DocumentReport = apps.get_model("os2datascanner_report", "DocumentReport")

    for dr in DocumentReport.objects.iterator():
        dr.data = {}
        for old_key, new_field in mapping.items(): 
            value = getattr(dr, new_field)
            if value:
                dr.data[old_key] = value
        dr.save()


class Migration(migrations.Migration):

    dependencies = [
        ('os2datascanner_report', '0039_documentreport_update_sort_key'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='documentreport',
            name='documentreport_matched',
        ),
        migrations.AddField(
            model_name='documentreport',
            name='raw_matches',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='documentreport',
            name='raw_metadata',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='documentreport',
            name='raw_problem',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='documentreport',
            name='raw_scan_tag',
            field=models.JSONField(null=True),
        ),
        migrations.RunPython(split_data, unsplit_data),
        migrations.RemoveField(
            model_name='documentreport',
            name='data',
        ),
        migrations.AddIndex(
            model_name='documentreport',
            index=models.Index(django.db.models.expressions.F('raw_matches__matched'), name='documentreport_matched'),
        ),
        migrations.AddIndex(
            model_name='documentreport',
            index=models.Index(fields=['scanner_job_pk', 'path'], name='pc_update_query'),
        ),
    ]
