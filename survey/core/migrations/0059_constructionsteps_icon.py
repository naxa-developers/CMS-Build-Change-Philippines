# Generated by Django 2.0 on 2018-11-05 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0058_standardschooldesignpdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='constructionsteps',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='construction_step/icons/'),
        ),
    ]
