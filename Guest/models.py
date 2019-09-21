# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


from django.contrib.auth.models import User


from country.models import Country, State


from django.utils import timezone
import datetime
title = (('Mr.','Mr.'), ('Dr.','Dr.'), ('Miss','Miss'), ('Mrs.','Mrs.'), ('Ms.','Ms.'), ('Rabbi','Rabbi'), ('Bishop','Bishop'), ('Father','Father'), ('Reverend','Reverend'), ('Pastor','Pastor'), ('Capt.','Capt.'), ('Gen.','Gen.'), ('Sir','Sir'))
gender = (('Male','Male'), ('Female','Female'))
status = (('Active','Active'), ('Inactive','Inactive'), ('Delete','Delete'))
ID = (('Passport','Passport'), ('License','License'))
Type = (('Normal','Normal'),('VIP','VIP'), ('Blacklist','Blacklist'))
class Guest(models.Model):
	guest_id = models.AutoField(primary_key=True)
	guest_uid = models.ForeignKey(User)
	guest_title = models.CharField(max_length=10, default='Mr', choices=title)
	guest_fname = models.CharField(max_length=50)
	guest_lname = models.CharField(max_length=50, blank=True)
	guest_email = models.EmailField(max_length=50,unique=True)
	guest_mobile = models.CharField(max_length=12)
	guest_gender = models.CharField(max_length=20, default='Male', choices=gender)
	guest_dob = models.DateField(blank=True, null=True)
	guest_nationality = models.CharField(max_length=100, blank=True, null=True)
	guest_address = models.TextField(blank=True, null=True)
	guest_country = models.ForeignKey(Country, blank=True, null=True)
	guest_state = models.ForeignKey(State, blank=True, null=True)
	guest_city = models.CharField(max_length=100, blank=True, null=True)
	guest_zipcode = models.IntegerField(blank=True, null=True)
	guest_type = models.CharField(max_length=100, default='Normal', choices=Type)
	guest_timestamp = models.DateTimeField(default=timezone.now)
	guest_utimestamp = models.DateTimeField(default=timezone.now)
	guest_track = models.TextField(blank=True)
	guest_utrack = models.TextField(blank=True)
	guest_status = models.CharField(max_length=10, default='Active', choices=status)
	guest_previous_stay = models.DateTimeField(default=timezone.now, blank=True)
	guest_future_stay = models.DateTimeField(blank=True, null=True)
	guest_comment = models.TextField(blank=True)
	guest_referal_url = models.TextField(blank=True)

	def publish(self):
        	self.guest_timestamp = timezone.now()
        	self.guest_utimestamp = timezone.now()
        	self.save()
        	send_mail('Subject here', 'Here is the message.', 'info@bookmywp.com', ['vijayjakhar.vj@gmail.com'], fail_silently=False)
        
	def __unicode__(self):
		return '%s %s %s %s' % (
			self.guest_title, 
			self.guest_fname, 
			self.guest_lname, 
			self.guest_mobile
			)
			

class gwork(models.Model):
	gwork_id = models.AutoField(primary_key=True)
	gwork_gid = models.ForeignKey('Guest', on_delete=models.CASCADE, default="")
	gwork_organization = models.CharField(max_length=555,blank=True, null=True)
	gwork_designation = models.CharField(max_length=555,blank=True, null=True)
	gwork_address = models.TextField(blank=True, null=True)
	gwork_country = models.ForeignKey(Country,blank=True, null=True)
	gwork_state = models.ForeignKey(State,blank=True, null=True)
	gwork_city = models.CharField(max_length=555,blank=True, null=True)
	gwork_zipcode = models.IntegerField(blank=True, null=True)
	gwork_email = models.EmailField(max_length=50, blank=True, null=True)
	gwork_phone = models.CharField(max_length=555,blank=True, null=True)
	gwork_mobile = models.CharField(max_length=555,blank=True, null=True)
	gwork_fax = models.CharField(max_length=555,blank=True, null=True)
	gwork_timestamp = models.DateTimeField(default=timezone.now)
	gwork_utimestamp = models.DateTimeField(default=timezone.now)
	#gwork_uaid = models.ForeignKey(User, null=True)
	gwork_track = models.CharField(max_length=555,blank=True, null=True)
	gwork_utrack = models.CharField(max_length=555,blank=True, null=True)
	gwork_status = models.CharField(max_length=10, default='Active', choices=status)

	def publish(self):
		self.gwork_timestamp = timezone.now()
		self.gwork_utimestamp = timezone.now()
		self.save()

	def __unicode__(self):
		return '%s %s %s %s %s' % (
			self.gwork_gid, 
			self.gwork_organization, 
			self.gwork_designation, 
			self.gwork_country, 
			self.gwork_mobile
			)
		

class gother(models.Model):
	gother_id = models.AutoField(primary_key=True)
	gother_gid = models.ForeignKey('Guest', on_delete=models.CASCADE, default="")
	gother_preferences = models.TextField(blank=True, null=True)
	gother_details = models.TextField(blank=True, null=True)
	gother_spouse_title = models.CharField(max_length=555,blank=True, null=True)
	gother_spouse_fname = models.CharField(max_length=555,blank=True, null=True)
	gother_spouse_lname = models.CharField(max_length=555,blank=True, null=True)
	gother_birthday = models.DateTimeField(default=timezone.now, null=True)
	gother_anniversory = models.DateTimeField(default=timezone.now, null=True)
	gother_timestamp = models.DateTimeField(default=timezone.now, null=True)
	gother_utimestamp = models.DateTimeField(default=timezone.now, null=True)
	gother_track = models.CharField(max_length=555,blank=True, null=True)
	gother_utrack = models.CharField(max_length=555,blank=True, null=True)
	gother_status = models.CharField(max_length=10, default='Active', choices=status)

	def __unicode__(self):
		return '%s %s %s %s' % (
			self.gother_gid, 
			self.gother_spouse_fname, 
			self.gother_spouse_lname, 
			self.gother_spouse_title
			)
	

