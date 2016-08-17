# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-04 19:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fosssite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserEdit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('handle', models.CharField(max_length=128)),
                ('about_me', models.TextField()),
                ('twitterurl', models.URLField()),
                ('facebookurl', models.URLField()),
                ('lnkdnurl', models.URLField()),
                ('githuburl', models.URLField()),
                ('example', models.URLField()),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='useredit',
            name='useredit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]