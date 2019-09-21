# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from ckeditor.fields import RichTextField

status = (('Active','Active'), ('Inactive','Inactive'), ('Delete','Delete'))
email_pur = (('Login','Login'), ('Register','Register'), ('Booking','Booking'), ('Payment','Payment'), ('Checkout','Checkout'), ('Cancellation','Cancellation'), ('Invoice','Invoice'), ('feedback','feedback'))

class Email_cron(models.Model):
	email_id = models.AutoField(primary_key=True)
	email_uid = models.ForeignKey(User)
	email_from = models.EmailField(max_length=100)
	email_to = models.EmailField(max_length=100)
	email_subject = models.CharField(max_length=222)
	email_body = RichTextField()
	email_sent = models.BooleanField(default=False)
	email_purpose = models.CharField(max_length=10, default='Login', choices=email_pur)
	email_timestamp = models.DateTimeField(default=timezone.now)
	email_utimestamp = models.DateTimeField(default=timezone.now)
	email_track = models.TextField(blank=True)
	email_utrack = models.TextField(blank=True)
	email_status = models.CharField(max_length=10, default='Active', choices=status)


	def __unicode__(self):
		return '%s %s' % (
			self.email_id,
			self.email_subject 
			
			)
