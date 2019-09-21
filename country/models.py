# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
from crum import get_current_request

class Country(models.Model):
	country_id = models.AutoField(primary_key=True)
	country_uid = models.ForeignKey(User)
	country_title = models.CharField(max_length=222)
	country_code = models.IntegerField()
	country_iso = models.CharField(max_length=222)
	country_timestamp = models.DateTimeField(default=timezone.now)
	country_track = models.TextField(blank=True, null=True)
	

	def __unicode__(self):
		return '%s' % (
			self.country_title, 
			)

	def save(self, *args, **kwargs):
		request = get_current_request()
		self.country_track = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
		
		super(Country, self).save(*args, **kwargs)

class State(models.Model):
	state_id = models.AutoField(primary_key=True)
	state_uid = models.ForeignKey(User)
	state_ctid = models.ForeignKey(Country)
	state_title = models.CharField(max_length=222)
	state_timestamp = models.DateTimeField(default=timezone.now)
	state_track = models.TextField(blank=True, null=True)
	

	def __unicode__(self):
		return '%s' % (
			self.state_title, 
			)

	def save(self, *args, **kwargs):
		request = get_current_request()
		self.state_track = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
		
		super(State, self).save(*args, **kwargs)

