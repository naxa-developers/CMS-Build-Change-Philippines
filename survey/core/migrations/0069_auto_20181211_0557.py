# Generated by Django 2.0 on 2018-12-11 05:57

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0068_auto_20181209_0546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='primaryphoto',
            name='image',
            field=models.ImageField(blank=True, null=True, storage=core.models.OverwriteStorage(), upload_to='materials/updated_primary_photo'),
        ),
    ]
