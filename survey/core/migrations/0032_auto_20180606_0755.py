# Generated by Django 2.0 on 2018-06-06 07:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0031_auto_20180601_0916'),
    ]

    operations = [
        migrations.AddField(
            model_name='step',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='report',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='report/'),
        ),
    ]
