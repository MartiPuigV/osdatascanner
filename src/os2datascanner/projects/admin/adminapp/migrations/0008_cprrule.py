# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-07-08 13:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('os2datascanner', '0007_version_metadata'),
    ]

    operations = [
        migrations.CreateModel(
            name='CPRRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='Navn')),
                ('description', models.TextField(verbose_name='Beskrivelse')),
                ('sensitivity', models.IntegerField(choices=[(0, 'Grøn'), (1, 'Gul'), (2, 'Rød')], default=2, verbose_name='Følsomhed')),
                ('do_modulus11', models.BooleanField(default=False, verbose_name='Tjek modulus-11')),
                ('ignore_irrelevant', models.BooleanField(default=False, verbose_name='Ignorer ugyldige fødselsdatoer')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='os2datascanner.Group', verbose_name='Gruppe')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='os2datascanner.Organization', verbose_name='Organisation')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]