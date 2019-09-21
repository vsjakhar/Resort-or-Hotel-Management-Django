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
ctype = (('Veg','Veg'), ('Non-veg','Non-veg'))
ofrom = (('Direct','Direct'), ('Call','Call'))
YN = (('YES','YES'), ('NO','NO'))
tstatus = (('Available','Available'), ('Booked','Booked'), ('Damaged','Damaged'))

class Category(models.Model):
	category_id = models.AutoField(primary_key=True)
	category_uid = models.ForeignKey(User)
	category_title = models.CharField(max_length=50)
	category_slug = models.SlugField()
	category_description = models.TextField(blank=True, null=True)
	category_discount = models.FloatField(default=0)
	category_tax = models.FloatField(default=0)
	category_vat = models.FloatField(default=0)
	category_timestamp = models.DateTimeField(default=timezone.now)
	category_utimestamp = models.DateTimeField(default=timezone.now)
	category_ueid = models.IntegerField(blank=True, null=True)
	category_track = models.TextField(blank=True, null=True)
	category_utrack = models.TextField(blank=True, null=True)
	category_status = models.CharField(max_length=50, default='Active', choices=status)

	def __unicode__(self):
		return '%s' % (
			self.category_title 
			#self.category_type
			)

	def save(self, *args, **kwargs):
		if not self.category_slug:
			self.category_slug = slugify(self.category_title)[:50]
		return super(Category, self).save(*args, **kwargs)


class Menu(models.Model):
	menu_id = models.AutoField(primary_key=True)
	menu_uid = models.ForeignKey(User)
	menu_ctid = models.ForeignKey(Category)
	menu_title = models.CharField(max_length=111)
	menu_slug = models.SlugField()
	menu_special = models.CharField(max_length=111)
	menu_description = models.TextField(blank=True, null=True)
	menu_timestamp = models.DateTimeField(default=timezone.now)
	menu_utimestamp = models.DateTimeField(default=timezone.now)
	menu_ueid = models.IntegerField(blank=True, null=True)
	menu_track = models.TextField(blank=True, null=True)
	menu_utrack = models.TextField(blank=True, null=True)
	menu_status = models.CharField(max_length=50, default='Active', choices=status)

	def __unicode__(self):
		return '%s %s %s' % (
			self.menu_title, 
			self.menu_ctid, 
			self.menu_special
			)

	def save(self, *args, **kwargs):
		if not self.menu_slug:
			self.menu_slug = slugify(self.menu_title)[:50]
		return super(Menu, self).save(*args, **kwargs)



class Cuisine(models.Model):
	cuisine_id = models.AutoField(primary_key=True)
	cuisine_uid = models.ForeignKey(User)
	cuisine_mid = models.ForeignKey(Menu)
	cuisine_title = models.CharField(max_length=111)
	cuisine_slug = models.SlugField()
	cuisine_special = models.CharField(max_length=111)
	cuisines_extra = models.TextField(blank=True, null=True)
	cuisine_description = models.TextField(blank=True, null=True)
	cuisines_price = models.FloatField(blank=True, null=True)
	cuisines_discount = models.FloatField(blank=True, null=True)
	cuisines_tax = models.FloatField(blank=True, null=True)
	cuisine_timestamp = models.DateTimeField(default=timezone.now)
	cuisine_utimestamp = models.DateTimeField(default=timezone.now)
	cuisine_ueid = models.IntegerField(blank=True, null=True)
	cuisine_track = models.TextField(blank=True, null=True)
	cuisine_utrack = models.TextField(blank=True, null=True)
	cuisine_status = models.CharField(max_length=50, default='Active', choices=status)

	def __unicode__(self):
		return '%s %s %s' % (
			self.cuisine_title, 
			self.cuisines_price, 
			self.cuisine_special
			)

	def save(self, *args, **kwargs):
		if not self.cuisine_slug:
			self.cuisine_slug = slugify(self.cuisine_title)[:50]
		return super(Cuisine, self).save(*args, **kwargs)


