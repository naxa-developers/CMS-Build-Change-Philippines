# Generated by Django 2.0 on 2019-01-11 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0079_merge_20190109_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='constructionsubsteps',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='constructionsubsteps',
            name='description_de',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='constructionsubsteps',
            name='description_en',
            field=models.TextField(blank=True, null=True),
        ),
    ]
