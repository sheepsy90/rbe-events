# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-03 21:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20161203_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventparticipant',
            name='state',
            field=models.CharField(choices=[('interested', 'Interested'), ('going', 'Going'), ('not_going', 'Not going')], max_length=32),
        ),
    ]