# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-06 02:42
from __future__ import unicode_literals

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('description', models.TextField()),
                ('title', models.TextField()),
                ('source', models.FileField(upload_to=core.models.Multimedia.get_upload_path)),
                ('authors', models.ManyToManyField(related_name='audio_content', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('description', models.TextField()),
                ('title', models.TextField()),
                ('source', models.FileField(upload_to=core.models.Multimedia.get_upload_path)),
                ('authors', models.ManyToManyField(related_name='image_content', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('biography', models.TextField()),
                ('avatar', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Image')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('description', models.TextField()),
                ('title', models.TextField()),
                ('lead', models.TextField()),
                ('content', models.TextField()),
                ('authors', models.ManyToManyField(related_name='story_content', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('description', models.TextField()),
                ('title', models.TextField()),
                ('source', models.FileField(upload_to=core.models.Multimedia.get_upload_path)),
                ('authors', models.ManyToManyField(related_name='video_content', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]