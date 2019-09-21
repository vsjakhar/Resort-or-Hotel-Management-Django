# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from Guest.models import Guest
from Room.models import Room_type, Room
from crum import get_current_request
from django.core.exceptions import ValidationError

from django.db.models import signals
from django.core.mail import EmailMultiAlternatives
#from Room.models import Room_type, Rooms
#from Employee.models import Employee, Task_Table
rate = (('Aura_cabine_suite_20999','Aura_cabine_suite_20999'), ('Aura_lanai_premium_14999','Aura_lanai_premium_14999'), ('Aura_lanai_10999','Aura_lanai_10999'), ('Aura_king_premium_7999','Aura_king_premium_7999'),('Aura_twin_premium','Aura_twin_premium'))
status = (('Active','Active'), ('Inactive','Inactive'), ('Delete','Delete'))
checkin_type = (('Perfect','Perfect'), ('Early','Early'), ('Late','Late'))

class Source(models.Model):
	source_id = models.AutoField(primary_key=True)
	source_uid = models.ForeignKey(User)
	source_title = models.CharField(max_length=55)
	source_timestamp = models.DateTimeField(default=timezone.now)
	source_utimestamp = models.DateTimeField(default=timezone.now)
	source_ueid = models.IntegerField(blank=True, null=True)
	source_track = models.TextField(blank=True, null=True)
	source_utrack = models.TextField(blank=True, null=True)
	source_status = models.CharField(max_length=10, default='Active', choices=status)

	def __unicode__(self):
		return '%s' % ( self.source_title )


class Booking(models.Model):
	booking_id = models.AutoField(primary_key=True)
	booking_gid = models.ForeignKey('Guest.Guest')
	booking_rid = models.ForeignKey('Room.Room')
	booking_sid = models.ForeignKey(Source,blank=True, null=True)
	booking_amount = models.IntegerField(blank=True)
	booking_discount = models.FloatField(blank=True, default=0)
	booking_service_tax = models.FloatField(default=0)
	booking_luxury_tax = models.FloatField(default=0)
	booking_tax = models.FloatField(blank=True, default=0)
	booking_total = models.FloatField(blank=True, default=0)
	booking_advance = models.FloatField(blank=True, default=0)
	booking_room_count = models.IntegerField(blank=True, default=1)
	booking_duration = models.IntegerField(blank=True, default=1)
	booking_adult = models.IntegerField(blank=True, default=1)
	booking_child = models.IntegerField(blank=True, default=0)
	booking_extra_bed = models.IntegerField(blank=True, default=0)
	booking_messages = models.TextField(blank=True, null=True)
	booking_note = models.TextField(blank=True, null=True)
	booking_arrival = models.DateTimeField(blank=True)
	booking_departure = models.DateTimeField(blank=True)
	booking_checkin_type = models.CharField(max_length=55, default='Perfect', choices=checkin_type)
	booking_checkin = models.DateTimeField(blank=True, null=True)
	booking_checkout = models.DateTimeField(blank=True, null=True)
	booking_expected_checkin = models.DateTimeField(blank=True, null=True)
	booking_expected_checkout = models.DateTimeField(blank=True, null=True)
	booking_timestamp = models.DateTimeField(default=timezone.now)
	booking_utimestamp = models.DateTimeField(default=timezone.now)
	booking_ueid = models.IntegerField(blank=True, null=True)
	booking_track = models.TextField(blank=True, null=True)
	booking_utrack = models.TextField(blank=True, null=True)
	booking_status = models.CharField(max_length=10, default='Active', choices=status)
	booking_tentative_arrival = models.DateTimeField(blank=True, null=True)
	booking_tentative_departure = models.DateTimeField(blank=True, null=True)
	booking_referal_url = models.TextField(blank=True)


	def __unicode__(self):
		return '%s %s %s %s' % (
			self.booking_gid, 
			self.booking_arrival, 
			self.booking_duration,
			self.booking_total
			)


class Travel(models.Model):
	travel_id = models.AutoField(primary_key=True)
	travel_bid = models.ForeignKey(Booking)
	travel_amode = models.CharField(max_length=55,blank=True, null=True)
	travel_atitle = models.TextField(blank=True, null=True)
	travel_atime = models.DateTimeField(blank=True, null=True)
	travel_atask = models.CharField(max_length=55,blank=True, null=True)
	travel_dmode = models.CharField(max_length=55,blank=True, null=True)
	travel_dtitle = models.TextField(blank=True, null=True)
	travel_dtime = models.DateTimeField(blank=True, null=True)
	travel_dtask = models.CharField(max_length=55,blank=True, null=True)
	travel_timestamp = models.DateTimeField(default=timezone.now)
	travel_utimestamp = models.DateTimeField(default=timezone.now)
	travel_ueid = models.IntegerField(blank=True, null=True)
	travel_track = models.TextField(blank=True, null=True)
	travel_utrack = models.TextField(blank=True, null=True)
	travel_status = models.CharField(max_length=10, default='Active', choices=status)

	def __unicode__(self):
		return '%s %s' % ( self.travel_bid,self.travel_atitle )
