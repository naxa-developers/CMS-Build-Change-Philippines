# Generated by Django 2.0 on 2019-05-28 06:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0089_auto_20190524_0929'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='reports/', verbose_name='Image')),
            ],
        ),
        migrations.RemoveField(
            model_name='substepreport',
            name='photo',
        ),
        migrations.AddField(
            model_name='images',
            name='substepreport',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='core.SubstepReport'),
        ),
    ]
