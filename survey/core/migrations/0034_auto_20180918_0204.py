# Generated by Django 2.0 on 2018-09-18 02:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0033_material_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConstructionSteps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('order', models.IntegerField(default=0)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='construction_steps', to='core.Project')),
            ],
        ),
        migrations.CreateModel(
            name='ConstructionSubSteps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True, max_length=300, null=True)),
                ('good_photo', models.ImageField(blank=True, null=True, upload_to='materials/update_good_photo')),
                ('bad_photo', models.ImageField(blank=True, null=True, upload_to='materials/update_bad_photo')),
                ('primary_photo', models.ImageField(blank=True, null=True, upload_to='materials/primary_photo')),
                ('order', models.IntegerField(default=0)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_steps', to='core.ConstructionSteps')),
            ],
        ),
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ('-date',)},
        ),
    ]
