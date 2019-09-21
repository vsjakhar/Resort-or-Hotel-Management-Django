# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
import datetime
from management.models import Staff
#from enum import Enum

status = (('Active','Active'), ('Inactive','Inactive'), ('Delete','Delete'))
condition = (('Dirty','Dirty'), ('Clean','Clean'), ('Active','Active'), ('Maintenance','Maintenance'),('DNR','DNR'))
class Room_type(models.Model):
	room_type_id = models.AutoField(primary_key=True)
	room_type_uid = models.ForeignKey(User)
	room_type_title = models.CharField(max_length=100)
	room_type_slug = models.SlugField(null=True, blank=True)
	room_type_facilities = models.TextField(blank=True)
	room_type_price = models.IntegerField()
	room_type_image = models.FileField(upload_to='room_type/%Y/%m/%d', null = True)
	room_type_timestamp = models.DateTimeField(default=timezone.now)
	room_type_utimestamp = models.DateTimeField(blank=True, null=True)
	room_type_track = models.TextField(blank=True)
	room_type_utrack = models.TextField(blank=True)
	room_type_number = models.IntegerField(blank=True)
	room_title_status = models.CharField(max_length=10, default='Active', choices=status)
	
	def __unicode__(self):
		return '%s %s %s' % (self.room_type_slug, self.room_title_status, self.room_type_title)

	def save(self, *args, **kwargs):
		if not self.room_type_slug:
			self.room_type_slug = slugify(self.room_type_title)[:50]
		return super(Room_type, self).save(*args, **kwargs)

class Room(models.Model):
	room_id = models.AutoField(primary_key=True)
	room_uid = models.ForeignKey(User)
	room_type_id = models.ForeignKey(Room_type)
	room_sid = models.ForeignKey(Staff,blank=True, null=True,verbose_name='Assign To Staff')
	room_number = models.IntegerField()
	room_title = models.CharField(max_length=200)
	room_slug = models.SlugField(null=True, blank=True)
	room_condition = models.CharField(max_length=15, choices=condition)
	room_amount = models.IntegerField(blank=True, null=True)
	room_type = models.CharField(max_length=200, blank=True, null=True)
	room_image = models.FileField(upload_to='room/%Y/%m/%d', blank=True, null=True)
	room_timestamp = models.DateTimeField(blank=True, null=True)
	room_utimestamp = models.DateTimeField(blank=True, null=True)
	room_track = models.TextField(blank=True)
	room_utrack = models.TextField(blank=True)
	room_history = models.TextField(blank=True)
	room_status = models.CharField(max_length=15, default='Active', choices=status)

	def __unicode__(self):
		return '%s %s %s' % (self.room_number, self.room_condition, self.room_type)

	def save(self, *args, **kwargs):
		if not self.room_slug:
			self.room_slug = slugify(self.room_title)[:50]
		return super(Room, self).save(*args, **kwargs)

