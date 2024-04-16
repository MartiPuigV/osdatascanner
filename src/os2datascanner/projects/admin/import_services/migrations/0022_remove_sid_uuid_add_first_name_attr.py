# Generated by Django 3.2.11 on 2024-04-15 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('import_services', '0021_ldapconf_sid_mapper'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ldapconfig',
            name='object_sid_mapper_uuid',
        ),
        migrations.AddField(
            model_name='ldapconfig',
            name='firstname_attribute',
            field=models.CharField(blank=True, help_text="Name of the LDAP attribute which is mapped as first name. For many LDAP server vendors it can be 'givenName'", max_length=64, null=True, verbose_name='First name LDAP attribute'),
        ),
    ]