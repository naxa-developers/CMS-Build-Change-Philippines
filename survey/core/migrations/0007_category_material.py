# Generated by Django 2.0 on 2018-05-13 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_step_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField(max_length=300)),
                ('good_photo', models.ImageField(upload_to='material/good_photo/%Y/%m/%D/')),
                ('bad_photo', models.ImageField(upload_to='material/bad_photo/%Y/%m/%D/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material', to='core.Category')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='material', to='core.Project')),
            ],
        ),
    ]
