# Generated by Django 3.0.4 on 2020-03-20 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('terra_geocrud', '0038_delete_propertydisplayrendering'),
    ]

    operations = [
        migrations.RenameField(
            model_name='crudview',
            old_name='name_plural',
            new_name='object_name_plural',
        ),
    ]
