# Generated by Django 2.2.9 on 2020-01-31 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('terra_geocrud', '0039_auto_20200129_1327'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='uiarrayschemaproperty',
            options={'verbose_name': 'UI Array object schema property', 'verbose_name_plural': 'UI Array object schema properties'},
        ),
        migrations.AlterModelOptions(
            name='uischemaproperty',
            options={'verbose_name': 'UI Schema property', 'verbose_name_plural': 'UI Schema properties'},
        ),
    ]
