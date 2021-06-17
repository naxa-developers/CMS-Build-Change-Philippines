# Generated by Django 2.0 on 2018-09-18 04:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_auto_20180918_0336'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sitesteps',
            old_name='steps',
            new_name='step',
        ),
        migrations.AddField(
            model_name='sitesteps',
            name='site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='site_steps', to='core.Site'),
        ),
    ]
