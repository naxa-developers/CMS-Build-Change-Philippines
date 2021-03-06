# Generated by Django 2.0 on 2019-07-18 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0094_auto_20190717_0529'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventlog',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='eventlog',
            name='title',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='eventlog',
            name='action',
            field=models.CharField(choices=[('phoned_to', 'phoned to'), ('submitted_a_response', 'submitted a response for general form'), ('updated_a_response', 'updated a response for general form'), ('submit_feedback', 'Admit submitted a feedback')], max_length=300),
        ),
    ]
