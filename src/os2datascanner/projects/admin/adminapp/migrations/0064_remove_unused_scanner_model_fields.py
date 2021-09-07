# Generated by Django 3.2.4 on 2021-08-30 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('os2datascanner', '0063_alter_jsonfields'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scanner',
            name='address_replace_text',
        ),
        migrations.RemoveField(
            model_name='scanner',
            name='cpr_replace_text',
        ),
        migrations.RemoveField(
            model_name='scanner',
            name='do_address_replace',
        ),
        migrations.RemoveField(
            model_name='scanner',
            name='do_cpr_replace',
        ),
        migrations.RemoveField(
            model_name='scanner',
            name='do_name_replace',
        ),
        migrations.RemoveField(
            model_name='scanner',
            name='do_run_synchronously',
        ),
        migrations.RemoveField(
            model_name='scanner',
            name='is_visible',
        ),
        migrations.RemoveField(
            model_name='scanner',
            name='name_replace_text',
        ),
        migrations.RemoveField(
            model_name='scanner',
            name='output_spreadsheet_file',
        ),
        migrations.RemoveField(
            model_name='scanner',
            name='process_urls',
        ),
    ]