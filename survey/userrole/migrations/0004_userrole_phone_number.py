# Generated by Django 2.0 on 2018-09-24 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userrole', '0003_merge_20180511_0601'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrole',
            name='phone_number',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
