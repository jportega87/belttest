# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-18 17:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RenameField(
            model_name='logins',
            old_name='email',
            new_name='username',
        ),
        migrations.AddField(
            model_name='items',
            name='login',
            field=models.ManyToManyField(to='testapp.Logins'),
        ),
    ]