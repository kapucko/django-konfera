# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-05 15:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('konfera', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='konfera.Event'),
            preserve_default=False,
        ),
    ]
