# Generated by Django 2.0 on 2018-05-21 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20180521_0651'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='description_de',
            field=models.TextField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='material',
            name='description_en',
            field=models.TextField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='material',
            name='title_de',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='material',
            name='title_en',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
