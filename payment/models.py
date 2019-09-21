# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


from django.utils import timezone
import datetime
from Guest.models import Guest
from booking.models import Booking

# Create your models here.

status = (('Active','Active'), ('Inactive','Inactive'), ('Delete','Delete'))
mode = (('Cash','Cash'), ('Cheque','Cheque'), ('Credit Card','Credit Card'), ('Bank Transfer','Bank Transfer'), ('POS','POS'), ('Revenue Loss','Revenue Loss'), ('Others','Others'))
invoice = (('YES','YES'), ('NO','NO'))
fmode = (('Room','Room'), ('Damage','Damage'), ('Restaurant','Restaurant'), ('Spa','Spa'), ('Bar','Bar'), ('Others','Others'))
class Payment(models.Model):
	payment_id = models.AutoField(primary_key=True)
	payment_gid = models.ForeignKey('Guest.Guest', blank=True, null=True)
	payment_bid = models.ForeignKey('booking.Booking', blank=True, null=True)
	payment_customer = models.CharField(max_length=55, blank=True, null=True)
	payment_amount = models.FloatField(blank=True)
	payment_tax = models.FloatField(blank=True, default=0)
	payment_total = models.FloatField(blank=True)
	payment_discount = models.FloatField(blank=True, default=0)
	payment_disc_res = models.TextField(blank=True)
	payment_from = models.CharField(max_length=55, default='Room', choices=fmode)
	payment_mode = models.CharField(max_length=55, default='Cash', choices=mode)
	payment_type = models.CharField(max_length=55, blank=True)
	#payment_amount = models.IntegerField(blank=True)
	payment_receipt = models.CharField(max_length=55, blank=True)
	payment_description = models.TextField(blank=True)
	payment_invoice = models.CharField(max_length=55, default='YES', choices=invoice)
	payment_type = models.CharField(max_length=55, blank=True)
	payment_timestamp = models.DateTimeField(default=timezone.now)
	payment_utimestamp = models.DateTimeField(default=timezone.now)
	payment_ueid = models.IntegerField(blank=True, default=0)
	payment_track = models.TextField(blank=True, null=True)
	payment_utrack = models.TextField(blank=True, null=True)
	payment_status = models.CharField(max_length=10, default='Active', choices=status)

	def __unicode__(self):
		return '%s %s %s' % (
			self.payment_gid, 
			self.payment_amount, 
			self.payment_from
			)


class Folio(models.Model):
	folio_id = models.AutoField(primary_key=True)
	folio_gid = models.ForeignKey('Guest.Guest')
	folio_bid = models.ForeignKey('booking.Booking')
	folio_title = models.CharField(max_length=111, blank=True)
	folio_unit = models.IntegerField(blank=True, default=0)
	folio_price = models.FloatField(blank=True, default=0)
	folio_amount = models.FloatField(blank=True)
	folio_tax = models.FloatField(blank=True, default=0)
	folio_total = models.FloatField(blank=True)
	folio_discount = models.FloatField(blank=True, default=0)
	folio_disc_res = models.TextField(blank=True)
	folio_from = models.CharField(max_length=55, default='Room', choices=fmode)
	folio_type = models.CharField(max_length=55, blank=True)
	folio_receipt = models.CharField(max_length=55, blank=True)
	folio_description = models.TextField(blank=True)
	folio_invoice = models.CharField(max_length=55, default='YES', choices=invoice)
	folio_type = models.CharField(max_length=55, blank=True)
	folio_timestamp = models.DateTimeField(default=timezone.now)
	folio_utimestamp = models.DateTimeField(default=timezone.now)
	folio_ueid = models.IntegerField(blank=True)
	folio_track = models.TextField(blank=True, null=True)
	folio_utrack = models.TextField(blank=True, null=True)
	folio_status = models.CharField(max_length=10, default='Active', choices=status)

	def __unicode__(self):
		return '%s %s %s' % (
			self.folio_gid, 
			self.folio_title, 
			self.folio_amount
			)
