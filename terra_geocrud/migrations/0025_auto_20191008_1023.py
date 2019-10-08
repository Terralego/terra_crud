# Generated by Django 2.2.6 on 2019-10-08 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terra_geocrud', '0024_propertydisplayrendering'),
    ]

    operations = [
        migrations.AddField(
            model_name='crudview',
            name='feature_title_property',
            field=models.CharField(blank=True, default='', help_text='Schema property used to define feature title.', max_length=250),
        ),
        migrations.AlterField(
            model_name='propertydisplayrendering',
            name='widget',
            field=models.CharField(choices=[('terra_geocrud.properties.widgets.DataUrlToImgWidget', 'DataUrlToImgWidget'), ('terra_geocrud.properties.widgets.FileAhrefWidget', 'FileAhrefWidget')], max_length=255),
        ),
    ]