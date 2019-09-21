# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


from django.contrib.auth.models import User

# Create your models here.
from django.utils import timezone
import datetime

status = (('Active','Active'), ('Inactive','Inactive'), ('Delete','Delete'))
title = (('Mr','Mr'), ('Mrs','Mrs'))
gender = (('Male','Male'), ('Female','Female'))

class Section(models.Model):
	section_id = models.AutoField(primary_key=True)
	section_uid = models.ForeignKey(User)
	section_title = models.CharField(max_length=50)
	section_slug = models.SlugField()
	section_description = models.TextField(blank=True, null=True)
	section_timestamp = models.DateTimeField(default=timezone.now)
	section_utimestamp = models.DateTimeField(default=timezone.now)
	section_ueid = models.IntegerField(blank=True, null=True)
	section_track = models.TextField(blank=True, null=True)
	section_utrack = models.TextField(blank=True, null=True)
	section_status = models.CharField(max_length=50, default='Active', choices=status)

	def save(self, *args, **kwargs):
		if not self.section_slug:
			self.section_slug = slugify(self.section_title)[:50]
		return super(Section, self).save(*args, **kwargs)


class Staff(models.Model):
	staff_id = models.AutoField(primary_key=True)
	staff_uid = models.ForeignKey(User)
	staff_title = models.CharField(max_length=10, default='Mr', choices=title)
	staff_fname = models.CharField(max_length=50)
	staff_lname = models.CharField(max_length=50, blank=True)
	staff_email = models.EmailField(max_length=50)
	staff_mobile = models.CharField(max_length=15, null=True)
	staff_phone = models.CharField(max_length=15, blank=True, null=True)
	staff_gender = models.CharField(max_length=20, default='Male', choices=gender)
	staff_nationality = models.CharField(max_length=100, blank=True, null=True)
	staff_address = models.TextField(blank=True, null=True)
	staff_country = models.CharField(max_length=100, blank=True, null=True)
	staff_state = models.CharField(max_length=100, blank=True, null=True)
	staff_city = models.CharField(max_length=100, blank=True, null=True)
	staff_zipcode = models.IntegerField(blank=True, null=True)
	staff_timestamp = models.DateTimeField(default=timezone.now)
	staff_utimestamp = models.DateTimeField(default=timezone.now)
	staff_track = models.TextField(blank=True, null=True)
	staff_utrack = models.TextField(blank=True, null=True)
	staff_status = models.CharField(max_length=10, default='Active', choices=status)


	def __unicode__(self):
		return '%s %s' % ( self.staff_fname, self.staff_lname )
