# Generated by Django 2.2.5 on 2019-09-28 10:49

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terra_geocrud', '0021_auto_20190928_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crudview',
            name='default_list_properties',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=250), blank=True, default=list, size=None),
        ),
    ]
