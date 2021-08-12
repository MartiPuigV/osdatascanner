# Generated by Django 3.2.4 on 2021-08-11 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('import_services', '0005_added_related_name_to_realm_and_importjob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ldapconfig',
            name='users_dn',
            field=models.TextField(help_text="Distinguished name for the (top) OU in which to search for users. Groups present under this OU will not necessarily be imported, as OS2datascanner reconstructs groups based on users' group memberships.", verbose_name='DN for users (OU)'),
        ),
    ]
