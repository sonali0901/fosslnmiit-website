# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-17 10:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fosssite', '0007_auto_20160817_0451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='about_me',
            field=models.TextField(blank=True, default=b'', max_length=300),
        ),
    ]