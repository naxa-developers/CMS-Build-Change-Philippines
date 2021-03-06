# Generated by Django 2.0 on 2018-05-24 05:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_merge_20180523_1117'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='site/documents')),
                ('document_name', models.CharField(blank=True, max_length=250, null=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='site_document', to='core.Site')),
            ],
        ),
        migrations.AlterField(
            model_name='material',
            name='bad_photo',
            field=models.ImageField(blank=True, null=True, upload_to='materials/bad_photo'),
        ),
        migrations.AlterField(
            model_name='material',
            name='good_photo',
            field=models.ImageField(blank=True, null=True, upload_to='materials/good_photo'),
        ),
    ]
