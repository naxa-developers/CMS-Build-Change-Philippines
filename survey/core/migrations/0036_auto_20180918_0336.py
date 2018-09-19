# Generated by Django 2.0 on 2018-09-18 03:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_auto_20180918_0330'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='constructionsteps',
            name='site',
        ),
        migrations.AddField(
            model_name='sitesteps',
            name='steps',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='site_steps', to='core.ConstructionSteps'),
        ),
    ]