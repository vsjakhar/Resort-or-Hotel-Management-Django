# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.models import User
# Create your models here.

from Guest.models import Guest
from booking.models import Booking
from django.utils import timezone
import datetime

status = (('Active','Active'), ('Inactive','Inactive'), ('Delete','Delete'))
etype = (('Chair','Chair'), ('Bed','Bed'))
ofrom = (('Direct','Direct'), ('Call','Call'))
YN = (('YES','YES'), ('NO','NO'))
tstatus = (('Available','Available'), ('Booked','Booked'), ('Damaged','Damaged'))

class Spa_type(models.Model):
	spa_type_id = models.AutoField(primary_key=True)
	spa_type_uid = models.ForeignKey(User)
	spa_type_title = models.CharField(max_length=50)
	spa_type_slug = models.SlugField()
	spa_type_description = models.TextField(blank=True, null=True)
	spa_type_discount = models.IntegerField()
	spa_type_tax = models.FloatField(default=0)
	spa_type_timestamp = models.DateTimeField(default=timezone.now)
	spa_type_utimestamp = models.DateTimeField(default=timezone.now)
	spa_type_ueid = models.IntegerField(blank=True, null=True)
	spa_type_track = models.TextField(blank=True, null=True)
	spa_type_utrack = models.TextField(blank=True, null=True)
	spa_type_status = models.CharField(max_length=50, default='Active', choices=status)

	def save(self, *args, **kwargs):
		if not self.spa_type_slug:
			self.spa_type_slug = slugify(self.spa_type_title)[:50]
		return super(Spa_type, self).save(*args, **kwargs)

	def __unicode__(self):
		return '%s %s' % (
			self.spa_type_title, 
			self.spa_type_description
			)

class Equipment(models.Model):
	equipment_id = models.AutoField(primary_key=True)
	equipment_uid = models.ForeignKey(User)
	equipment_nubmer = models.IntegerField()
	equipment_title = models.CharField(max_length=50)
	equipment_slug = models.SlugField()
	equipment_type = models.CharField(max_length=50, default='Chair', choices=etype)
	equipment_specification = models.TextField(blank=True, null=True)
	equipment_timestamp = models.DateTimeField(default=timezone.now)
	equipment_utimestamp = models.DateTimeField(default=timezone.now)
	equipment_ueid = models.IntegerField(blank=True, null=True)
	equipment_track = models.TextField(blank=True, null=True)
	equipment_utrack = models.TextField(blank=True, null=True)
	equipment_status = models.CharField(max_length=50, default='Active', choices=status)

	def save(self, *args, **kwargs):
		if not self.equipment_slug:
			self.equipment_slug = slugify(self.equipment_title)[:50]
		return super(Equipment, self).save(*args, **kwargs)

	def __unicode__(self):
		return '%s %s %s' % (
			self.equipment_title, 
			self.equipment_nubmer,
			self.equipment_type
			)



class Spa(models.Model):
	spa_id = models.AutoField(primary_key=True)
	spa_uid = models.ForeignKey(User)
	spa_stid = models.ForeignKey(Spa_type)
	spa_title = models.CharField(max_length=111)
	spa_slug = models.SlugField()
	spa_price = models.FloatField(blank=True, null=True)
	spa_discount = models.FloatField(blank=True, null=True)
	spa_tax = models.FloatField(blank=True, null=True)
	spa_special = models.CharField(max_length=111)
	spa_extra = models.TextField(blank=True, null=True)
	spa_description = models.TextField(blank=True, null=True)
	spa_timestamp = models.DateTimeField(default=timezone.now)
	spa_utimestamp = models.DateTimeField(default=timezone.now)
	spa_ueid = models.IntegerField(blank=True, null=True)
	spa_track = models.TextField(blank=True, null=True)
	spa_utrack = models.TextField(blank=True, null=True)
	spa_status = models.CharField(max_length=50, default='Active', choices=status)

	def save(self, *args, **kwargs):
		if not self.spa_slug:
			self.spa_slug = slugify(self.spa_title)[:50]
		return super(Spa, self).save(*args, **kwargs)

	def __unicode__(self):
		return '%s %s %s' % (
			self.spa_title, 
			self.spa_price,
			self.spa_stid
			)


class Service(models.Model):
	service_id = models.AutoField(primary_key=True)
	service_uid = models.ForeignKey(User)
	service_spid = models.ForeignKey(Spa)
	service_eid = models.ForeignKey(Equipment, blank=True, null=True)
	service_gid = models.ForeignKey('Guest.Guest', blank=True, null=True)
	service_bid = models.ForeignKey('booking.Booking', blank=True, null=True)
	service_customer = models.CharField(max_length=111)
	service_price = models.FloatField(blank=True, null=True)
	service_discount = models.FloatField(blank=True, null=True)
	service_tax = models.FloatField(blank=True, null=True)
	service_total = models.FloatField(blank=True, null=True)
	service_extra = models.TextField(blank=True, null=True)
	service_from = models.CharField(max_length=50, default='Direct', choices=ofrom)
	service_timestamp = models.DateTimeField(default=timezone.now)
	service_utimestamp = models.DateTimeField(default=timezone.now)
	service_ueid = models.IntegerField(blank=True, null=True)
	service_track = models.TextField(blank=True, null=True)
	service_utrack = models.TextField(blank=True, null=True)
	service_status = models.CharField(max_length=50, default='Active', choices=status)

	def __unicode__(self):
		return '%s %s %s' % (
			self.service_spid, 
			self.service_eid,
			self.service_total
			)

class Service_history(models.Model):
	serviceh_id = models.AutoField(primary_key=True)
	serviceh_uid = models.ForeignKey(User)
	serviceh_eid = models.ForeignKey(Equipment)
	serviceh_gid = models.ForeignKey('Guest.Guest', blank=True, null=True)
	serviceh_bid = models.ForeignKey('booking.Booking', blank=True, null=True)
	serviceh_sid = models.CharField(max_length=111)
	serviceh_customer = models.CharField(max_length=111, blank=True, null=True)
	serviceh_spas = models.TextField()
	serviceh_prices = models.TextField()
	serviceh_units = models.TextField()
	serviceh_amount = models.TextField()
	serviceh_discount = models.FloatField(default=0)
	serviceh_tax = models.FloatField(blank=True, null=True)
	serviceh_total = models.FloatField(default=0)
	serviceh_description = models.TextField(blank=True, null=True)
	serviceh_from = models.CharField(max_length=50, default='Direct', choices=ofrom)
	serviceh_timestamp = models.DateTimeField(default=timezone.now)
	serviceh_utimestamp = models.DateTimeField(default=timezone.now)
	serviceh_ueid = models.IntegerField(blank=True, null=True)
	serviceh_track = models.TextField(blank=True, null=True)
	serviceh_utrack = models.TextField(blank=True, null=True)
	serviceh_status = models.CharField(max_length=50, default='Active', choices=status)
