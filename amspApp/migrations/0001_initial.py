# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Helpbar',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('url', models.TextField(max_length=550)),
                ('angularUrl', models.TextField(max_length=550)),
                ('title', models.TextField(max_length=550)),
                ('help_fa', models.TextField(max_length=2000)),
                ('help_en', models.TextField(max_length=2000)),
                ('link_fa', models.TextField(max_length=450)),
                ('link_en', models.TextField(max_length=450)),
            ],
        ),
        migrations.CreateModel(
            name='Languages',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('en', models.TextField(max_length=2000, blank=True, null=True)),
                ('fa', models.TextField(max_length=2000, blank=True, null=True)),
                ('ar', models.TextField(max_length=2000, blank=True, null=True)),
                ('kr', models.TextField(max_length=2000, blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sidebar',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.TextField(max_length=50)),
                ('state', models.TextField(max_length=50)),
                ('type', models.TextField(max_length=50)),
                ('icon', models.TextField(max_length=50)),
                ('parent', models.IntegerField(blank=True, null=True)),
                ('order', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
