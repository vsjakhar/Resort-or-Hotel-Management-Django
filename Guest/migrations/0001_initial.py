# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-03 06:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('country', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='gother',
            fields=[
                ('gother_id', models.AutoField(primary_key=True, serialize=False)),
                ('gother_preferences', models.TextField(blank=True, null=True)),
                ('gother_details', models.TextField(blank=True, null=True)),
                ('gother_spouse_title', models.CharField(blank=True, max_length=555, null=True)),
                ('gother_spouse_fname', models.CharField(blank=True, max_length=555, null=True)),
                ('gother_spouse_lname', models.CharField(blank=True, max_length=555, null=True)),
                ('gother_birthday', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('gother_anniversory', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('gother_timestamp', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('gother_utimestamp', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('gother_track', models.CharField(blank=True, max_length=555, null=True)),
                ('gother_utrack', models.CharField(blank=True, max_length=555, null=True)),
                ('gother_status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Delete', 'Delete')], default='Active', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('guest_id', models.AutoField(primary_key=True, serialize=False)),
                ('guest_title', models.CharField(choices=[('Mr.', 'Mr.'), ('Dr.', 'Dr.'), ('Miss', 'Miss'), ('Mrs.', 'Mrs.'), ('Ms.', 'Ms.'), ('Rabbi', 'Rabbi'), ('Bishop', 'Bishop'), ('Father', 'Father'), ('Reverend', 'Reverend'), ('Pastor', 'Pastor'), ('Capt.', 'Capt.'), ('Gen.', 'Gen.'), ('Sir', 'Sir')], default='Mr', max_length=10)),
                ('guest_fname', models.CharField(max_length=50)),
                ('guest_lname', models.CharField(blank=True, max_length=50)),
                ('guest_email', models.EmailField(max_length=50, unique=True)),
                ('guest_mobile', models.CharField(max_length=12)),
                ('guest_gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=20)),
                ('guest_dob', models.DateField(blank=True, null=True)),
                ('guest_nationality', models.CharField(blank=True, max_length=100, null=True)),
                ('guest_address', models.TextField(blank=True, null=True)),
                ('guest_city', models.CharField(blank=True, max_length=100, null=True)),
                ('guest_zipcode', models.IntegerField(blank=True, null=True)),
                ('guest_type', models.CharField(choices=[('Normal', 'Normal'), ('VIP', 'VIP'), ('Blacklist', 'Blacklist')], default='Normal', max_length=100)),
                ('guest_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('guest_utimestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('guest_track', models.TextField(blank=True)),
                ('guest_utrack', models.TextField(blank=True)),
                ('guest_status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Delete', 'Delete')], default='Active', max_length=10)),
                ('guest_previous_stay', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('guest_future_stay', models.DateTimeField(blank=True, null=True)),
                ('guest_comment', models.TextField(blank=True)),
                ('guest_referal_url', models.TextField(blank=True)),
                ('guest_country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='country.Country')),
                ('guest_state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='country.State')),
                ('guest_uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='gwork',
            fields=[
                ('gwork_id', models.AutoField(primary_key=True, serialize=False)),
                ('gwork_organization', models.CharField(blank=True, max_length=555, null=True)),
                ('gwork_designation', models.CharField(blank=True, max_length=555, null=True)),
                ('gwork_address', models.TextField(blank=True, null=True)),
                ('gwork_city', models.CharField(blank=True, max_length=555, null=True)),
                ('gwork_zipcode', models.IntegerField(blank=True, null=True)),
                ('gwork_email', models.EmailField(blank=True, max_length=50, null=True)),
                ('gwork_phone', models.CharField(blank=True, max_length=555, null=True)),
                ('gwork_mobile', models.CharField(blank=True, max_length=555, null=True)),
                ('gwork_fax', models.CharField(blank=True, max_length=555, null=True)),
                ('gwork_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('gwork_utimestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('gwork_track', models.CharField(blank=True, max_length=555, null=True)),
                ('gwork_utrack', models.CharField(blank=True, max_length=555, null=True)),
                ('gwork_status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Delete', 'Delete')], default='Active', max_length=10)),
                ('gwork_country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='country.Country')),
                ('gwork_gid', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Guest.Guest')),
                ('gwork_state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='country.State')),
            ],
        ),
        migrations.AddField(
            model_name='gother',
            name='gother_gid',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='Guest.Guest'),
        ),
    ]
