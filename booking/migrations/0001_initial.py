# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-03 07:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Guest', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Room', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('booking_id', models.AutoField(primary_key=True, serialize=False)),
                ('booking_amount', models.IntegerField(blank=True)),
                ('booking_discount', models.FloatField(blank=True, default=0)),
                ('booking_service_tax', models.FloatField(default=0)),
                ('booking_luxury_tax', models.FloatField(default=0)),
                ('booking_tax', models.FloatField(blank=True, default=0)),
                ('booking_total', models.FloatField(blank=True, default=0)),
                ('booking_advance', models.FloatField(blank=True, default=0)),
                ('booking_room_count', models.IntegerField(blank=True, default=1)),
                ('booking_duration', models.IntegerField(blank=True, default=1)),
                ('booking_adult', models.IntegerField(blank=True, default=1)),
                ('booking_child', models.IntegerField(blank=True, default=0)),
                ('booking_extra_bed', models.IntegerField(blank=True, default=0)),
                ('booking_messages', models.TextField(blank=True, null=True)),
                ('booking_note', models.TextField(blank=True, null=True)),
                ('booking_arrival', models.DateTimeField(blank=True)),
                ('booking_departure', models.DateTimeField(blank=True)),
                ('booking_checkin_type', models.CharField(choices=[('Perfect', 'Perfect'), ('Early', 'Early'), ('Late', 'Late')], default='Perfect', max_length=55)),
                ('booking_checkin', models.DateTimeField(blank=True, null=True)),
                ('booking_checkout', models.DateTimeField(blank=True, null=True)),
                ('booking_expected_checkin', models.DateTimeField(blank=True, null=True)),
                ('booking_expected_checkout', models.DateTimeField(blank=True, null=True)),
                ('booking_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('booking_utimestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('booking_ueid', models.IntegerField(blank=True, null=True)),
                ('booking_track', models.TextField(blank=True, null=True)),
                ('booking_utrack', models.TextField(blank=True, null=True)),
                ('booking_status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Delete', 'Delete')], default='Active', max_length=10)),
                ('booking_tentative_arrival', models.DateTimeField(blank=True, null=True)),
                ('booking_tentative_departure', models.DateTimeField(blank=True, null=True)),
                ('booking_referal_url', models.TextField(blank=True)),
                ('booking_gid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Guest.Guest')),
                ('booking_rid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Room.Room')),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('source_id', models.AutoField(primary_key=True, serialize=False)),
                ('source_title', models.CharField(max_length=55)),
                ('source_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('source_utimestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('source_ueid', models.IntegerField(blank=True, null=True)),
                ('source_track', models.TextField(blank=True, null=True)),
                ('source_utrack', models.TextField(blank=True, null=True)),
                ('source_status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Delete', 'Delete')], default='Active', max_length=10)),
                ('source_uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Travel',
            fields=[
                ('travel_id', models.AutoField(primary_key=True, serialize=False)),
                ('travel_amode', models.CharField(blank=True, max_length=55, null=True)),
                ('travel_atitle', models.TextField(blank=True, null=True)),
                ('travel_atime', models.DateTimeField(blank=True, null=True)),
                ('travel_atask', models.CharField(blank=True, max_length=55, null=True)),
                ('travel_dmode', models.CharField(blank=True, max_length=55, null=True)),
                ('travel_dtitle', models.TextField(blank=True, null=True)),
                ('travel_dtime', models.DateTimeField(blank=True, null=True)),
                ('travel_dtask', models.CharField(blank=True, max_length=55, null=True)),
                ('travel_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('travel_utimestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('travel_ueid', models.IntegerField(blank=True, null=True)),
                ('travel_track', models.TextField(blank=True, null=True)),
                ('travel_utrack', models.TextField(blank=True, null=True)),
                ('travel_status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Delete', 'Delete')], default='Active', max_length=10)),
                ('travel_bid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.Booking')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='booking_sid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='booking.Source'),
        ),
    ]
