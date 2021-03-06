# Generated by Django 2.0 on 2018-05-20 05:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0023_auto_20180520_0339'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckListHistroy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_status', models.BooleanField()),
                ('new_status', models.BooleanField()),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RenameField(
            model_name='report',
            old_name='status',
            new_name='report_status',
        ),
        migrations.AddField(
            model_name='checklist',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='report',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='checklisthistroy',
            name='checklist',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='checklist_history', to='core.Checklist'),
        ),
        migrations.AddField(
            model_name='checklisthistroy',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_checklist_history', to=settings.AUTH_USER_MODEL),
        ),
    ]
