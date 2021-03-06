# Generated by Django 2.0 on 2018-05-21 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20180520_0517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='bad_photo',
            field=models.ImageField(blank=True, null=True, upload_to='material/bad_photo/%Y/%m/%D/'),
        ),
        migrations.AlterField(
            model_name='material',
            name='good_photo',
            field=models.ImageField(blank=True, null=True, upload_to='material/good_photo/%Y/%m/%D/'),
        ),
        migrations.AlterField(
            model_name='project',
            name='type',
            field=models.IntegerField(choices=[(0, 'School'), (1, 'House'), (2, 'Others')], default=0),
        ),
        migrations.AlterField(
            model_name='site',
            name='type',
            field=models.IntegerField(choices=[(0, 'Type I'), (1, 'Type II'), (2, 'Type III')], default=0),
        ),
    ]
