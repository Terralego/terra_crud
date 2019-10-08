# Generated by Django 2.2.6 on 2019-10-07 11:52

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('terra_geocrud', '0023_auto_20190928_1235'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyDisplayRendering',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property', models.CharField(max_length=255)),
                ('widget', models.CharField(choices=[('terra_geocrud.properties.widgets.DataUrlToImgWidget', 'DataUrlToImgWidget')], max_length=255)),
                ('args', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict)),
                ('crud_view', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feature_property_rendering', to='terra_geocrud.CrudView')),
            ],
            options={
                'verbose_name': 'Custom feature property rendering',
                'verbose_name_plural': 'Custom feature properties rendering',
                'ordering': ('crud_view', 'property'),
                'unique_together': {('crud_view', 'property')},
            },
        ),
    ]