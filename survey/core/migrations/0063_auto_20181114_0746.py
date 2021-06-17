# Generated by Django 2.0 on 2018-11-14 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0062_eventlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='substepchecklist',
            name='description_de',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='substepchecklist',
            name='description_en',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='substepchecklist',
            name='text_de',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='substepchecklist',
            name='text_en',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='eventlog',
            name='action',
            field=models.CharField(choices=[('phoned_to', 'phoned to'), ('submitted_a_response', 'submitted a response for general form'), ('updated_a_response', 'updated a response for general form')], max_length=300),
        ),
    ]