class Table(models.Model):
	table_id = models.AutoField(primary_key=True)
	table_uid = models.ForeignKey(User)
	table_no = models.IntegerField(blank=True)
	table_capacity = models.CharField(max_length=111)
	table_description = models.TextField(blank=True, null=True)
	table_smoking = models.CharField(max_length=50, default='NO', choices=YN)
	table_liquor = models.CharField(max_length=50, default='NO', choices=YN)
	table_timestamp = models.DateTimeField(default=timezone.now)
	table_utimestamp = models.DateTimeField(default=timezone.now)
	table_ueid = models.IntegerField(blank=True, null=True)
	table_track = models.TextField(blank=True, null=True)
	table_utrack = models.TextField(blank=True, null=True)
	table_status = models.CharField(max_length=50, default='Available', choices=tstatus)

	def __unicode__(self):
		return '%s %s' % (
			self.table_no, 
			self.table_capacity
			)

class Order(models.Model):
	order_id = models.AutoField(primary_key=True)
	order_uid = models.ForeignKey(User)
	order_cuid = models.ForeignKey(Cuisine)
	order_tid = models.ForeignKey(Table, blank=True, null=True)
	order_gid = models.ForeignKey('Guest.Guest', blank=True, null=True)
	order_bid = models.ForeignKey('booking.Booking', blank=True, null=True)
	order_customer = models.CharField(max_length=111)
	order_unit = models.IntegerField(default=1)
	order_price = models.FloatField(blank=True, null=True)
	order_discount = models.FloatField(blank=True, null=True)
	order_tax = models.FloatField(blank=True, null=True)
	order_vat = models.FloatField(default=0)
	order_total = models.FloatField(blank=True, null=True)
	order_extra = models.TextField(blank=True, null=True)
	order_from = models.CharField(max_length=50, default='Direct', choices=ofrom)
	order_timestamp = models.DateTimeField(default=timezone.now)
	order_utimestamp = models.DateTimeField(default=timezone.now)
	order_ueid = models.IntegerField(blank=True, null=True)
	order_track = models.TextField(blank=True, null=True)
	order_utrack = models.TextField(blank=True, null=True)
	order_status = models.CharField(max_length=50, default='Active', choices=status)

	def __unicode__(self):
		return '%s %s %s' % (
			self.order_cuid, 
			self.order_tid, 
			self.order_gid
			)


class Order_history(models.Model):
	orderh_id = models.AutoField(primary_key=True)
	orderh_uid = models.ForeignKey(User)
	orderh_tid = models.ForeignKey(Table, blank=True, null=True)
	orderh_gid = models.ForeignKey('Guest.Guest', blank=True, null=True)
	orderh_bid = models.ForeignKey('booking.Booking', blank=True, null=True)
	orderh_customer = models.CharField(max_length=111,blank=True)
	orderh_oid = models.CharField(max_length=111)
	orderh_cuisines = models.TextField(blank=True, null=True)
	orderh_prices = models.TextField(blank=True, null=True)
	orderh_units = models.TextField(blank=True, null=True)
	orderh_amount = models.TextField(blank=True, null=True)
	orderh_discount = models.FloatField(default=0)
	orderh_tax = models.FloatField(default=0)
	orderh_vat = models.FloatField(default=0)
	orderh_total = models.FloatField(default=0)
	orderh_description = models.TextField(blank=True, null=True)
	orderh_from = models.CharField(max_length=50, default='Direct', choices=ofrom)
	orderh_timestamp = models.DateTimeField(default=timezone.now)
	orderh_utimestamp = models.DateTimeField(default=timezone.now)
	orderh_ueid = models.IntegerField(blank=True, null=True)
	orderh_track = models.TextField(blank=True, null=True)
	orderh_utrack = models.TextField(blank=True, null=True)
	orderh_status = models.CharField(max_length=50, default='Active', choices=status)

	def __unicode__(self):
		return '%s %s %s %s' % (
			self.orderh_customer,
			self.orderh_cuisines,
			self.orderh_tid, 
			self.orderh_gid
			)

