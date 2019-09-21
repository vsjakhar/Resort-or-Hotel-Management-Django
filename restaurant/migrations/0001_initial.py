# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-03 08:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('booking', '0001_initial'),
        ('Guest', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_title', models.CharField(max_length=50)),
                ('category_slug', models.SlugField()),
                ('category_description', models.TextField(blank=True, null=True)),
                ('category_discount', models.FloatField(default=0)),
                ('category_tax', models.FloatField(default=0)),
                ('category_vat', models.FloatField(default=0)),
                ('category_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('category_utimestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('category_ueid', models.IntegerField(blank=True, null=True)),
                ('category_track', models.TextField(blank=True, null=True)),
                ('category_utrack', models.TextField(blank=True, null=True)),
                ('category_status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Delete', 'Delete')], default='Active', max_length=50)),
                ('category_uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('cuisine_id', models.AutoField(primary_key=True, serialize=False)),
                ('cuisine_title', models.CharField(max_length=111)),
                ('cuisine_slug', models.SlugField()),
                ('cuisine_special', models.CharField(max_length=111)),
                ('cuisines_extra', models.TextField(blank=True, null=True)),
                ('cuisine_description', models.TextField(blank=True, null=True)),
                ('cuisines_price', models.FloatField(blank=True, null=True)),
                ('cuisines_discount', models.FloatField(blank=True, null=True)),
                ('cuisines_tax', models.FloatField(blank=True, null=True)),
                ('cuisine_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('cuisine_utimestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('cuisine_ueid', models.IntegerField(blank=True, null=True)),
                ('cuisine_track', models.TextField(blank=True, null=True)),
                ('cuisine_utrack', models.TextField(blank=True, null=True)),
                ('cuisine_status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Delete', 'Delete')], default='Active', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('menu_id', models.AutoField(primary_key=True, serialize=False)),
                ('menu_title', models.CharField(max_length=111)),
                ('menu_slug', models.SlugField()),
                ('menu_special', models.CharField(max_length=111)),
                ('menu_description', models.TextField(blank=True, null=True)),
                ('menu_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('menu_utimestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('menu_ueid', models.IntegerField(blank=True, null=True)),
                ('menu_track', models.TextField(blank=True, null=True)),
                ('menu_utrack', models.TextField(blank=True, null=True)),
                ('menu_status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Delete', 'Delete')], default='Active', max_length=50)),
                ('menu_ctid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.Category')),
                ('menu_uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_customer', models.CharField(max_length=111)),
                ('order_unit', models.IntegerField(default=1)),
                ('order_price', models.FloatField(blank=True, null=True)),
                ('order_discount', models.FloatField(blank=True, null=True)),
                ('order_tax', models.FloatField(blank=True, null=True)),
                ('order_vat', models.FloatField(default=0)),
                ('order_total', models.FloatField(blank=True, null=True)),
                ('order_extra', models.TextField(blank=True, null=True)),
                ('order_from', models.CharField(choices=[('Direct', 'Direct'), ('Call', 'Call')], default='Direct', max_length=50)),
                ('order_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('order_utimestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('order_ueid', models.IntegerField(blank=True, null=True)),
                ('order_track', models.TextField(blank=True, null=True)),
                ('order_utrack', models.TextField(blank=True, null=True)),
                ('order_status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Delete', 'Delete')], default='Active', max_length=50)),
                ('order_bid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='booking.Booking')),
                ('order_cuid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.Cuisine')),
                ('order_gid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Guest.Guest')),
            ],
        ),
        migrations.CreateModel(
            name='Order_history',
            fields=[
                ('orderh_id', models.AutoField(primary_key=True, serialize=False)),
                ('orderh_customer', models.CharField(blank=True, max_length=111)),
                ('orderh_oid', models.CharField(max_length=111)),
                ('orderh_cuisines', models.TextField(blank=True, null=True)),
                ('orderh_prices', models.TextField(blank=True, null=True)),
                ('orderh_units', models.TextField(blank=True, null=True)),
                ('orderh_amount', models.TextField(blank=True, null=True)),
                ('orderh_discount', models.FloatField(default=0)),
                ('orderh_tax', models.FloatField(default=0)),
                ('orderh_vat', models.FloatField(default=0)),
                ('orderh_total', models.FloatField(default=0)),
                ('orderh_description', models.TextField(blank=True, null=True)),
                ('orderh_from', models.CharField(choices=[('Direct', 'Direct'), ('Call', 'Call')], default='Direct', max_length=50)),
                ('orderh_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('orderh_utimestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('orderh_ueid', models.IntegerField(blank=True, null=True)),
                ('orderh_track', models.TextField(blank=True, null=True)),
                ('orderh_utrack', models.TextField(blank=True, null=True)),
                ('orderh_status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive'), ('Delete', 'Delete')], default='Active', max_length=50)),
                ('orderh_bid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='booking.Booking')),
                ('orderh_gid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Guest.Guest')),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('table_id', models.AutoField(primary_key=True, serialize=False)),
                ('table_no', models.IntegerField(blank=True)),
                ('table_capacity', models.CharField(max_length=111)),
                ('table_description', models.TextField(blank=True, null=True)),
                ('table_smoking', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO')], default='NO', max_length=50)),
                ('table_liquor', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO')], default='NO', max_length=50)),
                ('table_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('table_utimestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('table_ueid', models.IntegerField(blank=True, null=True)),
                ('table_track', models.TextField(blank=True, null=True)),
                ('table_utrack', models.TextField(blank=True, null=True)),
                ('table_status', models.CharField(choices=[('Available', 'Available'), ('Booked', 'Booked'), ('Damaged', 'Damaged')], default='Available', max_length=50)),
                ('table_uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order_history',
            name='orderh_tid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurant.Table'),
        ),
        migrations.AddField(
            model_name='order_history',
            name='orderh_uid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='order_tid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurant.Table'),
        ),
        migrations.AddField(
            model_name='order',
            name='order_uid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cuisine',
            name='cuisine_mid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.Menu'),
        ),
        migrations.AddField(
            model_name='cuisine',
            name='cuisine_uid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
