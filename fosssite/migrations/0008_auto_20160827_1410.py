# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-27 14:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fosssite', '0007_auto_20160827_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributions',
            name='ticket_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]