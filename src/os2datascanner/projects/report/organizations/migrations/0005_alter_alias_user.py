# Generated by Django 3.2.11 on 2022-05-11 13:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '0004_alias'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alias',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aliases', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]