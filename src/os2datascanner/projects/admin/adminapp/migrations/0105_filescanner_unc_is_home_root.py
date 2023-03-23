# Generated by Django 3.2.11 on 2023-03-23 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('os2datascanner', '0104_scanner_covered_accounts'),
    ]

    operations = [
        migrations.AddField(
            model_name='filescanner',
            name='unc_is_home_root',
            field=models.BooleanField(default=False, help_text='all folders under the given UNC are user home folders; their owners have responsibility for everything they contain regardless of other filesystem metadata', verbose_name='UNC is home root'),
        ),
    ]
