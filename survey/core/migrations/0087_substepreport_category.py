# Generated by Django 2.0 on 2019-05-22 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0086_auto_20190210_1014'),
    ]

    operations = [
        migrations.AddField(
            model_name='substepreport',
            name='category',
            field=models.CharField(choices=[(0, 'Progress update'), (1, 'Issues/Concerns'), (2, 'Questions/Inquiries')], default=0, max_length=100),
        ),
    ]
