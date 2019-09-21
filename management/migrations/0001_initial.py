# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-03 07:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Section',
            fields=[
                ('section_id', models.AutoField(primary_key=True, serialize=False)),
                ('section_title', models.CharField(max_length=50)),
                ('section_slug', models.SlugField()),
                ('section_description', models.TextField(blank=True, null=True)),
                ('section_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('section_utimestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('section_ueid', models.IntegerField(blank=True, null=True)),
                ('section_track', models.TextField(blank=True, null=True)),
                ('section_utrack', models.TextField(blank=True, null=True)),
                ('section_status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Delete', 'Delete')], default='Active', max_length=50)),
                ('section_uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('staff_id', models.AutoField(primary_key=True, serialize=False)),
                ('staff_title', models.CharField(choices=[('Mr', 'Mr'), ('Mrs', 'Mrs')], default='Mr', max_length=10)),
                ('staff_fname', models.CharField(max_length=50)),
                ('staff_lname', models.CharField(blank=True, max_length=50)),
                ('staff_email', models.EmailField(max_length=50)),
                ('staff_mobile', models.CharField(max_length=15, null=True)),
                ('staff_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('staff_gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=20)),
                ('staff_nationality', models.CharField(blank=True, max_length=100, null=True)),
                ('staff_address', models.TextField(blank=True, null=True)),
                ('staff_country', models.CharField(blank=True, max_length=100, null=True)),
                ('staff_state', models.CharField(blank=True, max_length=100, null=True)),
                ('staff_city', models.CharField(blank=True, max_length=100, null=True)),
                ('staff_zipcode', models.IntegerField(blank=True, null=True)),
                ('staff_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('staff_utimestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('staff_track', models.TextField(blank=True, null=True)),
                ('staff_utrack', models.TextField(blank=True, null=True)),
                ('staff_status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Delete', 'Delete')], default='Active', max_length=10)),
                ('staff_uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]