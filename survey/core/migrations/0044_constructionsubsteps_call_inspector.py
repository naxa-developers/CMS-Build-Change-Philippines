# Generated by Django 2.0 on 2018-09-23 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_auto_20180920_0701'),
    ]

    operations = [
        migrations.AddField(
            model_name='constructionsubsteps',
            name='call_inspector',
            field=models.BooleanField(default=False),
        ),
    ]
