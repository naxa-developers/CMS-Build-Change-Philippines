# Generated by Django 2.0 on 2019-06-11 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0091_merge_20190611_0857'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitereport',
            name='photo',
        ),
    ]
