# Generated by Django 3.2.11 on 2022-11-03 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('os2datascanner', '0092_alter_customrule__rule'),
    ]

    operations = [
        migrations.AddField(
            model_name='scanstatus',
            name='matches_found',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='matches found'),
        ),
    ]
