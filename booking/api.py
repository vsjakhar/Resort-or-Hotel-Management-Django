# -*- coding: utf-8 -*-
from tastypie.authorization import Authorization
from tastypie import fields
from django.db import models
from django.contrib.auth.models import User
from tastypie.resources import ModelResource,ALL, Resource
from .models import Source, Booking, Travel
from jakhar.api import urlencodeSerializer, AdminApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization, ReadOnlyAuthorization, Authorization
from Guest.api import GuestResource
#from management.api import StaffResource
from Room.api import Room_typeResource, RoomResource
from Room.models import Room, Room_type
from payment.models import Payment, Folio
from Guest.models import Guest, gother
from tastypie.exceptions import BadRequest
from django.db import IntegrityError
import dateutil.parser
from dateutil.parser import parse
import datetime
from crum import get_current_request
from django.core.mail import send_mail
from django.utils import timezone
import pytz

from email_cronjob.models import Email_cron


class SourceResource(ModelResource):
	#travel_bid = fields.ForeignKey(BookingResource, 'travel_bid', full=True)
	class Meta:
		queryset = Source.objects.all()
		resource_name = 'source'
		allowed_methods = ['get']
		limit = 0
		always_return_data = True
		authentication = AdminApiKeyAuthentication()
		authorization = Authorization()
		serializer = urlencodeSerializer()


class BookingResource(ModelResource):
	booking_gid = fields.ForeignKey(GuestResource, 'booking_gid', full=True)
	booking_rid = fields.ForeignKey(RoomResource, 'booking_rid', full=True)
	booking_sid = fields.ForeignKey(SourceResource, 'booking_sid', full=True, blank=True, null=True)
	class Meta:
		queryset = Booking.objects.all()
		resource_name = 'booking'
		#allowed_methods = ['get', 'post', 'delete', 'put']
		filtering = {
			'booking_arrival': ALL,
			'booking_id': ALL,
			'booking_checkin': ALL,
			'booking_checkout': ALL,
			'booking_status': ALL,
			'booking_timestamp': ALL,
			
		}
		limit = 0
		always_return_data = True
		authentication = AdminApiKeyAuthentication()
		authorization = Authorization()
		serializer = urlencodeSerializer()

	def alter_list_data_to_serialize(self, request, data):
		total_amount = 0.0
		for i in data[ 'objects' ]:
			total_amount += i.data[ 'booking_total' ]

		return { 'meta' : data[ 'meta' ], 'objects' : data[ 'objects' ], 'total_amount' : total_amount }

	def obj_create(self, bundle, request=None, **kwargs):
		username = bundle.request.GET['username']
		user = User.objects.get(username=username)
		if user.has_perm('booking.add_booking'):
		
			datetim = bundle.data.get('booking_arrival', '')
			hari = dateutil.parser.parse(datetim).date()
			ramm = datetime.datetime.combine(hari, datetime.time(13, 59))
			arrive = str(ramm)		

			datetim1 = bundle.data.get('booking_departure', '')
			hari1 = dateutil.parser.parse(datetim1).date()
			ramm1 = datetime.datetime.combine(hari1, datetime.time(12, 01))
			depart = str(ramm1)

			# deptime = datetime.datetime.strptime(datetim1, '%Y-%m-%d %H:%M:%S')
			# bundle.data['booking_departure'] = deptime + datetime.timedelta(days=1)

			#checking for departure not less than or equal to arrival date
			if datetim1 <= datetim:
				raise Exception("Give the appropriate date for the departure")
			
			roome = bundle.data.get('booking_rid', '')
			a = roome.split('/')
			b = a[4]
			shyam = Booking.objects.filter(booking_rid__room_id = b).filter(booking_arrival__lte = depart).filter(booking_departure__gte = arrive).filter(booking_status='Active')
			
			if shyam:			
				raise Exception('already booked')
			else:			
				bundle = super(BookingResource, self).obj_create(bundle)
				bundle.obj.save()

			booking_guest = bundle.data.get('booking_gid', '')
			x = booking_guest.split('/')
			y = x[4]
			guest = Guest.objects.get(guest_id=y)
			email = guest.guest_email #"singhprabhanshu5@gmail.com"
			fname1 = bundle.obj.booking_gid.guest_fname
			lname1 = bundle.obj.booking_gid.guest_lname
			title1 = bundle.obj.booking_gid.guest_title
			fname = str(fname1)
			lname = str(lname1)
			title = str(title1)

			bookid = bundle.obj.booking_id
			bkid = str(bookid)
			arrival1 = str(datetim)
			departure1 = str(datetim1)
			dat_arrival = datetime.datetime.strptime(arrival1, '%Y-%m-%d %H:%M:%S').strftime('%d, %B %Y')
			dat_departure = datetime.datetime.strptime(departure1, '%Y-%m-%d %H:%M:%S').strftime('%d, %B %Y')
			arrival = str(dat_arrival)
			departure = str(dat_departure)
			booking_amount = bundle.obj.booking_total
			amount = str(booking_amount)
			room_no = bundle.obj.booking_rid.room_number
			room_nos = str(room_no)
			room_type = bundle.obj.booking_rid.room_type_id.room_type_title
			types = str(room_type)

			html_content = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><title>welcome aura</title><style type="text/css">/* Take care of image borders and formatting */img{max-width: 600px;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;}a img{border: none;}table{border-collapse: collapse !important;}#outlook a{padding:0;}.ReadMsgBody{width: 100%;}.ExternalClass{width:100%;}.backgroundTable{margin:0 auto; padding:0; width:100%;}table td{border-collapse: collapse;}.ExternalClass *{line-height: 115%;}/* General styling */td{font-family: Arial;color: #6f6f6f;}body{-webkit-font-smoothing:antialiased;-webkit-text-size-adjust:none;width: 100%;height: 100%;color: #6f6f6f;font-weight: 400;font-size: 18px;}h1{margin: 10px 0;}a{color: #27aa90;text-decoration: none;}.force-full-width{width: 100% !important;}.force-width-80{width: 80% !important;}.body-padding{padding: 0 75px;}.mobile-align{text-align: right;}</style><style type="text/css" media="screen">@media screen{@import url(http://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600,900);/* Thanks Outlook 2013! */*{font-family: "Arial" !important;}.w280{width: 280px !important;}}</style><style type="text/css" media="only screen and (max-width: 480px)">/* Mobile styles */@media only screen and (max-width: 480px){table[class*="w320"]{width: 320px !important;}td[class*="w320"]{width: 280px !important;padding-left: 20px !important;padding-right: 20px !important;}img[class*="w320"]{width: 250px !important;height: 67px !important;}td[class*="mobile-spacing"]{padding-top: 10px !important;padding-bottom: 10px !important;}*[class*="mobile-hide"]{display: none !important;}*[class*="mobile-br"]{font-size: 12px !important;}td[class*="mobile-w20"]{width: 20px !important;}img[class*="mobile-w20"]{width: 20px !important;}td[class*="mobile-center"]{text-align: center !important;}table[class*="w100p"]{width: 100% !important;}td[class*="activate-now"]{padding-right: 0 !important;padding-top: 20px !important;}td[class*="mobile-block"]{display: block !important;}td[class*="mobile-align"]{text-align: left !important;}}</style></head><body offset="0" class="body" style="padding:0; margin:0; display:block; -webkit-text-size-adjust:none" bgcolor="#eeebeb"><table align="center" cellpadding="0" cellspacing="0" width="100%" height="100%" ><tr><td align="center" valign="top" width="100%"><center style="font-family: Arial;"><table cellspacing="0" cellpadding="0" width="600" class="w320"><tr><td align="center" valign="top"><table cellspacing="0" cellpadding="0" width="100%" style="background-color:#3bcdb0;"><tr><td style="background-color:#3bcdb0;"><table style="margin:0 auto;" cellspacing="0" cellpadding="0" width="100%"></table><table cellspacing="0" cellpadding="0" width="100%"><tr><td style="font-size:20px; font-weight: 600; color: #ffffff; text-align:center;" class="mobile-spacing"><div class="mobile-br">&nbsp;</div>Thank you for choosing Auragoa Spa Retreat Resort.<br></td></tr><tr><td style="font-size:16px; text-align:center; padding: 5px 75px; color: #6f6f6f;" class="w320 mobile-spacing">We are pleased to confirm your reservation as under:</td></tr></table><table cellspacing="0" cellpadding="0" width="100%"><tr><td><img src="http://demodevelopment.in/mail_img/s_design12.png" style="max-width:100%; display:block;"></td></tr></table><table class="mobile" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td class="icon54" align="center"><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="170"><tbody><tr><td class="icon34" valign="top" align="center" width="100%"><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="fullCenter" cellspacing="0" cellpadding="0" align="right" border="0" width="175"><tbody><tr><td height="25" width="100%"></td></tr><tr><td style="text-align: center; font-family:Arial; font-size: 18px; color: #ffffff; line-height: 18px; font-weight: 600;" class="fullCenter" valign="middle" width="100%">Booking id: '+bkid+'</td></tr><tr><td height="10" width="100%"></td></tr><tr><td style="text-align: center; font-family:Arial; font-size: 15px; color: #ffffff; line-height: 24px; font-weight: 600;" class="fullCenter" valign="middle" width="100%">Dear '+title+' '+fname+' '+lname+'</td></tr></tbody></table></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="60" width="100%"></td></tr></tbody></table></td></tr></tbody></table></td></tr></table><table cellspacing="0" cellpadding="0" width="100%" bgcolor="#ffffff" ><tr><td style="background-color:#ffffff;"><table style=" text-align: center; margin-top:48px;margin-bottom:48px; font-size: 13px;" cellspacing="0" cellpadding="0" border="0" width="100%"><tbody><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Name of Guest</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+title+' '+fname+' '+lname+'</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Date of Arrival</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+arrival+'</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Date of Departure</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+departure+'</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Accommodation</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+types+'</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Amount to be pay</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+amount+'/-(inclusive all taxes)</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Check In</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+arrival+'</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="20%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Check Out</b></td><td width="20%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+departure+'</td><td width="20%"></td></tr></tbody></table><table style="margin:0 auto;" cellspacing="0" cellpadding="10" width="100%"><tr><td style="text-align:center; margin:0 auto;"><br><div><a href="http://auragoa.com/"style="background-color:#f5774e;color:#ffffff;display:inline-block;font-family:Arial;font-size:18px;font-weight:400;line-height:45px;text-align:center;text-decoration:none;width:180px;-webkit-text-size-adjust:none;border-radius:20px;">Term & Conditions</a></div><br></td></tr></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td valign="top" bgcolor="#344b61" align="center" width="100%"><table class="mobile" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td align="center"><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="10" width="100%"></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="600"><tbody><tr><td align="center" width="100%"><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="fullCenter" cellspacing="0" cellpadding="0" align="left" border="0" width="140"><tbody><tr><td style="text-align: center;font-family: Helvetica, Arial, sans-serif;font-size: 12px;color: #ffffff;line-height: 15px;font-weight: 400;padding-left: 30px;" class="fullCenter" valign="middle" width="200px">Aura Goa Wellness Resort, Mandrem, North Goa<br>+91 76653-22222<br>info@auragoa.com<br><a href="http://auragoa.com/" style="text-decoration: none; color: #ffffff;">auragoa.com</a></td></tr></tbody></table><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="full" cellspacing="0" cellpadding="0" align="left" border="0" width="20"><tbody><tr><td height="1" width="100%"></td></tr></tbody></table><table style="text-align: right; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="buttonScale" cellspacing="0" cellpadding="0" align="right" border="0" width="96"><tbody><tr><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"><a href="https://twitter.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_1.png" alt="" class="hover" border="0" width="17"></a></td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://www.facebook.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_2.png" alt="" class="hover" border="0" width="17"></a></td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://plus.google.com/u/0/103796393489619851236" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_3.png" alt="" class="hover" border="0" width="17"></a></td></tr></tbody></table></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="10" width="100%"></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></table></td></tr></table></center></td></tr></table></body></html>'
			#send_mail('Booking Confirmed', 'Someone Just Logined from your Account if that was not you then Contact to Admin. Logined at '+str(timezone.now())+' Time ', 'Auragoa <donotreply@auragoa.com>', [email], html_message=html_content, fail_silently=False)

			sender = 'donotreply@auragoa.com'
			receiver = email
			subject = 'Booking_Room'
			body = html_content
			purpose = 'Booking'
			Email_cron.objects.create(email_uid_id = user.id, email_from=sender, email_to=receiver, email_subject=subject, email_body=body, email_purpose=purpose)




		else:
			raise Exception('Permission Denied')

		
		return bundle

	def obj_update(self, bundle, request=None, **kwargs):
		username = bundle.request.GET['username']
		user = User.objects.get(username=username)


		if user.has_perm('booking.change_booking'):
			ram = bundle.data.get('booking_checkout')
			cancel = bundle.data.get('booking_status')
			#if self.booking_checkout.null:
			if not ram:
				if not cancel:
					bundle = super(BookingResource, self).obj_update(bundle, request=None, **kwargs)
				else:
					bundle = super(BookingResource, self).obj_update(bundle, request=None, **kwargs)
					email3 = bundle.obj.booking_gid.guest_email
					fname3 = str(bundle.obj.booking_gid.guest_fname)
					lname3 = str(bundle.obj.booking_gid.guest_lname)
					html_content2 = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head> <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/> <meta name="viewport" content="width=device-width, initial-scale=1"/> <title>feedback aura</title> <style type="text/css"> /* Take care of image borders and formatting */ img{max-width: 600px; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic;}a img{border: none;}table{border-collapse: collapse !important;}#outlook a{padding:0;}.ReadMsgBody{width: 100%;}.ExternalClass{width:100%;}.backgroundTable{margin:0 auto; padding:0; width:100%;}table td{border-collapse: collapse;}.ExternalClass *{line-height: 115%;}/* General styling */ td{font-family: Arial, sans-serif; color: #6f6f6f;}body{-webkit-font-smoothing:antialiased; -webkit-text-size-adjust:none; width: 100%; height: 100%; color: #6f6f6f; font-weight: 400; font-size: 18px;}h1{margin: 10px 0;}a{color: #27aa90; text-decoration: none;}.force-full-width{width: 100% !important;}.force-width-80{width: 80% !important;}.body-padding{padding: 0 75px;}.mobile-align{text-align: right;}</style> <style type="text/css" media="screen"> @media screen{@import url(http://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600,900); /* Thanks Outlook 2013! */ *{font-family: "Source Sans Pro", "Helvetica Neue", "Arial", "sans-serif" !important;}.w280{width: 280px !important;}}</style> <style type="text/css" media="only screen and (max-width: 480px)"> /* Mobile styles */ @media only screen and (max-width: 480px){table[class*="w320"]{width: 320px !important;}td[class*="w320"]{width: 280px !important; padding-left: 20px !important; padding-right: 20px !important;}img[class*="w320"]{width: 250px !important; height: 67px !important;}td[class*="mobile-spacing"]{padding-top: 10px !important; padding-bottom: 10px !important;}*[class*="mobile-hide"]{display: none !important;}*[class*="mobile-br"]{font-size: 12px !important;}td[class*="mobile-w20"]{width: 20px !important;}img[class*="mobile-w20"]{width: 20px !important;}td[class*="mobile-center"]{text-align: center !important;}table[class*="w100p"]{width: 100% !important;}td[class*="activate-now"]{padding-right: 0 !important; padding-top: 20px !important;}td[class*="mobile-block"]{display: block !important;}td[class*="mobile-align"]{text-align: left !important;}}</style></head><body offset="0" class="body" style="padding:0; margin:0; display:block; -webkit-text-size-adjust:none" bgcolor="#eeebeb"> <table align="center" cellpadding="0" cellspacing="0" width="100%" height="100%" > <tr> <td align="center" valign="top" width="100%"> <center style="font-family: Calibri, Verdana, Ariel, sans-serif;"> <table cellspacing="0" cellpadding="0" width="600" class="w320"> <tr> <td align="center" valign="top"> <table cellspacing="0" cellpadding="0" width="100%" style="background-color:#3bcdb0;"> <tr> <td style="background-color:#3bcdb0;"> <table style="margin:0 auto;" cellspacing="0" cellpadding="0" width="100%"> </table> <table cellspacing="0" cellpadding="0" width="100%"> <tr> <td> <img src="http://demodevelopment.in/mail_img/s_design12.png" style="max-width:100%; display:block;"> </td></tr></table> </td></tr></table> <table cellspacing="0" cellpadding="0" width="100%" bgcolor="#ffffff" > <tr> <td style="background-color:#ffffff;padding: 0px 30px !important;"> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="600"> <tbody> <tr> <td align="center" width="100%"> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"> <tbody> <tr> <td height="60" width="100%"></td></tr></tbody> </table> <table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="fullCenter" cellspacing="0" cellpadding="0" align="center" border="0" width="600"> <tbody> <tr> <td style="text-align: center; font-family: Helvetica, Arial, sans-serif, "Open Sans"; font-size: 20px; color: #444444; line-height: 32px; font-weight: 700;" class="fullCenter" valign="middle" width="100%"> Dear '+fname3+' '+lname3+' </td></tr><tr> <td height="30" width="100%"></td></tr><tr> <td width="100%"> <table cellspacing="0" cellpadding="0" align="center" border="0" width="100"> <tbody> <tr> <td style="font-size: 1px; line-height: 1px;" bgcolor="#808080" height="1" width="100">&nbsp;</td></tr></tbody> </table> </td></tr><tr> <td height="30" width="100%"></td></tr><tr> <td style="text-align: left; font-family: Helvetica, Arial, sans-serif, "Open Sans"; font-size: 14px; color: #808080; line-height: 22px; font-weight: 400;" class="fullCenter" valign="middle" width="100%"> Thank you for choosing <strong>Auragoa</strong> for your recent stay in Goa. We have read your comments about the hotel and we greatly appreciate that you took the time to write them, as guests satisfaction is our priority. </td></tr><tr> <td height="25" width="100%"></td></tr><tr> <td style="text-align: left; font-family: Helvetica, Arial, sans-serif, "Open Sans"; font-size: 14px; color: #808080; line-height: 22px; font-weight: 400;" class="fullCenter" valign="middle" width="100%"> We invite you, to share your opinion, using the following rattings: </td></tr><tr> <td height="25" width="100%"></td></tr><tr> <table style="margin: 0 auto;" class="force-width-80" cellspacing="0" cellpadding="0"> <tbody><tr> <td class="pusher">&nbsp;</td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_03_0.gif" alt="0"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_03.gif" alt="1"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_04.gif" alt="2"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_05.gif" alt="3"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_06.gif" alt="4"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_07.gif" alt="5"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_08.gif" alt="6"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_09.gif" alt="8"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_10.gif" alt="9"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_11.gif" alt="10"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_12.gif" alt="10"> </a> </td><td class="pusher">&nbsp;</td></tr></tbody></table> </tr><tr> <td height="25" width="100%"></td></tr><tr> <td style="text-align: left; font-family: Helvetica, Arial, sans-serif, "Open Sans"; font-size: 14px; color: #808080; line-height: 22px; font-weight: 400;" class="fullCenter" valign="middle" width="100%"> It is very important for us that guests experiences are shared. </td></tr><tr> <td height="25" width="100%"></td></tr><tr> <td style="text-align: left; font-family: Helvetica, Arial, sans-serif, "Open Sans"; font-size: 14px; color: #808080; line-height: 22px; font-weight: 400;" class="fullCenter" valign="middle" width="100%"> It was a pleasure to have you as our guest. We would like to take this opportunity to thank you for your collaboration and we hope to see you again soon at <strong>Auragoa</strong>. </td></tr><tr> <td height="25" width="100%"></td></tr><tr> <td style="text-align: left; font-family: Helvetica, Arial, sans-serif, "Open Sans"; font-size: 14px; color: #808080; line-height: 22px; font-weight: 400;" class="fullCenter" valign="middle" width="100%"> <strong>Management</strong>,<br><strong>Aura Goa Wellness Resort</strong><br></td></tr></tbody> </table> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"> <tbody> <tr> <td height="60" width="100%"></td></tr></tbody> </table> </td></tr></tbody> </table> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"> <tbody> <tr> <td valign="top" bgcolor="#344b61" align="center" width="100%"> <table class="mobile" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"> <tbody> <tr> <td align="center"> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"> <tbody> <tr> <td height="10" width="100%"></td></tr></tbody> </table> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="600"> <tbody> <tr> <td align="center" width="100%"> <table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="fullCenter" cellspacing="0" cellpadding="0" align="left" border="0" width="140"> <tbody> <tr> <td style="text-align: center;font-family: Helvetica, Arial, sans-serif;font-size: 12px;color: #ffffff;line-height: 15px;font-weight: 400;padding-left: 30px;" class="fullCenter" valign="middle" width="200px"> Aura Goa Wellness Resort, Mandrem, North Goa <br>+91 76653-22222<br>info@auragoa.com<br><a href="http://auragoa.com/" style="text-decoration: none; color: #ffffff;"> auragoa.com</a> </td></tr></tbody> </table> <table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="full" cellspacing="0" cellpadding="0" align="left" border="0" width="20"> <tbody> <tr> <td height="1" width="100%"></td></tr></tbody> </table> <table style="text-align: right; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="buttonScale" cellspacing="0" cellpadding="0" align="right" border="0" width="96"> <tbody> <tr> <td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://twitter.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_1.png" alt="" class="hover" border="0" width="17"></a> </td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://www.facebook.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_2.png" alt="" class="hover" border="0" width="17"></a> </td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://plus.google.com/u/0/103796393489619851236" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_3.png" alt="" class="hover" border="0" width="17"></a> </td></tr></tbody> </table> </td></tr></tbody> </table> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"> <tbody> <tr> <td height="10" width="100%"></td></tr></tbody> </table> </td></tr></tbody> </table> </td></tr></tbody> </table> </td></tr></table> </td></tr></table> </center> </td></tr></table> </body> </html>'
					#send_mail('Cancel_Feedback Report', 'Someone Just Logined from your Account if that was not you then Contact to Admin. Logined at '+str(timezone.now())+' Time ', 'Auragoa <donotreply@auragoa.com>', [email3], html_message = html_content2, fail_silently=False)

					sender = 'donotreply@auragoa.com'
					receiver = email3
					subject = 'Cancel_Feedback Report'
					body = html_content2
					purpose = 'Cancellation'
					Email_cron.objects.create(email_uid_id = user.id, email_from=sender, email_to=receiver, email_subject=subject, email_body=body, email_purpose=purpose)


					
			else:
				
				x = kwargs['pk']
				field = Payment.objects.filter(payment_bid__booking_id=x)
				sield = Folio.objects.filter(folio_bid__booking_id=x)
				booking = Booking.objects.get(booking_id=x)
				p = booking.booking_total
				n = 0
				k = 0
				for i in field:
					n = n + i.payment_total
				for l in sield:
					k = k + l.folio_total
				bundle.data['payment_due'] = k + p - n
				bundle.data['payment_total'] = n
				bundle.data['folio_total'] = k
				bundle.data['booking_checkout'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
				due = k + p - n
				demo = str(due)
				#if due>0:
				if due > 10 or due < -10:
					raise Exception('your payment_due is: Rs.'+ demo)
				else:
					bundle = super(BookingResource, self).obj_update(bundle, request=None, **kwargs)
					room = str(bundle.obj.booking_rid.room_number)
					bkid = str(bundle.obj.booking_id)
					gid = str(bundle.obj.booking_gid.guest_id)
					arriv_dat = bundle.obj.booking_checkin

					#format1 = "%Y-%m-%d %H:%M:%S"
					#now_utc = bundle.obj.booking_checkin
					#raise Exception(now_utc)
					arriv_dat_timezone = arriv_dat.astimezone(pytz.timezone('Asia/Kolkata'))
					#raise Exception(now_asia.strftime(format))
					#raise Exception(now_asia.strftime("%Y-%m-%d %H:%M:%S"))
					arriv_dat_timezone_format = str(arriv_dat_timezone.strftime("%Y-%m-%d %H:%M:%S"))


					arrival_time = arriv_dat_timezone_format[11:19]
					#raise Exception(arriv_dat_slice)
					depart_dat = bundle.obj.booking_checkout
					depart_dat_timezone = depart_dat.astimezone(pytz.timezone('Asia/Kolkata'))
					depart_dat_timezone_format = str(depart_dat_timezone.strftime("%Y-%m-%d %H:%M:%S"))
					departure_time = depart_dat_timezone_format[11:19]
					#raise Exception(depart_dat)
					arrival_date = str(dateutil.parser.parse(str(arriv_dat)).date())
					departure_date = str(dateutil.parser.parse(str(depart_dat)).date())
					# at = datetime.datetime.strptime(arriv_dat, "%Y-%m-%d %H:%M:%S")
					# dt = datetime.datetime.strptime(depart_dat, "%Y-%m-%d %H:%M:%S")
					# arrival_time = str(at.time().strftime('%H:%M:%S'))
					# departure_time = str(dt.time().strftime('%H:%M:%S'))
					fname = str(bundle.obj.booking_gid.guest_fname)
					lname = str(bundle.obj.booking_gid.guest_lname)
					room_type = str(bundle.obj.booking_rid.room_type_id.room_type_title)
					room_tarrif = bundle.obj.booking_amount
					luxury_tax = bundle.obj.booking_luxury_tax
					service_tax = bundle.obj.booking_service_tax
					discount = bundle.obj.booking_discount
					pay_frm_restaurant = Payment.objects.filter(payment_from="Restaurant").filter(payment_bid__booking_id=bundle.obj.booking_id)
					pay_frm_spa = Payment.objects.filter(payment_from="Spa").filter(payment_bid__booking_id=bundle.obj.booking_id)
					#raise Exception(pay_frm_spa)
					total_restaurant = 0
					total_spa = 0
					if pay_frm_restaurant:
						for g in pay_frm_restaurant:
							total_restaurant += g.payment_total
					if pay_frm_spa:
						for h in pay_frm_spa:
							total_spa += h.payment_total

					#raise Exception(total_spa)
					a = room_tarrif + luxury_tax
					b = a + service_tax
					c = b - discount
					d = c + total_restaurant
					e = d + total_spa


					email = bundle.obj.booking_gid.guest_email
					html_content1 = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head> <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/> <meta name="viewport" content="width=device-width, initial-scale=1"/> <title>feedback aura</title> <style type="text/css"> /* Take care of image borders and formatting */ img{max-width: 600px; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic;}a img{border: none;}table{border-collapse: collapse !important;}#outlook a{padding:0;}.ReadMsgBody{width: 100%;}.ExternalClass{width:100%;}.backgroundTable{margin:0 auto; padding:0; width:100%;}table td{border-collapse: collapse;}.ExternalClass *{line-height: 115%;}/* General styling */ td{font-family: Arial, sans-serif; color: #6f6f6f;}body{-webkit-font-smoothing:antialiased; -webkit-text-size-adjust:none; width: 100%; height: 100%; color: #6f6f6f; font-weight: 400; font-size: 18px;}h1{margin: 10px 0;}a{color: #27aa90; text-decoration: none;}.force-full-width{width: 100% !important;}.force-width-80{width: 80% !important;}.body-padding{padding: 0 75px;}.mobile-align{text-align: right;}</style> <style type="text/css" media="screen"> @media screen{@import url(http://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600,900); /* Thanks Outlook 2013! */ *{font-family: "Source Sans Pro", "Helvetica Neue", "Arial", "sans-serif" !important;}.w280{width: 280px !important;}}</style> <style type="text/css" media="only screen and (max-width: 480px)"> /* Mobile styles */ @media only screen and (max-width: 480px){table[class*="w320"]{width: 320px !important;}td[class*="w320"]{width: 280px !important; padding-left: 20px !important; padding-right: 20px !important;}img[class*="w320"]{width: 250px !important; height: 67px !important;}td[class*="mobile-spacing"]{padding-top: 10px !important; padding-bottom: 10px !important;}*[class*="mobile-hide"]{display: none !important;}*[class*="mobile-br"]{font-size: 12px !important;}td[class*="mobile-w20"]{width: 20px !important;}img[class*="mobile-w20"]{width: 20px !important;}td[class*="mobile-center"]{text-align: center !important;}table[class*="w100p"]{width: 100% !important;}td[class*="activate-now"]{padding-right: 0 !important; padding-top: 20px !important;}td[class*="mobile-block"]{display: block !important;}td[class*="mobile-align"]{text-align: left !important;}}</style></head><body offset="0" class="body" style="padding:0; margin:0; display:block; -webkit-text-size-adjust:none" bgcolor="#eeebeb"> <table align="center" cellpadding="0" cellspacing="0" width="100%" height="100%" > <tr> <td align="center" valign="top" width="100%"> <center style="font-family: Calibri, Verdana, Ariel, sans-serif;"> <table cellspacing="0" cellpadding="0" width="600" class="w320"> <tr> <td align="center" valign="top"> <table cellspacing="0" cellpadding="0" width="100%" style="background-color:#3bcdb0;"> <tr> <td style="background-color:#3bcdb0;"> <table style="margin:0 auto;" cellspacing="0" cellpadding="0" width="100%"> </table> <table cellspacing="0" cellpadding="0" width="100%"> <tr> <td> <img src="http://demodevelopment.in/mail_img/s_design12.png" style="max-width:100%; display:block;"> </td></tr></table> </td></tr></table> <table cellspacing="0" cellpadding="0" width="100%" bgcolor="#ffffff" > <tr> <td style="background-color:#ffffff;padding: 0px 30px !important;"> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="600"> <tbody> <tr> <td align="center" width="100%"> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"> <tbody> <tr> <td height="60" width="100%"></td></tr></tbody> </table> <table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="fullCenter" cellspacing="0" cellpadding="0" align="center" border="0" width="600"> <tbody> <tr> <td style="text-align: center; font-family: Helvetica, Arial, sans-serif, "Open Sans"; font-size: 20px; color: #444444; line-height: 32px; font-weight: 700;" class="fullCenter" valign="middle" width="100%"> Dear '+fname+' '+lname+' </td></tr><tr> <td height="30" width="100%"></td></tr><tr> <td width="100%"> <table cellspacing="0" cellpadding="0" align="center" border="0" width="100"> <tbody> <tr> <td style="font-size: 1px; line-height: 1px;" bgcolor="#808080" height="1" width="100">&nbsp;</td></tr></tbody> </table> </td></tr><tr> <td height="30" width="100%"></td></tr><tr> <td style="text-align: left; font-family: Helvetica, Arial, sans-serif, "Open Sans"; font-size: 14px; color: #808080; line-height: 22px; font-weight: 400;" class="fullCenter" valign="middle" width="100%"> Thank you for choosing <strong>Auragoa</strong> for your recent stay in Goa. We have read your comments about the hotel and we greatly appreciate that you took the time to write them, as guests satisfaction is our priority. </td></tr><tr> <td height="25" width="100%"></td></tr><tr> <td style="text-align: left; font-family: Helvetica, Arial, sans-serif, "Open Sans"; font-size: 14px; color: #808080; line-height: 22px; font-weight: 400;" class="fullCenter" valign="middle" width="100%"> We invite you, to share your opinion, using the following rattings: </td></tr><tr> <td height="25" width="100%"></td></tr><tr> <table style="margin: 0 auto;" class="force-width-80" cellspacing="0" cellpadding="0"> <tbody><tr> <td class="pusher">&nbsp;</td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_03_0.gif" alt="0"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_03.gif" alt="1"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_04.gif" alt="2"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_05.gif" alt="3"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_06.gif" alt="4"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_07.gif" alt="5"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_08.gif" alt="6"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_09.gif" alt="8"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_10.gif" alt="9"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_11.gif" alt="10"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_12.gif" alt="10"> </a> </td><td class="pusher">&nbsp;</td></tr></tbody></table> </tr><tr> <td height="25" width="100%"></td></tr><tr> <td style="text-align: left; font-family: Helvetica, Arial, sans-serif, "Open Sans"; font-size: 14px; color: #808080; line-height: 22px; font-weight: 400;" class="fullCenter" valign="middle" width="100%"> It is very important for us that guests experiences are shared. </td></tr><tr> <td height="25" width="100%"></td></tr><tr> <td style="text-align: left; font-family: Helvetica, Arial, sans-serif, "Open Sans"; font-size: 14px; color: #808080; line-height: 22px; font-weight: 400;" class="fullCenter" valign="middle" width="100%"> It was a pleasure to have you as our guest. We would like to take this opportunity to thank you for your collaboration and we hope to see you again soon at <strong>Auragoa</strong>. </td></tr><tr> <td height="25" width="100%"></td></tr><tr> <td style="text-align: left; font-family: Helvetica, Arial, sans-serif, "Open Sans"; font-size: 14px; color: #808080; line-height: 22px; font-weight: 400;" class="fullCenter" valign="middle" width="100%"> <strong>Management</strong>,<br><strong>Aura Goa Wellness Resort</strong><br></td></tr></tbody> </table> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"> <tbody> <tr> <td height="60" width="100%"></td></tr></tbody> </table> </td></tr></tbody> </table> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"> <tbody> <tr> <td valign="top" bgcolor="#344b61" align="center" width="100%"> <table class="mobile" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"> <tbody> <tr> <td align="center"> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"> <tbody> <tr> <td height="10" width="100%"></td></tr></tbody> </table> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="600"> <tbody> <tr> <td align="center" width="100%"> <table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="fullCenter" cellspacing="0" cellpadding="0" align="left" border="0" width="140"> <tbody> <tr> <td style="text-align: center;font-family: Helvetica, Arial, sans-serif;font-size: 12px;color: #ffffff;line-height: 15px;font-weight: 400;padding-left: 30px;" class="fullCenter" valign="middle" width="200px"> Aura Goa Wellness Resort, Mandrem, North Goa <br>+91 76653-22222<br>info@auragoa.com<br><a href="http://auragoa.com/" style="text-decoration: none; color: #ffffff;"> auragoa.com</a> </td></tr></tbody> </table> <table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="full" cellspacing="0" cellpadding="0" align="left" border="0" width="20"> <tbody> <tr> <td height="1" width="100%"></td></tr></tbody> </table> <table style="text-align: right; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="buttonScale" cellspacing="0" cellpadding="0" align="right" border="0" width="96"> <tbody> <tr> <td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://twitter.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_1.png" alt="" class="hover" border="0" width="17"></a> </td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://www.facebook.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_2.png" alt="" class="hover" border="0" width="17"></a> </td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://plus.google.com/u/0/103796393489619851236" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_3.png" alt="" class="hover" border="0" width="17"></a> </td></tr></tbody> </table> </td></tr></tbody> </table> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"> <tbody> <tr> <td height="10" width="100%"></td></tr></tbody> </table> </td></tr></tbody> </table> </td></tr></tbody> </table> </td></tr></table> </td></tr></table> </center> </td></tr></table> </body> </html>'
					##html_content = '<!DOCTYPE html><html xmlns=http://www.w3.org/1999/xhtml><meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"><head><meta content="text/html; charset=UTF-8" http-equiv="Content-Type"><meta content="width=device-width,initial-scale=1" name="viewport"><title>Payment</title><head><style>img{max-width:600px;outline:0;text-decoration:none;-ms-interpolation-mode:bicubic}a img{border:none}table{border-collapse:collapse!important}#outlook a{padding:0}.ReadMsgBody{width:100%}.ExternalClass{width:100%}.backgroundTable{margin:0 auto;padding:0;width:100%!important}table td{border-collapse:collapse}.ExternalClass *{line-height:115%}.container-for-gmail-android{min-width:600px}*{font-family:Helvetica,Arial,sans-serif}body{-webkit-font-smoothing:antialiased;-webkit-text-size-adjust:none;width:100%!important;margin:0!important;height:100%;color:#676767}td{font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#777;text-align:center;line-height:21px}a{color:#676767;text-decoration:none!important}.pull-left{text-align:left}.pull-right{text-align:right}.header-lg,.header-md,.header-sm{font-size:32px;font-weight:700;line-height:normal;padding:35px 0 0;color:#4d4d4d}.header-md{font-size:24px}.header-sm{padding:5px 0;font-size:18px;line-height:1.3}.content-padding{padding:20px 0 5px}.mobile-header-padding-right{width:290px;text-align:right;padding-left:10px}.mobile-header-padding-left{width:290px;text-align:left;padding-left:10px}.free-text{width:100%!important;padding:10px 60px 0}.button{padding:30px 0}.mini-block{border:1px solid #e5e5e5;border-radius:5px;background-color:#fff;padding:12px 15px 15px;text-align:left;width:253px}.mini-container-left{width:278px;padding:10px 0 10px 15px}.mini-container-right{width:278px;padding:10px 14px 10px 15px}.product{text-align:left;vertical-align:top;width:175px}.total-space{padding-bottom:8px;display:inline-block}.item-table{padding:50px 20px;width:560px}.item{width:300px}.mobile-hide-img{text-align:left;width:125px}.mobile-hide-img img{border:1px solid #e6e6e6;border-radius:4px}.title-dark{border-bottom:1px solid #ccc;color:#4d4d4d;font-weight:700;padding-bottom:5px}.item-col{padding-top:20px;vertical-align:top}.force-width-gmail{min-width:600px;height:0!important;line-height:1px!important;font-size:1px!important}</style><style media=screen>@import url(http://fonts.googleapis.com/css?family=Oxygen:400,700);</style><style media=screen>@media screen{*{font-family:Oxygen,"Helvetica Neue",Arial,sans-serif!important}}</style><style media="only screen and (max-width:480px)">@media only screen and (max-width:480px){table[class*=container-for-gmail-android]{min-width:290px!important;width:100%!important}img[class=force-width-gmail]{display:none!important;width:0!important;height:0!important}table[class=w320]{width:320px!important}td[class*=mobile-header-padding-left]{width:160px!important;padding-left:0!important}td[class*=mobile-header-padding-right]{width:160px!important;padding-right:0!important}td[class=header-lg]{font-size:24px!important;padding-bottom:5px!important}td[class=content-padding]{padding:5px 0 5px!important}td[class=button]{padding:5px 5px 30px!important}td[class*=free-text]{padding:10px 18px 30px!important}td[class~=mobile-hide-img]{display:none!important;height:0!important;width:0!important;line-height:0!important}td[class~=item]{width:140px!important;vertical-align:top!important}td[class~=quantity]{width:50px!important}td[class~=price]{width:90px!important}td[class=item-table]{padding:30px 20px!important}td[class=mini-container-left],td[class=mini-container-right]{padding:0 15px 15px!important;display:block!important;width:290px!important}}</style></head><body bgcolor=#f7f7f7><table cellpadding=0 cellspacing=0 width=100% class=container-for-gmail-android align=center><tr><td class=content-padding width=100% style="background-color:#3BCDB0" valign=top align=center><center><table cellpadding=0 cellspacing=0 width=600 class=w320><tr><td class=w320><table cellpadding=0 cellspacing=0 width=100%><tr><td class=mini-container-left><table cellpadding=0 cellspacing=0 width=100%><tr><td class=mini-block-padding><table cellpadding=0 cellspacing=0 width=100% style="border-collapse:separate!important"><tr><td><img src=http://auragoa.com/wp-content/uploads/2017/01/aura-goa-logofinal.png></table></table><td class=mini-container-right><table cellpadding=0 cellspacing=0 width=100%><tr><td class=mini-block-padding><table cellpadding=0 cellspacing=0 width=100% style=border-collapse:separate!important><tr><td class="item-col quantity" style="text-align:center"><span class=total-space style="font-weight:700;color:#4d4d4d">Aura Goa Wellness Resort </span><span style="color:#4d4d4d" class=total-space>near R D khalp school,</span><br><span style="color:#4d4d4d" class=total-space>Mandrem,</span><br><span style="color:#4d4d4d" class=total-space>North Goa.</span><br></table></table></table><tr><td class=w320><table cellpadding=0 cellspacing=0 width=100%><tr><td class=mini-container-left><table cellpadding=0 cellspacing=0 width=100%><tr><td class=mini-block-padding><table cellpadding=0 cellspacing=0 width=100% style="border-collapse:separate!important"><tr><td class=mini-block><b>Room #</b> '+room+'<br><b>Checkin Date :</b> '+arrival_date+'<br><b>Checkout Date :</b> '+departure_date+'<br><b>Room Type :</b> '+room_type+'<br></table></table><td class=mini-container-right><table cellpadding=0 cellspacing=0 width=100%><tr><td class=mini-block-padding><table cellpadding=0 cellspacing=0 width=100% style="border-collapse:separate!important"><tr><td class=mini-block><b>Invoice #</b> '+gid+''+bkid+'<br><b>Arr. Time : </b>'+arrival_time+'<br><b>Dep. Time :</b> '+departure_time+'<br><b>Page #</b> 1</table></table></table></table></center><tr><td width=100% style="background-color:#fff;border-top:1px solid #e5e5e5;border-bottom:1px solid #e5e5e5"valign=top align=center><center><table cellpadding=0 cellspacing=0 width=600 class=w320><tr><td class=item-table><table cellpadding=0 cellspacing=0 width=100%><tr><td class=title-dark width=100>Date<td class=title-dark width=100>Description<td class=title-dark width=100>Document<td class=title-dark width=100>Debited<td class=title-dark width=100>Credited<td class=title-dark width=100>Balance<tr><td class="item-col item"><table cellpadding=0 cellspacing=0 width=100%><tr><td class=product>'+arrival_date+'</table><td class=item-col>Room Tariff<td class=item-col>1234<td class=item-col>'+str(room_tarrif)+'<td class=item-col><td class=item-col>'+str(room_tarrif)+'<tr><td class="item-col item"><table cellpadding=0 cellspacing=0 width=100%><tr><td class=product>'+arrival_date+'</table><td class=item-col>Luxury Tax<td class=item-col>1234<td class=item-col>'+str(luxury_tax)+'<td class=item-col><td class=item-col>'+str(a)+'<tr><td class="item-col item"><table cellpadding=0 cellspacing=0 width=100%><tr><td class=product>'+arrival_date+'</table><td class=item-col>Service Tax<td class=item-col>1234<td class=item-col>'+str(service_tax)+'<td class=item-col><td class=item-col>'+str(b)+'<tr><td class="item-col item"><table cellpadding=0 cellspacing=0 width=100%><tr><td class=product>'+arrival_date+'</table><td class=item-col>Discount<td class=item-col>Discount<td class=item-col><td class=item-col>'+str(discount)+'<td class=item-col>'+str(c)+'<tr><td class="item-col item"><table cellpadding=0 cellspacing=0 width=100%><tr><td class=product>05/04/2017</table><td class=item-col>In House Guest<br> F & B<td class=item-col>1234<td class=item-col>'+str(total_restaurant)+'<td class=item-col><td class=item-col>'+str(d)+'<tr><td class="item-col item"><table cellpadding=0 cellspacing=0 width=100%><tr><td class=product>05/04/2017</table><td class=item-col>In House Guest<br> F & B<td class=item-col>1234<td class=item-col>'+str(total_spa)+'<td class=item-col><td class=item-col>'+str(e)+'<tr><td class="item-col item mobile-row-padding"><td class="item-col quantity"><td class="item-col price"><tr><td class="item-col item"><td class="item-col item"><td class="item-col item"><td class="item-col item"><td class="item-col quantity" style="text-align:right;padding-right:10px;border-top:1px solid #ccc"><span class=total-space>Discount</span><br><span class=total-space>Tax</span><br><span class=total-space style="font-weight:700;color:#4d4d4d">Total</span><td class="item-col price" style="text-align:left;border-top:1px solid #ccc"><span class=total-space>4000</span><br><span class=total-space>4000</span><br><span class=total-space style="font-weight:700;color:#4d4d4d">4000</span></table></table></center><tr><td style="background-color:#344B61;height:100px;padding:20px" valign="top" width="100%" align="center"><center><table cellpadding="0" cellspacing="0" width="600" class="w320"><tbody><tr><td class="fullCenter" style="text-align:center;font-family:Helvetica,Arial,sans-serif;font-size:12px;color:white;line-height:15px;font-weight:400;padding-left:30px;line-height:2" valign="middle" width="200px">Aura Goa Wellness Resort, Mandrem, North Goa <br>+91 76653-22222 <br> <a style="text-decoration:none;color:white">info@auragoa.com </a> <br> <a href="http://auragoa.com/" style="text-decoration:none;color:white">auragoa.com </a></td><td class="mobile-header-padding-right pull-right"> <a href="https://twitter.com/aurasparetreat"> <img src="http://s3.amazonaws.com/swu-filepicker/k8D8A7SLRuetZspHxsJk_social_08.gif" alt="twitter" height="47" width="44"> </a> <a href="https://www.facebook.com/aurasparetreat"> <img src="http://s3.amazonaws.com/swu-filepicker/LMPMj7JSRoCWypAvzaN3_social_09.gif" alt="facebook" height="47" width="38"> </a></td></tr></tbody></table></center></td></tr></table></body></html>'
					html_content = '<!DOCTYPE html><html xmlns=http://www.w3.org/1999/xhtml><meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"><head><meta content="text/html; charset=UTF-8" http-equiv="Content-Type"><meta content="width=device-width,initial-scale=1" name="viewport"><title>Payment</title><head><style>img{max-width:600px;outline:0;text-decoration:none;-ms-interpolation-mode:bicubic}a img{border:none}table{border-collapse:collapse!important}#outlook a{padding:0}.ReadMsgBody{width:100%}.ExternalClass{width:100%}.backgroundTable{margin:0 auto;padding:0;width:100%!important}table td{border-collapse:collapse}.ExternalClass *{line-height:115%}.container-for-gmail-android{min-width:600px}*{font-family:Helvetica,Arial,sans-serif}body{-webkit-font-smoothing:antialiased;-webkit-text-size-adjust:none;width:100%!important;margin:0!important;height:100%;color:#676767}td{font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#777;text-align:center;line-height:21px}a{color:#676767;text-decoration:none!important}.pull-left{text-align:left}.pull-right{text-align:right}.header-lg,.header-md,.header-sm{font-size:32px;font-weight:700;line-height:normal;padding:35px 0 0;color:#4d4d4d}.header-md{font-size:24px}.header-sm{padding:5px 0;font-size:18px;line-height:1.3}.content-padding{padding:20px 0 5px}.mobile-header-padding-right{width:290px;text-align:right;padding-left:10px}.mobile-header-padding-left{width:290px;text-align:left;padding-left:10px}.free-text{width:100%!important;padding:10px 60px 0}.button{padding:30px 0}.mini-block{border:1px solid #e5e5e5;border-radius:5px;background-color:#fff;padding:12px 15px 15px;text-align:left;width:253px}.mini-container-left{width:278px;padding:10px 0 10px 15px}.mini-container-right{width:278px;padding:10px 14px 10px 15px}.product{text-align:left;vertical-align:top;width:175px}.total-space{padding-bottom:8px;display:inline-block}.item-table{padding:50px 20px;width:560px}.item{width:300px}.mobile-hide-img{text-align:left;width:125px}.mobile-hide-img img{border:1px solid #e6e6e6;border-radius:4px}.title-dark{border-bottom:1px solid #ccc;color:#4d4d4d;font-weight:700;padding-bottom:5px}.item-col{padding-top:20px;vertical-align:top}.force-width-gmail{min-width:600px;height:0!important;line-height:1px!important;font-size:1px!important}</style><style media=screen>@import url(http://fonts.googleapis.com/css?family=Oxygen:400,700);</style><style media=screen>@media screen{*{font-family:Oxygen,"Helvetica Neue",Arial,sans-serif!important}}</style><style media="only screen and (max-width:480px)">@media only screen and (max-width:480px){table[class*=container-for-gmail-android]{min-width:290px!important;width:100%!important}img[class=force-width-gmail]{display:none!important;width:0!important;height:0!important}table[class=w320]{width:320px!important}td[class*=mobile-header-padding-left]{width:160px!important;padding-left:0!important}td[class*=mobile-header-padding-right]{width:160px!important;padding-right:0!important}td[class=header-lg]{font-size:24px!important;padding-bottom:5px!important}td[class=content-padding]{padding:5px 0 5px!important}td[class=button]{padding:5px 5px 30px!important}td[class*=free-text]{padding:10px 18px 30px!important}td[class~=mobile-hide-img]{display:none!important;height:0!important;width:0!important;line-height:0!important}td[class~=item]{width:140px!important;vertical-align:top!important}td[class~=quantity]{width:50px!important}td[class~=price]{width:90px!important}td[class=item-table]{padding:30px 20px!important}td[class=mini-container-left],td[class=mini-container-right]{padding:0 15px 15px!important;display:block!important;width:290px!important}}</style></head><body bgcolor=#f7f7f7><table cellpadding=0 cellspacing=0 width=100% class=container-for-gmail-android align=center><tr><td class=content-padding width=100% style="background-color:#3BCDB0" valign=top align=center><center><table cellpadding=0 cellspacing=0 width=600 class=w320><tr><td class=w320><table cellpadding=0 cellspacing=0 width=100%><tr><td class=mini-container-left><table cellpadding=0 cellspacing=0 width=100%><tr><td class=mini-block-padding><table cellpadding=0 cellspacing=0 width=100% style="border-collapse:separate!important"><tr><td><img src=http://auragoa.com/wp-content/uploads/2017/01/aura-goa-logofinal.png></table></table><td class=mini-container-right><table cellpadding=0 cellspacing=0 width=100%><tr><td class=mini-block-padding><table cellpadding=0 cellspacing=0 width=100% style=border-collapse:separate!important><tr><td class="item-col quantity" style="text-align:center"><span class=total-space style="font-weight:700;color:#4d4d4d">Aura Goa Wellness Resort </span><span style="color:#4d4d4d" class=total-space>near R D khalp school,</span><br><span style="color:#4d4d4d" class=total-space>Mandrem,</span><br><span style="color:#4d4d4d" class=total-space>North Goa.</span><br></table></table></table><tr><td class=w320><table cellpadding=0 cellspacing=0 width=100%><tr><td class=mini-container-left><table cellpadding=0 cellspacing=0 width=100%><tr><td class=mini-block-padding><table cellpadding=0 cellspacing=0 width=100% style="border-collapse:separate!important"><tr><td class=mini-block><b>Guest:</b> '+fname+' '+lname+'<br><b>Room Type :</b> '+room_type+'<br><b>checkin Date :</b> '+arrival_date+'<br><b>Checkout Date :</b> '+departure_date+'<br></table></table><td class=mini-container-right><table cellpadding=0 cellspacing=0 width=100%><tr><td class=mini-block-padding><table cellpadding=0 cellspacing=0 width=100% style="border-collapse:separate!important"><tr><td class=mini-block><b>Invoice #</b> '+gid+''+bkid+'<br><b>Room # : </b>'+room+'<br><b>Checkin Time :</b> '+arrival_time+'<br><b>Checkout Time</b> '+departure_time+'</table></table></table></table></center><tr><td width=100% style="background-color:#fff;border-top:1px solid #e5e5e5;border-bottom:1px solid #e5e5e5"valign=top align=center><center><table cellpadding=0 cellspacing=0 width=600 class=w320><tr><td class=item-table><table cellpadding=0 cellspacing=0 width=100%><tr><td class=title-dark width=100>Date<td class=title-dark width=100>Description<td class=title-dark width=100>Debited<td class=title-dark width=100>Credited<td class=title-dark width=100>Balance<tr><td class="item-col item"><table cellpadding=0 cellspacing=0 width=100%><tr><td class=product>'+arrival_date+'</table><td class=item-col>Room Tariff<td class=item-col>'+str(room_tarrif)+'<td class=item-col><td class=item-col>'+str(room_tarrif)+'<tr><td class="item-col item"><table cellpadding=0 cellspacing=0 width=100%><tr><td class=product>'+arrival_date+'</table><td class=item-col>Luxury Tax<td class=item-col>'+str(luxury_tax)+'<td class=item-col><td class=item-col>'+str(a)+'<tr><td class="item-col item"><table cellpadding=0 cellspacing=0 width=100%><tr><td class=product>'+arrival_date+'</table><td class=item-col>Service Tax<td class=item-col>'+str(service_tax)+'<td class=item-col><td class=item-col>'+str(b)+'<tr><td class="item-col item"><table cellpadding=0 cellspacing=0 width=100%><tr><td class=product>'+arrival_date+'</table><td class=item-col>Discount<td class=item-col><td class=item-col>'+str(discount)+'<td class=item-col>'+str(c)+'<tr><td colspan="2" class=item-col>In House Guest F & B<td class=item-col>'+str(total_restaurant)+'<td class=item-col><td class=item-col>'+str(d)+'<tr><td colspan="2" class=item-col>Payment From Spa<td class=item-col>'+str(total_spa)+'<td class=item-col><td class=item-col>'+str(e)+'<tr><td class="item-col item mobile-row-padding"><td class="item-col quantity"><td class="item-col price"><tr><td class="item-col item"><td class="item-col item"><td class="item-col item"><td class="item-col quantity" style="text-align:right;padding-right:10px;border-top:1px solid #ccc"><span class=total-space style="font-weight:700;color:#4d4d4d">Total</span><td class="item-col price" style="border-top:1px solid #ccc"><span class=total-space>'+str(e)+'</span></table></table></center><tr><td style="background-color:#344B61;height:100px;padding:20px" valign="top" width="100%" align="center"><center><table cellpadding="0" cellspacing="0" width="600" class="w320"><tbody><tr><td class="fullCenter" style="text-align:center;font-family:Helvetica,Arial,sans-serif;font-size:12px;color:white;line-height:15px;font-weight:400;padding-left:30px;line-height:2" valign="middle" width="200px">Aura Goa Wellness Resort, Mandrem, North Goa <br>+91 76653-22222 <br> <a style="text-decoration:none;color:white">info@auragoa.com </a> <br> <a href="http://auragoa.com/" style="text-decoration:none;color:white">auragoa.com </a></td><td class="mobile-header-padding-right pull-right"> <a href="https://twitter.com/aurasparetreat"> <img src="http://s3.amazonaws.com/swu-filepicker/k8D8A7SLRuetZspHxsJk_social_08.gif" alt="twitter" height="47" width="44"> </a> <a href="https://www.facebook.com/aurasparetreat"> <img src="http://s3.amazonaws.com/swu-filepicker/LMPMj7JSRoCWypAvzaN3_social_09.gif" alt="facebook" height="47" width="38"> </a></td></tr></tbody></table></center></td></tr></table></body></html>'
					#send_mail('Auragoa Invoice', 'Someone Just Logined from your Account if that was not you then Contact to Admin. Logined at '+str(timezone.now())+' Time ', 'Auragoa <donotreply@auragoa.com>', [email], html_message = html_content, fail_silently=False)
					#send_mail('Feedback Report', 'Someone Just Logined from your Account if that was not you then Contact to Admin. Logined at '+str(timezone.now())+' Time ', 'Auragoa <donotreply@auragoa.com>', [email], html_message = html_content1, fail_silently=False)

					sender = 'donotreply@auragoa.com'
					receiver = email
					subject = 'Auragoa Invoice'
					body = html_content
					purpose = 'Invoice'
					Email_cron.objects.create(email_uid_id = user.id, email_from=sender, email_to=receiver, email_subject=subject, email_body=body, email_purpose=purpose)

					sender = 'donotreply@auragoa.com'
					receiver = email
					subject = 'Feedback Report'
					body = html_content1
					purpose = 'Feedback'
					Email_cron.objects.create(email_uid_id = user.id, email_from=sender, email_to=receiver, email_subject=subject, email_body=body, email_purpose=purpose)


		else:
			raise Exception('Permission Denied')
		
		return bundle

	def hydrate(self, bundle):
		request = get_current_request()
		emp = bundle.request.GET['username']
		emp1 = User.objects.get(username = emp)
		t = int(emp1.id)
		checkin = bundle.data.get('booking_checkin')
		

		 
		if request.method == 'POST':
			bundle.data['booking_track'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['booking_utrack'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['booking_referal_url'] = request.META['HTTP_REFERER']
			bundle.data['booking_ueid'] = t
			amount = bundle.data.get('booking_amount')
			disc = bundle.data.get('booking_discount')
			amount = int(amount)
			if disc:
				discount = disc
			else:
				discount = 0

			x = amount - int(discount)
			# service tax
			tax1 = (x * (float(9)/100)) 
			# luxury tax
			if amount >= 3000 and amount < 5000:
				tax2 = (amount * (float(9)/100))
			else:
				tax2 = (amount * (float(12)/100))

			bundle.data['booking_service_tax'] = tax1
			bundle.data['booking_luxury_tax'] = tax2
			bundle.data['booking_tax'] = tax1 + tax2
			bundle.data['booking_total'] = tax1 + tax2 + x

			#GST Tax
			if x<=1000:
				bundle.data['booking_tax'] = 0
			elif x<=2500:
				bundle.data['booking_tax'] = x*0.12
			elif x<=7500:
				bundle.data['booking_tax'] = x*0.18
			else:
				bundle.data['booking_tax'] = x*0.28

			bundle.data['booking_total'] = x+bundle.data['booking_tax']

			if checkin:
				bundle.data['booking_checkin'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


		elif request.method == 'PUT':
			# emp = bundle.request.GET['username']
			# emp1 = User.objects.get(username = emp)
			# t = int(emp1.id)
			bundle.data['booking_utrack'] = request.META['REMOTE_ADDR'] #+ ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['booking_utimestamp'] = timezone.now()
			bundle.data['booking_ueid'] = t
			if checkin:
				bundle.data['booking_checkin'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

		return bundle

	# showing guest preference in booking from gother_preferences	
	def dehydrate(self, bundle):
		gid = bundle.obj.booking_gid.guest_id
		tbid = bundle.obj.booking_id
		preferences = gother.objects.filter(gother_gid__guest_id=gid)
		travel = Travel.objects.filter(travel_bid=tbid)
		if preferences:
			for i in preferences:
				bundle.data['booking_guest_preferences'] = i.gother_preferences

		if travel:
			for i in travel:
				bundle.data['booking_travel_detail'] = {'travel_id':i.travel_id, 'travel_bid':i.travel_bid, 'travel_amode':i.travel_amode, 'travel_atitle':i.travel_atitle, 'travel_atime':i.travel_atime, 'travel_atask':i.travel_atask, 'travel_dmode':i.travel_dmode, 'travel_dtitle':i.travel_dtitle, 'travel_dtime':i.travel_dtime, 'travel_dtask':i.travel_dtask, 'travel_timestamp':i.travel_timestamp, 'travel_utimestamp':i.travel_utimestamp, 'travel_ueid':i.travel_ueid, 'travel_track':i.travel_track, 'travel_utrack':i.travel_utrack, 'travel_status':i.travel_status}
		return bundle

	

class Booking_detailResource(ModelResource):
	booking_gid = fields.ForeignKey(GuestResource, 'booking_gid', full=True)
	booking_rid = fields.ForeignKey(RoomResource, 'booking_rid', full=True)
	#folio_detail = fields.ForeignKey(FolioResource, 'folio', full=True)
	class Meta:
		queryset = Booking.objects.all()
		resource_name = 'booking_detail'
		#allowed_methods = ['get', 'post', 'delete', 'put']
		filtering = {
			'booking_arrival': ALL,
			'booking_id': ALL
		}
		limit = 0
		always_return_data = True
		authentication = AdminApiKeyAuthentication()
		authorization = Authorization()
		serializer = urlencodeSerializer()

	def obj_get_list(self, bundle, **kwargs):
		y = bundle.request.GET['id']
		objects = Booking.objects.filter(booking_id=y)
		return objects

	def dehydrate(self, bundle):
		x = bundle.request.GET['id']
		field = Payment.objects.filter(payment_bid__booking_id=x)
		sield = Folio.objects.filter(folio_bid__booking_id=x)
		booking = Booking.objects.get(booking_id=x)
		p = booking.booking_total
		n = 0
		k = 0
		a=0
		b=0
		ram = {}
		shyam = {}
		for i in field:
			n = n + i.payment_total
			shyam[a] = {'payment_amount':i.payment_amount, 'payment_bid':i.payment_bid, 'payment_description':i.payment_description, 'payment_disc_res':i.payment_disc_res, 'payment_discount':i.payment_discount, 'payment_gid':i.payment_gid, 'payment_id':i.payment_id, 'payment_invoice':i.payment_invoice, 'payment_mode':i.payment_mode, 'payment_receipt':i.payment_receipt, 'payment_tax':i.payment_tax, 'payment_total':i.payment_total, 'payment_type':i.payment_type}
			bundle.data['payment'] = shyam
			a+=1
			
		for l in sield:
			k = k + l.folio_total
			ram[b] = {'folio_amount':l.folio_amount, 'folio_bid':l.folio_bid, 'folio_description':l.folio_description, 'folio_disc_res':l.folio_disc_res, 'folio_discount':l.folio_discount, 'folio_from':l.folio_from, 'folio_gid':l.folio_gid, 'folio_id':l.folio_id, 'folio_invoice':l.folio_invoice, 'folio_price':l.folio_price, 'folio_receipt':l.folio_receipt, 'folio_tax':l.folio_tax, 'folio_title':l.folio_title, 'folio_total':l.folio_total, 'folio_type':l.folio_type}
			bundle.data['folio'] = ram
			b+=1
			
		bundle.data['payment_due'] = k + p - n 
		bundle.data['payment_total'] = n
		bundle.data['folio_total'] = k		
		
		return bundle

class TravelResource(ModelResource):
	travel_bid = fields.ForeignKey(BookingResource, 'travel_bid', full=True)
	class Meta:
		queryset = Travel.objects.all()
		resource_name = 'travel'
		#allowed_methods = ['get', 'post', 'delete', 'put']
		# filtering = {
		# 	'booking_arrival': ALL,
		# 	'booking_id': ALL,
		# 	'booking_checkin': ALL,
		# 	'booking_checkout': ALL
		# }
		limit = 0
		always_return_data = True
		authentication = AdminApiKeyAuthentication()
		authorization = Authorization()
		serializer = urlencodeSerializer()

class Room_availResource(ModelResource):

   
    room_type_id = fields.ForeignKey(Room_typeResource, 'room_type_id', full=True, blank=True, null=True)
    
    class Meta:
       
        queryset = Room.objects.all()
        resource_name = 'room_avail'
        filtering = {
        	'room_condition': ALL,
        }
        
        limit = 0
        always_return_data = True
        authentication = AdminApiKeyAuthentication()
        authorization = Authorization()
        serializer = urlencodeSerializer()

    def obj_get_list(self, bundle, **kwargs):
        b_start = bundle.request.GET['arrival']
        b_end = bundle.request.GET['departure']
        room = Room.objects.all()
        booking = Room.objects.filter(booking__booking_arrival__lte = b_end, booking__booking_departure__gte = b_start, booking__booking_status='Active')
        objects = room.exclude(room_id__in = booking)
        
        return objects

class DaybookingResource(ModelResource):
	booking_gid = fields.ForeignKey(GuestResource, 'booking_gid', full=True)
	booking_rid = fields.ForeignKey(RoomResource, 'booking_rid', full=True)
	class Meta:
		queryset = Booking.objects.all()
		resource_name = 'daybook'
		allowed_methods = ['get', 'post', 'delete', 'put', 'patch']
		filtering = {
			'booking_arrival': ALL,
			'booking_id': ALL,
			'booking_status': ALL
		}
		limit = 0
		always_return_data = True
		authentication = AdminApiKeyAuthentication()
		authorization = Authorization()
		serializer = urlencodeSerializer()

	def obj_get_list(self, bundle, **kwargs):
		y = bundle.request.GET['date']
		hari1 = dateutil.parser.parse(y).date()
		ramm = datetime.datetime.combine(hari1, datetime.time.max)
		l = datetime.datetime.combine(hari1, datetime.time.min)
		z = str(ramm)
		l1 = str(l)
		#x = datetime.date(y)
		#raise Exception(ramm)
		objects = Booking.objects.filter(booking_arrival__lte=z).filter(booking_departure__gte=l1).filter(booking_status='Active')
		return objects

class RangebookingObject(object):
	def __init__(self, initial=None):
		self.__dict__['_data'] = {}
		if initial:
			self.update(initial)
	def __getattr__(self, name):
		return self._data.get(name, None)

	def __setattr__(self, name, value):
		self.__dict__['_data'][name] = value

	def update(self, other):
		for k in other:
			self.__setattr__(k, other[k])

	def to_dict(self):
		return self._data
 
class RangebookingResource(Resource):
	class Meta:
		resource_name = 'rangebooking'
		fields = ['value']
		allowed_methods = ['get']
		object_class = RangebookingObject
		serializers = urlencodeSerializer
		include_resource_uri = False

	def detail_uri_kwargs(self, bundle_or_obj ):
		kwargs = {}
		if isinstance(bundle_or_obj, Bundle):
			kwargs['value'] = bundle_or_obj.obj.value
		else:
			kwargs['value'] = bundle_or_obj.value
		return kwargs

	def get_obj_list(self, request):
		return [self.obj_get()]

	def obj_get_list(self, request=None, **kwargs):
		return [self.obj_get()]

	def obj_get(self, request=None, key=None, **kwargs):
		setting = RangebookingObject()

	def dehydrate(self, bundle):
		a = bundle.request.GET['start']
		b = bundle.request.GET['end']

		l = dateutil.parser.parse(a).date()
		m = datetime.datetime.combine(l, datetime.time.max)
		h = datetime.datetime.combine(l, datetime.time.min)
		n = str(m)

		x = dateutil.parser.parse(b).date()
		y = datetime.datetime.combine(x, datetime.time.max)
		z = str(y)


		#ram = {}
		#filt = Booking.objects.filter(booking_arrival__lte=n).filter(booking_departure__gte=n)
		t = x + datetime.timedelta(days=1)
		k = int((t-l).days)
		count1 = 0
		p = 0
		for i in range(k):
			
			s = str(m)
			h1 = str (h)
			filt = Booking.objects.filter(booking_arrival__lte=s).filter(booking_departure__gte=h1)
			count = filt.count()
			count1 = count1 + count
			bundle.data['Total_count'] = count1
			m = m + datetime.timedelta(days=1)
			h = h + datetime.timedelta(days=1)
			shyam = {}
			
			ram = {}

			g = 0
			dateslice = s[0:10]
			ram['booking_count'] = count
			
			for u in filt:
				shyam[g] = {'booking_id':u.booking_id, 'booking_arrival':u.booking_arrival, 'booking_departure':u.booking_departure, 'booking_amount':u.booking_amount}
				ram['booking'] = shyam
				ram['booking_date'] = dateslice
				#ram['booking_count'] = count
				#bundle.data[dateslice] = ram
				g = g + 1

			bundle.data[p] = ram
			
			p = p + 1
			
				
			
			
			# shyam[m] = Booking.objects.filter(booking_arrival__lte=s).filter(booking_departure__gte=s)
			# bundle.data['saka'] = shyam
		return bundle

class BookingguestResource(ModelResource):
	booking_gid = fields.ForeignKey(GuestResource, 'booking_gid', full=True)
	booking_rid = fields.ForeignKey(RoomResource, 'booking_rid', full=True)
	booking_sid = fields.ForeignKey(SourceResource, 'booking_sid', full=True, blank=True, null=True)
	class Meta:
		queryset = Booking.objects.all()
		resource_name = 'bookingguest'
		#allowed_methods = ['get', 'post', 'delete', 'put']
		filtering = {
			'booking_arrival': ALL,
			'booking_id': ALL,
			'booking_checkin': ALL,
			'booking_checkout': ALL,
			'booking_timestamp': ALL
		}
		limit = 0
		always_return_data = True
		authentication = AdminApiKeyAuthentication()
		authorization = Authorization()
		serializer = urlencodeSerializer()

	def obj_create(self, bundle, request=None, **kwargs):
		username = bundle.request.GET['username']
		user = User.objects.get(username=username)
		if user.has_perm('booking.add_booking'):
		
			datetim = bundle.data.get('booking_arrival', '')
			hari = dateutil.parser.parse(datetim).date()
			ramm = datetime.datetime.combine(hari, datetime.time.min)
			arrive = str(ramm)		

			datetim1 = bundle.data.get('booking_departure', '')
			hari1 = dateutil.parser.parse(datetim1).date()
			ramm1 = datetime.datetime.combine(hari1, datetime.time.min)
			depart = str(ramm1)
			
			roome = bundle.data.get('booking_rid', '')
			a = roome.split('/')
			b = a[4]
			shyam = Booking.objects.filter(booking_rid__room_id = b).filter(booking_arrival__lte = depart).filter(booking_departure__gte = arrive)
			
			if shyam:			
				raise Exception('already booked')
			else:			
				bundle = super(BookingguestResource, self).obj_create(bundle)
				bundle.obj.save()

			# booking_guest = bundle.data.get('booking_gid', '')
			# x = booking_guest.split('/')
			# y = x[4]
			# guest = Guest.objects.get(guest_id=y)
			email = bundle.obj.booking_gid.guest_email#guest.guest_email #"singhprabhanshu5@gmail.com"
			fname1 = bundle.obj.booking_gid.guest_fname
			lname1 = bundle.obj.booking_gid.guest_lname
			title1 = bundle.obj.booking_gid.guest_title
			fname = str(fname1)
			lname = str(lname1)
			title = str(title1)

			bookid = bundle.obj.booking_id
			bkid = str(bookid)
			arrival1 = str(datetim)
			departure1 = str(datetim1)
			dat_arrival = datetime.datetime.strptime(arrival1, '%Y-%m-%d %H:%M:%S').strftime('%d, %B %Y')
			dat_departure = datetime.datetime.strptime(departure1, '%Y-%m-%d %H:%M:%S').strftime('%d, %B %Y')
			arrival = str(dat_arrival)
			departure = str(dat_departure)
			booking_amount = bundle.obj.booking_amount
			amount = str(booking_amount)
			room_no = bundle.obj.booking_rid.room_number
			room_nos = str(room_no)
			room_type = bundle.obj.booking_rid.room_type_id.room_type_title
			types = str(room_type)

			html_content = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><title>welcome aura</title><style type="text/css">/* Take care of image borders and formatting */img{max-width: 600px;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;}a img{border: none;}table{border-collapse: collapse !important;}#outlook a{padding:0;}.ReadMsgBody{width: 100%;}.ExternalClass{width:100%;}.backgroundTable{margin:0 auto; padding:0; width:100%;}table td{border-collapse: collapse;}.ExternalClass *{line-height: 115%;}/* General styling */td{font-family: Arial;color: #6f6f6f;}body{-webkit-font-smoothing:antialiased;-webkit-text-size-adjust:none;width: 100%;height: 100%;color: #6f6f6f;font-weight: 400;font-size: 18px;}h1{margin: 10px 0;}a{color: #27aa90;text-decoration: none;}.force-full-width{width: 100% !important;}.force-width-80{width: 80% !important;}.body-padding{padding: 0 75px;}.mobile-align{text-align: right;}</style><style type="text/css" media="screen">@media screen{@import url(http://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600,900);/* Thanks Outlook 2013! */*{font-family: "Arial" !important;}.w280{width: 280px !important;}}</style><style type="text/css" media="only screen and (max-width: 480px)">/* Mobile styles */@media only screen and (max-width: 480px){table[class*="w320"]{width: 320px !important;}td[class*="w320"]{width: 280px !important;padding-left: 20px !important;padding-right: 20px !important;}img[class*="w320"]{width: 250px !important;height: 67px !important;}td[class*="mobile-spacing"]{padding-top: 10px !important;padding-bottom: 10px !important;}*[class*="mobile-hide"]{display: none !important;}*[class*="mobile-br"]{font-size: 12px !important;}td[class*="mobile-w20"]{width: 20px !important;}img[class*="mobile-w20"]{width: 20px !important;}td[class*="mobile-center"]{text-align: center !important;}table[class*="w100p"]{width: 100% !important;}td[class*="activate-now"]{padding-right: 0 !important;padding-top: 20px !important;}td[class*="mobile-block"]{display: block !important;}td[class*="mobile-align"]{text-align: left !important;}}</style></head><body offset="0" class="body" style="padding:0; margin:0; display:block; -webkit-text-size-adjust:none" bgcolor="#eeebeb"><table align="center" cellpadding="0" cellspacing="0" width="100%" height="100%" ><tr><td align="center" valign="top" width="100%"><center style="font-family: Arial;"><table cellspacing="0" cellpadding="0" width="600" class="w320"><tr><td align="center" valign="top"><table cellspacing="0" cellpadding="0" width="100%" style="background-color:#3bcdb0;"><tr><td style="background-color:#3bcdb0;"><table style="margin:0 auto;" cellspacing="0" cellpadding="0" width="100%"></table><table cellspacing="0" cellpadding="0" width="100%"><tr><td style="font-size:20px; font-weight: 600; color: #ffffff; text-align:center;" class="mobile-spacing"><div class="mobile-br">&nbsp;</div>Thank you for choosing Auragoa Spa Retreat Resort.<br></td></tr><tr><td style="font-size:16px; text-align:center; padding: 5px 75px; color: #6f6f6f;" class="w320 mobile-spacing">We are pleased to confirm your reservation as under:</td></tr></table><table cellspacing="0" cellpadding="0" width="100%"><tr><td><img src="http://demodevelopment.in/mail_img/s_design12.png" style="max-width:100%; display:block;"></td></tr></table><table class="mobile" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td class="icon54" align="center"><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="170"><tbody><tr><td class="icon34" valign="top" align="center" width="100%"><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="fullCenter" cellspacing="0" cellpadding="0" align="right" border="0" width="175"><tbody><tr><td height="25" width="100%"></td></tr><tr><td style="text-align: center; font-family:Arial; font-size: 18px; color: #ffffff; line-height: 18px; font-weight: 600;" class="fullCenter" valign="middle" width="100%">Booking id: '+bkid+'</td></tr><tr><td height="10" width="100%"></td></tr><tr><td style="text-align: center; font-family:Arial; font-size: 15px; color: #ffffff; line-height: 24px; font-weight: 600;" class="fullCenter" valign="middle" width="100%">Dear '+title+' '+fname+' '+lname+'</td></tr></tbody></table></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="60" width="100%"></td></tr></tbody></table></td></tr></tbody></table></td></tr></table><table cellspacing="0" cellpadding="0" width="100%" bgcolor="#ffffff" ><tr><td style="background-color:#ffffff;"><table style=" text-align: center; margin-top:48px;margin-bottom:48px; font-size: 13px;" cellspacing="0" cellpadding="0" border="0" width="100%"><tbody><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Name of Guest</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+title+' '+fname+' '+lname+'</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Date of Arrival</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+arrival+'</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Date of Departure</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+departure+'</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Accommodation</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+types+'</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Amount to be pay</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+amount+'/-(excluding of taxes)</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Check In</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+arrival+'</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="20%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Check Out</b></td><td width="20%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+departure+'</td><td width="20%"></td></tr></tbody></table><table style="margin:0 auto;" cellspacing="0" cellpadding="10" width="100%"><tr><td style="text-align:center; margin:0 auto;"><br><div><a href="http://"style="background-color:#f5774e;color:#ffffff;display:inline-block;font-family:Arial;font-size:18px;font-weight:400;line-height:45px;text-align:center;text-decoration:none;width:180px;-webkit-text-size-adjust:none;border-radius:20px;">Term & Conditions</a></div><br></td></tr></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td valign="top" bgcolor="#344b61" align="center" width="100%"><table class="mobile" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td align="center"><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="10" width="100%"></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="600"><tbody><tr><td align="center" width="100%"><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="fullCenter" cellspacing="0" cellpadding="0" align="left" border="0" width="140"><tbody><tr><td style="text-align: center;font-family: Helvetica, Arial, sans-serif;font-size: 12px;color: #ffffff;line-height: 15px;font-weight: 400;padding-left: 30px;" class="fullCenter" valign="middle" width="200px">Aura Goa Wellness Resort, Mandrem, North Goa<br>+91 76653-22222<br>info@auragoa.com<br><a href="http://auragoa.com/" style="text-decoration: none; color: #ffffff;">auragoa.com</a></td></tr></tbody></table><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="full" cellspacing="0" cellpadding="0" align="left" border="0" width="20"><tbody><tr><td height="1" width="100%"></td></tr></tbody></table><table style="text-align: right; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="buttonScale" cellspacing="0" cellpadding="0" align="right" border="0" width="96"><tbody><tr><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"><a href="https://twitter.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_1.png" alt="" class="hover" border="0" width="17"></a></td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://www.facebook.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_2.png" alt="" class="hover" border="0" width="17"></a></td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://plus.google.com/u/0/103796393489619851236" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_3.png" alt="" class="hover" border="0" width="17"></a></td></tr></tbody></table></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="10" width="100%"></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></table></td></tr></table></center></td></tr></table></body></html>'
			send_mail('Booking Confirmed', 'Someone Just Logined from your Account if that was not you then Contact to Admin. Logined at '+str(timezone.now())+' Time ', 'Auragoa <donotreply@auragoa.com>', [email], html_message=html_content, fail_silently=False)

		else:
			raise Exception('Permission Denied')

		
		return bundle

class BookingguestjsonResource(ModelResource):
	booking_gid = fields.ForeignKey(GuestResource, 'booking_gid', full=True)
	booking_rid = fields.ForeignKey(RoomResource, 'booking_rid', full=True)
	booking_sid = fields.ForeignKey(SourceResource, 'booking_sid', full=True, blank=True, null=True)
	class Meta:
		queryset = Booking.objects.all()
		resource_name = 'bookingguestjson'
		#allowed_methods = ['get', 'post', 'delete', 'put']
		filtering = {
			'booking_arrival': ALL,
			'booking_id': ALL,
			'booking_checkin': ALL,
			'booking_checkout': ALL
		}
		limit = 0
		always_return_data = True
		authentication = AdminApiKeyAuthentication()
		authorization = Authorization()
		serializer = urlencodeSerializer()

	def obj_create(self, bundle, request=None, **kwargs):
		username = bundle.request.GET['username']
		user = User.objects.get(username=username)
		if user.has_perm('booking.add_booking'):
		
			datetim = bundle.data.get('booking_arrival', '')
			hari = dateutil.parser.parse(datetim).date()
			ramm = datetime.datetime.combine(hari, datetime.time.min)
			arrive = str(ramm)		

			datetim1 = bundle.data.get('booking_departure', '')
			hari1 = dateutil.parser.parse(datetim1).date()
			ramm1 = datetime.datetime.combine(hari1, datetime.time.min)
			depart = str(ramm1)
			
			roome = bundle.data.get('booking_rid', '')
			a = roome.split('/')
			b = a[4]
			shyam = Booking.objects.filter(booking_rid__room_id = b).filter(booking_arrival__lte = depart).filter(booking_departure__gte = arrive)
			
			if shyam:			
				raise Exception('already booked')
			else:			
				bundle = super(BookingguestjsonResource, self).obj_create(bundle)
				bundle.obj.save()

			# booking_guest = bundle.data.get('booking_gid', '')
			# x = booking_guest.split('/')
			# y = x[4]
			# guest = Guest.objects.get(guest_id=y)
			email = bundle.obj.booking_gid.guest_email#guest.guest_email #"singhprabhanshu5@gmail.com"
			fname1 = bundle.obj.booking_gid.guest_fname
			lname1 = bundle.obj.booking_gid.guest_lname
			title1 = bundle.obj.booking_gid.guest_title
			fname = str(fname1)
			lname = str(lname1)
			title = str(title1)

			bookid = bundle.obj.booking_id
			bkid = str(bookid)
			arrival1 = str(datetim)
			departure1 = str(datetim1)
			dat_arrival = datetime.datetime.strptime(arrival1, '%Y-%m-%d %H:%M:%S').strftime('%d, %B %Y')
			dat_departure = datetime.datetime.strptime(departure1, '%Y-%m-%d %H:%M:%S').strftime('%d, %B %Y')
			arrival = str(dat_arrival)
			departure = str(dat_departure)
			booking_amount = bundle.obj.booking_amount
			amount = str(booking_amount)
			room_no = bundle.obj.booking_rid.room_number
			room_nos = str(room_no)
			room_type = bundle.obj.booking_rid.room_type_id.room_type_title
			types = str(room_type)

			html_content = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><title>welcome aura</title><style type="text/css">/* Take care of image borders and formatting */img{max-width: 600px;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;}a img{border: none;}table{border-collapse: collapse !important;}#outlook a{padding:0;}.ReadMsgBody{width: 100%;}.ExternalClass{width:100%;}.backgroundTable{margin:0 auto; padding:0; width:100%;}table td{border-collapse: collapse;}.ExternalClass *{line-height: 115%;}/* General styling */td{font-family: Arial;color: #6f6f6f;}body{-webkit-font-smoothing:antialiased;-webkit-text-size-adjust:none;width: 100%;height: 100%;color: #6f6f6f;font-weight: 400;font-size: 18px;}h1{margin: 10px 0;}a{color: #27aa90;text-decoration: none;}.force-full-width{width: 100% !important;}.force-width-80{width: 80% !important;}.body-padding{padding: 0 75px;}.mobile-align{text-align: right;}</style><style type="text/css" media="screen">@media screen{@import url(http://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600,900);/* Thanks Outlook 2013! */*{font-family: "Arial" !important;}.w280{width: 280px !important;}}</style><style type="text/css" media="only screen and (max-width: 480px)">/* Mobile styles */@media only screen and (max-width: 480px){table[class*="w320"]{width: 320px !important;}td[class*="w320"]{width: 280px !important;padding-left: 20px !important;padding-right: 20px !important;}img[class*="w320"]{width: 250px !important;height: 67px !important;}td[class*="mobile-spacing"]{padding-top: 10px !important;padding-bottom: 10px !important;}*[class*="mobile-hide"]{display: none !important;}*[class*="mobile-br"]{font-size: 12px !important;}td[class*="mobile-w20"]{width: 20px !important;}img[class*="mobile-w20"]{width: 20px !important;}td[class*="mobile-center"]{text-align: center !important;}table[class*="w100p"]{width: 100% !important;}td[class*="activate-now"]{padding-right: 0 !important;padding-top: 20px !important;}td[class*="mobile-block"]{display: block !important;}td[class*="mobile-align"]{text-align: left !important;}}</style></head><body offset="0" class="body" style="padding:0; margin:0; display:block; -webkit-text-size-adjust:none" bgcolor="#eeebeb"><table align="center" cellpadding="0" cellspacing="0" width="100%" height="100%" ><tr><td align="center" valign="top" width="100%"><center style="font-family: Arial;"><table cellspacing="0" cellpadding="0" width="600" class="w320"><tr><td align="center" valign="top"><table cellspacing="0" cellpadding="0" width="100%" style="background-color:#3bcdb0;"><tr><td style="background-color:#3bcdb0;"><table style="margin:0 auto;" cellspacing="0" cellpadding="0" width="100%"></table><table cellspacing="0" cellpadding="0" width="100%"><tr><td style="font-size:20px; font-weight: 600; color: #ffffff; text-align:center;" class="mobile-spacing"><div class="mobile-br">&nbsp;</div>Thank you for choosing Auragoa Spa Retreat Resort.<br></td></tr><tr><td style="font-size:16px; text-align:center; padding: 5px 75px; color: #6f6f6f;" class="w320 mobile-spacing">We are pleased to confirm your reservation as under:</td></tr></table><table cellspacing="0" cellpadding="0" width="100%"><tr><td><img src="http://demodevelopment.in/mail_img/s_design12.png" style="max-width:100%; display:block;"></td></tr></table><table class="mobile" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td class="icon54" align="center"><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="170"><tbody><tr><td class="icon34" valign="top" align="center" width="100%"><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="fullCenter" cellspacing="0" cellpadding="0" align="right" border="0" width="175"><tbody><tr><td height="25" width="100%"></td></tr><tr><td style="text-align: center; font-family:Arial; font-size: 18px; color: #ffffff; line-height: 18px; font-weight: 600;" class="fullCenter" valign="middle" width="100%">Booking id: '+bkid+'</td></tr><tr><td height="10" width="100%"></td></tr><tr><td style="text-align: center; font-family:Arial; font-size: 15px; color: #ffffff; line-height: 24px; font-weight: 600;" class="fullCenter" valign="middle" width="100%">Dear '+title+'. '+fname+' '+lname+'</td></tr></tbody></table></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="60" width="100%"></td></tr></tbody></table></td></tr></tbody></table></td></tr></table><table cellspacing="0" cellpadding="0" width="100%" bgcolor="#ffffff" ><tr><td style="background-color:#ffffff;"><table style=" text-align: center; margin-top:48px;margin-bottom:48px; font-size: 13px;" cellspacing="0" cellpadding="0" border="0" width="100%"><tbody><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Name of Guest</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+title+'. '+fname+' '+lname+'</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Date of Arrival</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+arrival+'</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Date of Departure</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+departure+'</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Accommodation</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+types+'</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Amount to be pay</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+amount+'/-(excluding of taxes)</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Check In</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+arrival+'</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="20%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Check Out</b></td><td width="20%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+departure+'</td><td width="20%"></td></tr></tbody></table><table style="margin:0 auto;" cellspacing="0" cellpadding="10" width="100%"><tr><td style="text-align:center; margin:0 auto;"><br><div><a href="http://"style="background-color:#f5774e;color:#ffffff;display:inline-block;font-family:Arial;font-size:18px;font-weight:400;line-height:45px;text-align:center;text-decoration:none;width:180px;-webkit-text-size-adjust:none;border-radius:20px;">Term & Conditions</a></div><br></td></tr></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td valign="top" bgcolor="#344b61" align="center" width="100%"><table class="mobile" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td align="center"><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="10" width="100%"></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="600"><tbody><tr><td align="center" width="100%"><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="fullCenter" cellspacing="0" cellpadding="0" align="left" border="0" width="140"><tbody><tr><td style="text-align: center;font-family: Helvetica, Arial, sans-serif;font-size: 12px;color: #ffffff;line-height: 15px;font-weight: 400;padding-left: 30px;" class="fullCenter" valign="middle" width="200px">Aura Goa Wellness Resort, Mandrem, North Goa<br>+91 76653-22222<br>info@auragoa.com<br><a href="http://auragoa.com/" style="text-decoration: none; color: #ffffff;">auragoa.com</a></td></tr></tbody></table><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="full" cellspacing="0" cellpadding="0" align="left" border="0" width="20"><tbody><tr><td height="1" width="100%"></td></tr></tbody></table><table style="text-align: right; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="buttonScale" cellspacing="0" cellpadding="0" align="right" border="0" width="96"><tbody><tr><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"><a href="https://twitter.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_1.png" alt="" class="hover" border="0" width="17"></a></td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://www.facebook.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_2.png" alt="" class="hover" border="0" width="17"></a></td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://plus.google.com/u/0/103796393489619851236" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_3.png" alt="" class="hover" border="0" width="17"></a></td></tr></tbody></table></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="10" width="100%"></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></table></td></tr></table></center></td></tr></table></body></html>'
			send_mail('Booking Confirmed', 'Someone Just Logined from your Account if that was not you then Contact to Admin. Logined at '+str(timezone.now())+' Time ', 'Auragoa <donotreply@auragoa.com>', [email], html_message=html_content, fail_silently=False)

		else:
			raise Exception('Permission Denied')

		
		return bundle


class Room_room_typeObject(object):
	def __init__(self, initial=None):
		self.__dict__['_data'] = {}
		if initial:
			self.update(initial)
	def __getattr__(self, name):
		return self._data.get(name, None)

	def __setattr__(self, name, value):
		self.__dict__['_data'][name] = value

	def update(self, other):
		for k in other:
			self.__setattr__(k, other[k])

	def to_dict(self):
		return self._data
 
class Room_room_typeResource(Resource):
	class Meta:
		resource_name = 'room_room_type'
		fields = ['value']
		allowed_methods = ['get']
		object_class = Room_room_typeObject
		serializers = urlencodeSerializer
		include_resource_uri = False

	def detail_uri_kwargs(self, bundle_or_obj ):
		kwargs = {}
		if isinstance(bundle_or_obj, Bundle):
			kwargs['value'] = bundle_or_obj.obj.value
		else:
			kwargs['value'] = bundle_or_obj.value
		return kwargs

	def get_obj_list(self, request):
		return [self.obj_get()]

	def obj_get_list(self, request=None, **kwargs):
		return [self.obj_get()]

	def obj_get(self, request=None, key=None, **kwargs):
		setting = Room_room_typeObject()
	
	def dehydrate(self, bundle):
		b_start = bundle.request.GET['b_s']
		b_end = bundle.request.GET['b_e']
		room = Room.objects.all()
		booking = Room.objects.filter(booking__booking_arrival__lte= b_end, booking__booking_departure__gte= b_start, booking__booking_status='Active')
		room_avail = room.exclude(room_id__in = booking)
		room_avail1 = room_avail.values_list('room_type_id__room_type_id', flat=True).distinct()
		room_avail1_count = len(room_avail1)
		#raise Exception(len(room_avail1))
		#room_type = Room_type.objects.all()
		ram = {}
		#shyam = {}
		h = 0
		for i in range(room_avail1_count):
			x = room_avail.filter(room_type_id__room_type_id=room_avail1[i])
			#ram[i.room_type_id.room_type_title] = room_avail.filter(room_type_id__room_type_id=i.room_type_id.room_type_id)
			shyam = {}
			g = 0

			for j in x:
				shyam[g] = {'room_id':j.room_id, 'room_uid':j.room_uid, 'room_type_id':j.room_type_id, 'room_sid':j.room_sid, 'room_number':j.room_number, 'room_title':j.room_title, 'room_slug':j.room_slug, 'room_condition':j.room_condition, 'room_amount':j.room_amount, 'room_type':j.room_type, 'room_image':j.room_image, 'room_history':j.room_history, 'room_status':j.room_status}
				g += 1

			#ram[i.room_type_id.room_type_title] = shyam
			#ram[] = shyam
			k = Room_type.objects.get(room_type_id=room_avail1[i])
			#raise Exception(k.room_type_id)
			ram[h] = {'room_type_id':k.room_type_id, 'room_type_title':k.room_type_title, 'room_type_slug':k.room_type_slug, 'room_type_facilities':k.room_type_facilities, 'room_type_price':k.room_type_price, 'room_type_image':k.room_type_image, 'room_type_number':k.room_type_number, 'room_type_status':k.room_title_status, 'rooms':shyam}
				
			h += 1
			
			bundle.data['Room_type'] = ram
			
		return bundle

#getting the booking detail having payment and folio without explicit need of id.
class Booking_full_detailResource(ModelResource):
	booking_gid = fields.ForeignKey(GuestResource, 'booking_gid', full=True)
	booking_rid = fields.ForeignKey(RoomResource, 'booking_rid', full=True)
	#folio_detail = fields.ForeignKey(FolioResource, 'folio', full=True)
	class Meta:
		queryset = Booking.objects.all()
		resource_name = 'booking_full_detail'
		#allowed_methods = ['get', 'post', 'delete', 'put']
		filtering = {
			'booking_arrival': ALL,
			'booking_id': ALL,
			'booking_checkin': ALL,
			'booking_checkout': ALL,
			'booking_status': ALL,
			'booking_timestamp': ALL,
		}
		limit = 0
		always_return_data = True
		authentication = AdminApiKeyAuthentication()
		authorization = Authorization()
		serializer = urlencodeSerializer()

	# def obj_get_list(self, bundle, **kwargs):
	# 	y = bundle.request.GET['id']
	# 	objects = Booking.objects.filter(booking_id=y)
	# 	return objects

	def dehydrate(self, bundle):
		#x = bundle.request.GET['id']
		field = Payment.objects.filter(payment_bid__booking_id=bundle.obj.booking_id)
		sield = Folio.objects.filter(folio_bid__booking_id=bundle.obj.booking_id)
		booking = Booking.objects.get(booking_id=bundle.obj.booking_id)
		p = booking.booking_total
		n = 0
		k = 0
		a=0
		b=0
		ram = {}
		shyam = {}
		for i in field:
			n = n + i.payment_total
			shyam[a] = {'payment_amount':i.payment_amount, 'payment_bid':i.payment_bid, 'payment_description':i.payment_description, 'payment_disc_res':i.payment_disc_res, 'payment_discount':i.payment_discount, 'payment_gid':i.payment_gid, 'payment_id':i.payment_id, 'payment_invoice':i.payment_invoice, 'payment_mode':i.payment_mode, 'payment_receipt':i.payment_receipt, 'payment_tax':i.payment_tax, 'payment_total':i.payment_total, 'payment_type':i.payment_type, 'payment_from':i.payment_from}
			bundle.data['payment'] = shyam
			a+=1
			
		for l in sield:
			k = k + l.folio_total
			ram[b] = {'folio_amount':l.folio_amount, 'folio_bid':l.folio_bid, 'folio_description':l.folio_description, 'folio_disc_res':l.folio_disc_res, 'folio_discount':l.folio_discount, 'folio_from':l.folio_from, 'folio_gid':l.folio_gid, 'folio_id':l.folio_id, 'folio_invoice':l.folio_invoice, 'folio_price':l.folio_price, 'folio_receipt':l.folio_receipt, 'folio_tax':l.folio_tax, 'folio_title':l.folio_title, 'folio_total':l.folio_total, 'folio_type':l.folio_type}
			bundle.data['folio'] = ram
			b+=1
			
		bundle.data['payment_due'] = k + p - n 
		bundle.data['payment_total'] = n
		bundle.data['folio_total'] = k		
		
		return bundle


'''
#BookingoldResource
class BookingResource(ModelResource):
	booking_gid = fields.ForeignKey(GuestResource, 'booking_gid', full=True)
	booking_rid = fields.ForeignKey(RoomResource, 'booking_rid', full=True)
	booking_sid = fields.ForeignKey(SourceResource, 'booking_sid', full=True, blank=True, null=True)
	class Meta:
		queryset = Booking.objects.all()
		resource_name = 'booking'
		#allowed_methods = ['get', 'post', 'delete', 'put']
		filtering = {
			'booking_arrival': ALL,
			'booking_id': ALL,
			'booking_checkin': ALL,
			'booking_checkout': ALL,
			'booking_status': ALL,
			'booking_timestamp': ALL,
			
		}
		limit = 0
		always_return_data = True
		authentication = AdminApiKeyAuthentication()
		authorization = Authorization()
		serializer = urlencodeSerializer()

	def alter_list_data_to_serialize(self, request, data):
		total_amount = 0.0
		for i in data[ 'objects' ]:
			total_amount += i.data[ 'booking_total' ]

		return { 'meta' : data[ 'meta' ], 'objects' : data[ 'objects' ], 'total_amount' : total_amount }

	def obj_create(self, bundle, request=None, **kwargs):
		username = bundle.request.GET['username']
		user = User.objects.get(username=username)
		if user.has_perm('booking.add_booking'):
		
			datetim = bundle.data.get('booking_arrival', '')
			hari = dateutil.parser.parse(datetim).date()
			ramm = datetime.datetime.combine(hari, datetime.time.min)
			arrive = str(ramm)		

			datetim1 = bundle.data.get('booking_departure', '')
			hari1 = dateutil.parser.parse(datetim1).date()
			ramm1 = datetime.datetime.combine(hari1, datetime.time.min)
			depart = str(ramm1)

			#checking for departure not less than or equal to arrival date
			if datetim1 <= datetim:
				raise Exception("Give the appropriate date for the departure")
			
			roome = bundle.data.get('booking_rid', '')
			a = roome.split('/')
			b = a[4]
			shyam = Booking.objects.filter(booking_rid__room_id = b).filter(booking_arrival__lte = depart).filter(booking_departure__gte = arrive).filter(booking_status='Active')
			
			if shyam:			
				raise Exception('already booked')
			else:			
				bundle = super(BookingResource, self).obj_create(bundle)
				bundle.obj.save()

			booking_guest = bundle.data.get('booking_gid', '')
			x = booking_guest.split('/')
			y = x[4]
			guest = Guest.objects.get(guest_id=y)
			email = guest.guest_email #"singhprabhanshu5@gmail.com"
			fname1 = bundle.obj.booking_gid.guest_fname
			lname1 = bundle.obj.booking_gid.guest_lname
			title1 = bundle.obj.booking_gid.guest_title
			fname = str(fname1)
			lname = str(lname1)
			title = str(title1)

			bookid = bundle.obj.booking_id
			bkid = str(bookid)
			arrival1 = str(datetim)
			departure1 = str(datetim1)
			dat_arrival = datetime.datetime.strptime(arrival1, '%Y-%m-%d %H:%M:%S').strftime('%d, %B %Y')
			dat_departure = datetime.datetime.strptime(departure1, '%Y-%m-%d %H:%M:%S').strftime('%d, %B %Y')
			arrival = str(dat_arrival)
			departure = str(dat_departure)
			booking_amount = bundle.obj.booking_total
			amount = str(booking_amount)
			room_no = bundle.obj.booking_rid.room_number
			room_nos = str(room_no)
			room_type = bundle.obj.booking_rid.room_type_id.room_type_title
			types = str(room_type)

			html_content = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><title>welcome aura</title><style type="text/css">/* Take care of image borders and formatting */img{max-width: 600px;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;}a img{border: none;}table{border-collapse: collapse !important;}#outlook a{padding:0;}.ReadMsgBody{width: 100%;}.ExternalClass{width:100%;}.backgroundTable{margin:0 auto; padding:0; width:100%;}table td{border-collapse: collapse;}.ExternalClass *{line-height: 115%;}/* General styling */td{font-family: Arial;color: #6f6f6f;}body{-webkit-font-smoothing:antialiased;-webkit-text-size-adjust:none;width: 100%;height: 100%;color: #6f6f6f;font-weight: 400;font-size: 18px;}h1{margin: 10px 0;}a{color: #27aa90;text-decoration: none;}.force-full-width{width: 100% !important;}.force-width-80{width: 80% !important;}.body-padding{padding: 0 75px;}.mobile-align{text-align: right;}</style><style type="text/css" media="screen">@media screen{@import url(http://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600,900);/* Thanks Outlook 2013! */*{font-family: "Arial" !important;}.w280{width: 280px !important;}}</style><style type="text/css" media="only screen and (max-width: 480px)">/* Mobile styles */@media only screen and (max-width: 480px){table[class*="w320"]{width: 320px !important;}td[class*="w320"]{width: 280px !important;padding-left: 20px !important;padding-right: 20px !important;}img[class*="w320"]{width: 250px !important;height: 67px !important;}td[class*="mobile-spacing"]{padding-top: 10px !important;padding-bottom: 10px !important;}*[class*="mobile-hide"]{display: none !important;}*[class*="mobile-br"]{font-size: 12px !important;}td[class*="mobile-w20"]{width: 20px !important;}img[class*="mobile-w20"]{width: 20px !important;}td[class*="mobile-center"]{text-align: center !important;}table[class*="w100p"]{width: 100% !important;}td[class*="activate-now"]{padding-right: 0 !important;padding-top: 20px !important;}td[class*="mobile-block"]{display: block !important;}td[class*="mobile-align"]{text-align: left !important;}}</style></head><body offset="0" class="body" style="padding:0; margin:0; display:block; -webkit-text-size-adjust:none" bgcolor="#eeebeb"><table align="center" cellpadding="0" cellspacing="0" width="100%" height="100%" ><tr><td align="center" valign="top" width="100%"><center style="font-family: Arial;"><table cellspacing="0" cellpadding="0" width="600" class="w320"><tr><td align="center" valign="top"><table cellspacing="0" cellpadding="0" width="100%" style="background-color:#3bcdb0;"><tr><td style="background-color:#3bcdb0;"><table style="margin:0 auto;" cellspacing="0" cellpadding="0" width="100%"></table><table cellspacing="0" cellpadding="0" width="100%"><tr><td style="font-size:20px; font-weight: 600; color: #ffffff; text-align:center;" class="mobile-spacing"><div class="mobile-br">&nbsp;</div>Thank you for choosing Auragoa Spa Retreat Resort.<br></td></tr><tr><td style="font-size:16px; text-align:center; padding: 5px 75px; color: #6f6f6f;" class="w320 mobile-spacing">We are pleased to confirm your reservation as under:</td></tr></table><table cellspacing="0" cellpadding="0" width="100%"><tr><td><img src="http://demodevelopment.in/mail_img/s_design12.png" style="max-width:100%; display:block;"></td></tr></table><table class="mobile" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td class="icon54" align="center"><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="170"><tbody><tr><td class="icon34" valign="top" align="center" width="100%"><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="fullCenter" cellspacing="0" cellpadding="0" align="right" border="0" width="175"><tbody><tr><td height="25" width="100%"></td></tr><tr><td style="text-align: center; font-family:Arial; font-size: 18px; color: #ffffff; line-height: 18px; font-weight: 600;" class="fullCenter" valign="middle" width="100%">Booking id: '+bkid+'</td></tr><tr><td height="10" width="100%"></td></tr><tr><td style="text-align: center; font-family:Arial; font-size: 15px; color: #ffffff; line-height: 24px; font-weight: 600;" class="fullCenter" valign="middle" width="100%">Dear '+title+' '+fname+' '+lname+'</td></tr></tbody></table></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="60" width="100%"></td></tr></tbody></table></td></tr></tbody></table></td></tr></table><table cellspacing="0" cellpadding="0" width="100%" bgcolor="#ffffff" ><tr><td style="background-color:#ffffff;"><table style=" text-align: center; margin-top:48px;margin-bottom:48px; font-size: 13px;" cellspacing="0" cellpadding="0" border="0" width="100%"><tbody><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Name of Guest</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+title+' '+fname+' '+lname+'</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Date of Arrival</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+arrival+'</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Date of Departure</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+departure+'</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Accommodation</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+types+'</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Amount to be pay</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+amount+'/-(inclusive all taxes)</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Check In</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+arrival+'</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="20%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Check Out</b></td><td width="20%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+departure+'</td><td width="20%"></td></tr></tbody></table><table style="margin:0 auto;" cellspacing="0" cellpadding="10" width="100%"><tr><td style="text-align:center; margin:0 auto;"><br><div><a href="http://auragoa.com/"style="background-color:#f5774e;color:#ffffff;display:inline-block;font-family:Arial;font-size:18px;font-weight:400;line-height:45px;text-align:center;text-decoration:none;width:180px;-webkit-text-size-adjust:none;border-radius:20px;">Term & Conditions</a></div><br></td></tr></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td valign="top" bgcolor="#344b61" align="center" width="100%"><table class="mobile" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td align="center"><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="10" width="100%"></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="600"><tbody><tr><td align="center" width="100%"><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="fullCenter" cellspacing="0" cellpadding="0" align="left" border="0" width="140"><tbody><tr><td style="text-align: center;font-family: Helvetica, Arial, sans-serif;font-size: 12px;color: #ffffff;line-height: 15px;font-weight: 400;padding-left: 30px;" class="fullCenter" valign="middle" width="200px">Aura Goa Wellness Resort, Mandrem, North Goa<br>+91 76653-22222<br>info@auragoa.com<br><a href="http://auragoa.com/" style="text-decoration: none; color: #ffffff;">auragoa.com</a></td></tr></tbody></table><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="full" cellspacing="0" cellpadding="0" align="left" border="0" width="20"><tbody><tr><td height="1" width="100%"></td></tr></tbody></table><table style="text-align: right; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="buttonScale" cellspacing="0" cellpadding="0" align="right" border="0" width="96"><tbody><tr><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"><a href="https://twitter.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_1.png" alt="" class="hover" border="0" width="17"></a></td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://www.facebook.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_2.png" alt="" class="hover" border="0" width="17"></a></td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://plus.google.com/u/0/103796393489619851236" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_3.png" alt="" class="hover" border="0" width="17"></a></td></tr></tbody></table></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="10" width="100%"></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></table></td></tr></table></center></td></tr></table></body></html>'
			send_mail('Booking Confirmed', 'Someone Just Logined from your Account if that was not you then Contact to Admin. Logined at '+str(timezone.now())+' Time ', 'Auragoa <info@bookmywp.com>', [email], html_message=html_content, fail_silently=False)

		else:
			raise Exception('Permission Denied')

		
		return bundle

	def obj_update(self, bundle, request=None, **kwargs):
		username = bundle.request.GET['username']
		user = User.objects.get(username=username)


		if user.has_perm('booking.change_booking'):
			ram = bundle.data.get('booking_checkout')
			cancel = bundle.data.get('booking_status')
			#if self.booking_checkout.null:
			if not ram:
				if not cancel:
					bundle = super(BookingResource, self).obj_update(bundle, request=None, **kwargs)
				else:
					bundle = super(BookingResource, self).obj_update(bundle, request=None, **kwargs)
					email3 = bundle.obj.booking_gid.guest_email
					fname3 = str(bundle.obj.booking_gid.guest_fname)
					lname3 = str(bundle.obj.booking_gid.guest_lname)
					html_content2 = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head> <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/> <meta name="viewport" content="width=device-width, initial-scale=1"/> <title>feedback aura</title> <style type="text/css"> /* Take care of image borders and formatting */ img{max-width: 600px; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic;}a img{border: none;}table{border-collapse: collapse !important;}#outlook a{padding:0;}.ReadMsgBody{width: 100%;}.ExternalClass{width:100%;}.backgroundTable{margin:0 auto; padding:0; width:100%;}table td{border-collapse: collapse;}.ExternalClass *{line-height: 115%;}/* General styling */ td{font-family: Arial, sans-serif; color: #6f6f6f;}body{-webkit-font-smoothing:antialiased; -webkit-text-size-adjust:none; width: 100%; height: 100%; color: #6f6f6f; font-weight: 400; font-size: 18px;}h1{margin: 10px 0;}a{color: #27aa90; text-decoration: none;}.force-full-width{width: 100% !important;}.force-width-80{width: 80% !important;}.body-padding{padding: 0 75px;}.mobile-align{text-align: right;}</style> <style type="text/css" media="screen"> @media screen{@import url(http://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600,900); /* Thanks Outlook 2013! */ *{font-family: "Source Sans Pro", "Helvetica Neue", "Arial", "sans-serif" !important;}.w280{width: 280px !important;}}</style> <style type="text/css" media="only screen and (max-width: 480px)"> /* Mobile styles */ @media only screen and (max-width: 480px){table[class*="w320"]{width: 320px !important;}td[class*="w320"]{width: 280px !important; padding-left: 20px !important; padding-right: 20px !important;}img[class*="w320"]{width: 250px !important; height: 67px !important;}td[class*="mobile-spacing"]{padding-top: 10px !important; padding-bottom: 10px !important;}*[class*="mobile-hide"]{display: none !important;}*[class*="mobile-br"]{font-size: 12px !important;}td[class*="mobile-w20"]{width: 20px !important;}img[class*="mobile-w20"]{width: 20px !important;}td[class*="mobile-center"]{text-align: center !important;}table[class*="w100p"]{width: 100% !important;}td[class*="activate-now"]{padding-right: 0 !important; padding-top: 20px !important;}td[class*="mobile-block"]{display: block !important;}td[class*="mobile-align"]{text-align: left !important;}}</style></head><body offset="0" class="body" style="padding:0; margin:0; display:block; -webkit-text-size-adjust:none" bgcolor="#eeebeb"> <table align="center" cellpadding="0" cellspacing="0" width="100%" height="100%" > <tr> <td align="center" valign="top" width="100%"> <center style="font-family: Calibri, Verdana, Ariel, sans-serif;"> <table cellspacing="0" cellpadding="0" width="600" class="w320"> <tr> <td align="center" valign="top"> <table cellspacing="0" cellpadding="0" width="100%" style="background-color:#3bcdb0;"> <tr> <td style="background-color:#3bcdb0;"> <table style="margin:0 auto;" cellspacing="0" cellpadding="0" width="100%"> </table> <table cellspacing="0" cellpadding="0" width="100%"> <tr> <td> <img src="http://demodevelopment.in/mail_img/s_design12.png" style="max-width:100%; display:block;"> </td></tr></table> </td></tr></table> <table cellspacing="0" cellpadding="0" width="100%" bgcolor="#ffffff" > <tr> <td style="background-color:#ffffff;padding: 0px 30px !important;"> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="600"> <tbody> <tr> <td align="center" width="100%"> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"> <tbody> <tr> <td height="60" width="100%"></td></tr></tbody> </table> <table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="fullCenter" cellspacing="0" cellpadding="0" align="center" border="0" width="600"> <tbody> <tr> <td style="text-align: center; font-family: Helvetica, Arial, sans-serif, "Open Sans"; font-size: 20px; color: #444444; line-height: 32px; font-weight: 700;" class="fullCenter" valign="middle" width="100%"> Dear '+fname3+' '+lname3+' </td></tr><tr> <td height="30" width="100%"></td></tr><tr> <td width="100%"> <table cellspacing="0" cellpadding="0" align="center" border="0" width="100"> <tbody> <tr> <td style="font-size: 1px; line-height: 1px;" bgcolor="#808080" height="1" width="100">&nbsp;</td></tr></tbody> </table> </td></tr><tr> <td height="30" width="100%"></td></tr><tr> <td style="text-align: left; font-family: Helvetica, Arial, sans-serif, "Open Sans"; font-size: 14px; color: #808080; line-height: 22px; font-weight: 400;" class="fullCenter" valign="middle" width="100%"> Thank you for choosing <strong>Auragoa</strong> for your recent stay in Goa. We have read your comments about the hotel and we greatly appreciate that you took the time to write them, as guests satisfaction is our priority. </td></tr><tr> <td height="25" width="100%"></td></tr><tr> <td style="text-align: left; font-family: Helvetica, Arial, sans-serif, "Open Sans"; font-size: 14px; color: #808080; line-height: 22px; font-weight: 400;" class="fullCenter" valign="middle" width="100%"> We invite you, to share your opinion, using the following rattings: </td></tr><tr> <td height="25" width="100%"></td></tr><tr> <table style="margin: 0 auto;" class="force-width-80" cellspacing="0" cellpadding="0"> <tbody><tr> <td class="pusher">&nbsp;</td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_03_0.gif" alt="0"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_03.gif" alt="1"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_04.gif" alt="2"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_05.gif" alt="3"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_06.gif" alt="4"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_07.gif" alt="5"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_08.gif" alt="6"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_09.gif" alt="8"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_10.gif" alt="9"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_11.gif" alt="10"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_12.gif" alt="10"> </a> </td><td class="pusher">&nbsp;</td></tr></tbody></table> </tr><tr> <td height="25" width="100%"></td></tr><tr> <td style="text-align: left; font-family: Helvetica, Arial, sans-serif, "Open Sans"; font-size: 14px; color: #808080; line-height: 22px; font-weight: 400;" class="fullCenter" valign="middle" width="100%"> It is very important for us that guests experiences are shared. </td></tr><tr> <td height="25" width="100%"></td></tr><tr> <td style="text-align: left; font-family: Helvetica, Arial, sans-serif, "Open Sans"; font-size: 14px; color: #808080; line-height: 22px; font-weight: 400;" class="fullCenter" valign="middle" width="100%"> It was a pleasure to have you as our guest. We would like to take this opportunity to thank you for your collaboration and we hope to see you again soon at <strong>Auragoa</strong>. </td></tr><tr> <td height="25" width="100%"></td></tr><tr> <td style="text-align: left; font-family: Helvetica, Arial, sans-serif, "Open Sans"; font-size: 14px; color: #808080; line-height: 22px; font-weight: 400;" class="fullCenter" valign="middle" width="100%"> <strong>Management</strong>,<br><strong>Aura Goa Wellness Resort</strong><br></td></tr></tbody> </table> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"> <tbody> <tr> <td height="60" width="100%"></td></tr></tbody> </table> </td></tr></tbody> </table> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"> <tbody> <tr> <td valign="top" bgcolor="#344b61" align="center" width="100%"> <table class="mobile" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"> <tbody> <tr> <td align="center"> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"> <tbody> <tr> <td height="10" width="100%"></td></tr></tbody> </table> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="600"> <tbody> <tr> <td align="center" width="100%"> <table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="fullCenter" cellspacing="0" cellpadding="0" align="left" border="0" width="140"> <tbody> <tr> <td style="text-align: center;font-family: Helvetica, Arial, sans-serif;font-size: 12px;color: #ffffff;line-height: 15px;font-weight: 400;padding-left: 30px;" class="fullCenter" valign="middle" width="200px"> Aura Goa Wellness Resort, Mandrem, North Goa <br>+91 76653-22222<br>info@auragoa.com<br><a href="http://auragoa.com/" style="text-decoration: none; color: #ffffff;"> auragoa.com</a> </td></tr></tbody> </table> <table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="full" cellspacing="0" cellpadding="0" align="left" border="0" width="20"> <tbody> <tr> <td height="1" width="100%"></td></tr></tbody> </table> <table style="text-align: right; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="buttonScale" cellspacing="0" cellpadding="0" align="right" border="0" width="96"> <tbody> <tr> <td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://twitter.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_1.png" alt="" class="hover" border="0" width="17"></a> </td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://www.facebook.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_2.png" alt="" class="hover" border="0" width="17"></a> </td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://plus.google.com/u/0/103796393489619851236" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_3.png" alt="" class="hover" border="0" width="17"></a> </td></tr></tbody> </table> </td></tr></tbody> </table> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"> <tbody> <tr> <td height="10" width="100%"></td></tr></tbody> </table> </td></tr></tbody> </table> </td></tr></tbody> </table> </td></tr></table> </td></tr></table> </center> </td></tr></table> </body> </html>'
					send_mail('Cancel_Feedback Report', 'Someone Just Logined from your Account if that was not you then Contact to Admin. Logined at '+str(timezone.now())+' Time ', 'Auragoa <info@bookmywp.com>', [email3], html_message = html_content2, fail_silently=False)
					
			else:
				
				x = kwargs['pk']
				field = Payment.objects.filter(payment_bid__booking_id=x)
				sield = Folio.objects.filter(folio_bid__booking_id=x)
				booking = Booking.objects.get(booking_id=x)
				p = booking.booking_total
				n = 0
				k = 0
				for i in field:
					n = n + i.payment_total
				for l in sield:
					k = k + l.folio_total
				bundle.data['payment_due'] = k + p - n
				bundle.data['payment_total'] = n
				bundle.data['folio_total'] = k
				bundle.data['booking_checkout'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
				due = k + p - n
				demo = str(due)
				#if due>0:
				if due > 10 or due < -10:
					raise Exception('your payment_due is: Rs.'+ demo)
				else:
					bundle = super(BookingResource, self).obj_update(bundle, request=None, **kwargs)
					room = str(bundle.obj.booking_rid.room_number)
					bkid = str(bundle.obj.booking_id)
					gid = str(bundle.obj.booking_gid.guest_id)
					arriv_dat = bundle.obj.booking_checkin

					#format1 = "%Y-%m-%d %H:%M:%S"
					#now_utc = bundle.obj.booking_checkin
					#raise Exception(now_utc)
					arriv_dat_timezone = arriv_dat.astimezone(pytz.timezone('Asia/Kolkata'))
					#raise Exception(now_asia.strftime(format))
					#raise Exception(now_asia.strftime("%Y-%m-%d %H:%M:%S"))
					arriv_dat_timezone_format = str(arriv_dat_timezone.strftime("%Y-%m-%d %H:%M:%S"))


					arrival_time = arriv_dat_timezone_format[11:19]
					#raise Exception(arriv_dat_slice)
					depart_dat = bundle.obj.booking_checkout
					depart_dat_timezone = depart_dat.astimezone(pytz.timezone('Asia/Kolkata'))
					depart_dat_timezone_format = str(depart_dat_timezone.strftime("%Y-%m-%d %H:%M:%S"))
					departure_time = depart_dat_timezone_format[11:19]
					#raise Exception(depart_dat)
					arrival_date = str(dateutil.parser.parse(str(arriv_dat)).date())
					departure_date = str(dateutil.parser.parse(str(depart_dat)).date())
					# at = datetime.datetime.strptime(arriv_dat, "%Y-%m-%d %H:%M:%S")
					# dt = datetime.datetime.strptime(depart_dat, "%Y-%m-%d %H:%M:%S")
					# arrival_time = str(at.time().strftime('%H:%M:%S'))
					# departure_time = str(dt.time().strftime('%H:%M:%S'))
					fname = str(bundle.obj.booking_gid.guest_fname)
					lname = str(bundle.obj.booking_gid.guest_lname)
					room_type = str(bundle.obj.booking_rid.room_type_id.room_type_title)
					room_tarrif = bundle.obj.booking_amount
					luxury_tax = bundle.obj.booking_luxury_tax
					service_tax = bundle.obj.booking_service_tax
					discount = bundle.obj.booking_discount
					pay_frm_restaurant = Payment.objects.filter(payment_from="Restaurant").filter(payment_bid__booking_id=bundle.obj.booking_id)
					pay_frm_spa = Payment.objects.filter(payment_from="Spa").filter(payment_bid__booking_id=bundle.obj.booking_id)
					#raise Exception(pay_frm_spa)
					total_restaurant = 0
					total_spa = 0
					if pay_frm_restaurant:
						for g in pay_frm_restaurant:
							total_restaurant += g.payment_total
					if pay_frm_spa:
						for h in pay_frm_spa:
							total_spa += h.payment_total

					#raise Exception(total_spa)
					a = room_tarrif + luxury_tax
					b = a + service_tax
					c = b - discount
					d = c + total_restaurant
					e = d + total_spa


					email = bundle.obj.booking_gid.guest_email
					html_content1 = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head> <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/> <meta name="viewport" content="width=device-width, initial-scale=1"/> <title>feedback aura</title> <style type="text/css"> /* Take care of image borders and formatting */ img{max-width: 600px; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic;}a img{border: none;}table{border-collapse: collapse !important;}#outlook a{padding:0;}.ReadMsgBody{width: 100%;}.ExternalClass{width:100%;}.backgroundTable{margin:0 auto; padding:0; width:100%;}table td{border-collapse: collapse;}.ExternalClass *{line-height: 115%;}/* General styling */ td{font-family: Arial, sans-serif; color: #6f6f6f;}body{-webkit-font-smoothing:antialiased; -webkit-text-size-adjust:none; width: 100%; height: 100%; color: #6f6f6f; font-weight: 400; font-size: 18px;}h1{margin: 10px 0;}a{color: #27aa90; text-decoration: none;}.force-full-width{width: 100% !important;}.force-width-80{width: 80% !important;}.body-padding{padding: 0 75px;}.mobile-align{text-align: right;}</style> <style type="text/css" media="screen"> @media screen{@import url(http://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600,900); /* Thanks Outlook 2013! */ *{font-family: "Source Sans Pro", "Helvetica Neue", "Arial", "sans-serif" !important;}.w280{width: 280px !important;}}</style> <style type="text/css" media="only screen and (max-width: 480px)"> /* Mobile styles */ @media only screen and (max-width: 480px){table[class*="w320"]{width: 320px !important;}td[class*="w320"]{width: 280px !important; padding-left: 20px !important; padding-right: 20px !important;}img[class*="w320"]{width: 250px !important; height: 67px !important;}td[class*="mobile-spacing"]{padding-top: 10px !important; padding-bottom: 10px !important;}*[class*="mobile-hide"]{display: none !important;}*[class*="mobile-br"]{font-size: 12px !important;}td[class*="mobile-w20"]{width: 20px !important;}img[class*="mobile-w20"]{width: 20px !important;}td[class*="mobile-center"]{text-align: center !important;}table[class*="w100p"]{width: 100% !important;}td[class*="activate-now"]{padding-right: 0 !important; padding-top: 20px !important;}td[class*="mobile-block"]{display: block !important;}td[class*="mobile-align"]{text-align: left !important;}}</style></head><body offset="0" class="body" style="padding:0; margin:0; display:block; -webkit-text-size-adjust:none" bgcolor="#eeebeb"> <table align="center" cellpadding="0" cellspacing="0" width="100%" height="100%" > <tr> <td align="center" valign="top" width="100%"> <center style="font-family: Calibri, Verdana, Ariel, sans-serif;"> <table cellspacing="0" cellpadding="0" width="600" class="w320"> <tr> <td align="center" valign="top"> <table cellspacing="0" cellpadding="0" width="100%" style="background-color:#3bcdb0;"> <tr> <td style="background-color:#3bcdb0;"> <table style="margin:0 auto;" cellspacing="0" cellpadding="0" width="100%"> </table> <table cellspacing="0" cellpadding="0" width="100%"> <tr> <td> <img src="http://demodevelopment.in/mail_img/s_design12.png" style="max-width:100%; display:block;"> </td></tr></table> </td></tr></table> <table cellspacing="0" cellpadding="0" width="100%" bgcolor="#ffffff" > <tr> <td style="background-color:#ffffff;padding: 0px 30px !important;"> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="600"> <tbody> <tr> <td align="center" width="100%"> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"> <tbody> <tr> <td height="60" width="100%"></td></tr></tbody> </table> <table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="fullCenter" cellspacing="0" cellpadding="0" align="center" border="0" width="600"> <tbody> <tr> <td style="text-align: center; font-family: Helvetica, Arial, sans-serif, "Open Sans"; font-size: 20px; color: #444444; line-height: 32px; font-weight: 700;" class="fullCenter" valign="middle" width="100%"> Dear '+fname+' '+lname+' </td></tr><tr> <td height="30" width="100%"></td></tr><tr> <td width="100%"> <table cellspacing="0" cellpadding="0" align="center" border="0" width="100"> <tbody> <tr> <td style="font-size: 1px; line-height: 1px;" bgcolor="#808080" height="1" width="100">&nbsp;</td></tr></tbody> </table> </td></tr><tr> <td height="30" width="100%"></td></tr><tr> <td style="text-align: left; font-family: Helvetica, Arial, sans-serif, "Open Sans"; font-size: 14px; color: #808080; line-height: 22px; font-weight: 400;" class="fullCenter" valign="middle" width="100%"> Thank you for choosing <strong>Auragoa</strong> for your recent stay in Goa. We have read your comments about the hotel and we greatly appreciate that you took the time to write them, as guests satisfaction is our priority. </td></tr><tr> <td height="25" width="100%"></td></tr><tr> <td style="text-align: left; font-family: Helvetica, Arial, sans-serif, "Open Sans"; font-size: 14px; color: #808080; line-height: 22px; font-weight: 400;" class="fullCenter" valign="middle" width="100%"> We invite you, to share your opinion, using the following rattings: </td></tr><tr> <td height="25" width="100%"></td></tr><tr> <table style="margin: 0 auto;" class="force-width-80" cellspacing="0" cellpadding="0"> <tbody><tr> <td class="pusher">&nbsp;</td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_03_0.gif" alt="0"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_03.gif" alt="1"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_04.gif" alt="2"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_05.gif" alt="3"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_06.gif" alt="4"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_07.gif" alt="5"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_08.gif" alt="6"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_09.gif" alt="8"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_10.gif" alt="9"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_11.gif" alt="10"> </a> </td><td> <a href=""> <img class="step" src="http://demodevelopment.in/mail_img/sunday_12.gif" alt="10"> </a> </td><td class="pusher">&nbsp;</td></tr></tbody></table> </tr><tr> <td height="25" width="100%"></td></tr><tr> <td style="text-align: left; font-family: Helvetica, Arial, sans-serif, "Open Sans"; font-size: 14px; color: #808080; line-height: 22px; font-weight: 400;" class="fullCenter" valign="middle" width="100%"> It is very important for us that guests experiences are shared. </td></tr><tr> <td height="25" width="100%"></td></tr><tr> <td style="text-align: left; font-family: Helvetica, Arial, sans-serif, "Open Sans"; font-size: 14px; color: #808080; line-height: 22px; font-weight: 400;" class="fullCenter" valign="middle" width="100%"> It was a pleasure to have you as our guest. We would like to take this opportunity to thank you for your collaboration and we hope to see you again soon at <strong>Auragoa</strong>. </td></tr><tr> <td height="25" width="100%"></td></tr><tr> <td style="text-align: left; font-family: Helvetica, Arial, sans-serif, "Open Sans"; font-size: 14px; color: #808080; line-height: 22px; font-weight: 400;" class="fullCenter" valign="middle" width="100%"> <strong>Management</strong>,<br><strong>Aura Goa Wellness Resort</strong><br></td></tr></tbody> </table> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"> <tbody> <tr> <td height="60" width="100%"></td></tr></tbody> </table> </td></tr></tbody> </table> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"> <tbody> <tr> <td valign="top" bgcolor="#344b61" align="center" width="100%"> <table class="mobile" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"> <tbody> <tr> <td align="center"> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"> <tbody> <tr> <td height="10" width="100%"></td></tr></tbody> </table> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="600"> <tbody> <tr> <td align="center" width="100%"> <table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="fullCenter" cellspacing="0" cellpadding="0" align="left" border="0" width="140"> <tbody> <tr> <td style="text-align: center;font-family: Helvetica, Arial, sans-serif;font-size: 12px;color: #ffffff;line-height: 15px;font-weight: 400;padding-left: 30px;" class="fullCenter" valign="middle" width="200px"> Aura Goa Wellness Resort, Mandrem, North Goa <br>+91 76653-22222<br>info@auragoa.com<br><a href="http://auragoa.com/" style="text-decoration: none; color: #ffffff;"> auragoa.com</a> </td></tr></tbody> </table> <table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="full" cellspacing="0" cellpadding="0" align="left" border="0" width="20"> <tbody> <tr> <td height="1" width="100%"></td></tr></tbody> </table> <table style="text-align: right; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="buttonScale" cellspacing="0" cellpadding="0" align="right" border="0" width="96"> <tbody> <tr> <td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://twitter.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_1.png" alt="" class="hover" border="0" width="17"></a> </td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://www.facebook.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_2.png" alt="" class="hover" border="0" width="17"></a> </td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://plus.google.com/u/0/103796393489619851236" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_3.png" alt="" class="hover" border="0" width="17"></a> </td></tr></tbody> </table> </td></tr></tbody> </table> <table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"> <tbody> <tr> <td height="10" width="100%"></td></tr></tbody> </table> </td></tr></tbody> </table> </td></tr></tbody> </table> </td></tr></table> </td></tr></table> </center> </td></tr></table> </body> </html>'
					##html_content = '<!DOCTYPE html><html xmlns=http://www.w3.org/1999/xhtml><meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"><head><meta content="text/html; charset=UTF-8" http-equiv="Content-Type"><meta content="width=device-width,initial-scale=1" name="viewport"><title>Payment</title><head><style>img{max-width:600px;outline:0;text-decoration:none;-ms-interpolation-mode:bicubic}a img{border:none}table{border-collapse:collapse!important}#outlook a{padding:0}.ReadMsgBody{width:100%}.ExternalClass{width:100%}.backgroundTable{margin:0 auto;padding:0;width:100%!important}table td{border-collapse:collapse}.ExternalClass *{line-height:115%}.container-for-gmail-android{min-width:600px}*{font-family:Helvetica,Arial,sans-serif}body{-webkit-font-smoothing:antialiased;-webkit-text-size-adjust:none;width:100%!important;margin:0!important;height:100%;color:#676767}td{font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#777;text-align:center;line-height:21px}a{color:#676767;text-decoration:none!important}.pull-left{text-align:left}.pull-right{text-align:right}.header-lg,.header-md,.header-sm{font-size:32px;font-weight:700;line-height:normal;padding:35px 0 0;color:#4d4d4d}.header-md{font-size:24px}.header-sm{padding:5px 0;font-size:18px;line-height:1.3}.content-padding{padding:20px 0 5px}.mobile-header-padding-right{width:290px;text-align:right;padding-left:10px}.mobile-header-padding-left{width:290px;text-align:left;padding-left:10px}.free-text{width:100%!important;padding:10px 60px 0}.button{padding:30px 0}.mini-block{border:1px solid #e5e5e5;border-radius:5px;background-color:#fff;padding:12px 15px 15px;text-align:left;width:253px}.mini-container-left{width:278px;padding:10px 0 10px 15px}.mini-container-right{width:278px;padding:10px 14px 10px 15px}.product{text-align:left;vertical-align:top;width:175px}.total-space{padding-bottom:8px;display:inline-block}.item-table{padding:50px 20px;width:560px}.item{width:300px}.mobile-hide-img{text-align:left;width:125px}.mobile-hide-img img{border:1px solid #e6e6e6;border-radius:4px}.title-dark{border-bottom:1px solid #ccc;color:#4d4d4d;font-weight:700;padding-bottom:5px}.item-col{padding-top:20px;vertical-align:top}.force-width-gmail{min-width:600px;height:0!important;line-height:1px!important;font-size:1px!important}</style><style media=screen>@import url(http://fonts.googleapis.com/css?family=Oxygen:400,700);</style><style media=screen>@media screen{*{font-family:Oxygen,"Helvetica Neue",Arial,sans-serif!important}}</style><style media="only screen and (max-width:480px)">@media only screen and (max-width:480px){table[class*=container-for-gmail-android]{min-width:290px!important;width:100%!important}img[class=force-width-gmail]{display:none!important;width:0!important;height:0!important}table[class=w320]{width:320px!important}td[class*=mobile-header-padding-left]{width:160px!important;padding-left:0!important}td[class*=mobile-header-padding-right]{width:160px!important;padding-right:0!important}td[class=header-lg]{font-size:24px!important;padding-bottom:5px!important}td[class=content-padding]{padding:5px 0 5px!important}td[class=button]{padding:5px 5px 30px!important}td[class*=free-text]{padding:10px 18px 30px!important}td[class~=mobile-hide-img]{display:none!important;height:0!important;width:0!important;line-height:0!important}td[class~=item]{width:140px!important;vertical-align:top!important}td[class~=quantity]{width:50px!important}td[class~=price]{width:90px!important}td[class=item-table]{padding:30px 20px!important}td[class=mini-container-left],td[class=mini-container-right]{padding:0 15px 15px!important;display:block!important;width:290px!important}}</style></head><body bgcolor=#f7f7f7><table cellpadding=0 cellspacing=0 width=100% class=container-for-gmail-android align=center><tr><td class=content-padding width=100% style="background-color:#3BCDB0" valign=top align=center><center><table cellpadding=0 cellspacing=0 width=600 class=w320><tr><td class=w320><table cellpadding=0 cellspacing=0 width=100%><tr><td class=mini-container-left><table cellpadding=0 cellspacing=0 width=100%><tr><td class=mini-block-padding><table cellpadding=0 cellspacing=0 width=100% style="border-collapse:separate!important"><tr><td><img src=http://auragoa.com/wp-content/uploads/2017/01/aura-goa-logofinal.png></table></table><td class=mini-container-right><table cellpadding=0 cellspacing=0 width=100%><tr><td class=mini-block-padding><table cellpadding=0 cellspacing=0 width=100% style=border-collapse:separate!important><tr><td class="item-col quantity" style="text-align:center"><span class=total-space style="font-weight:700;color:#4d4d4d">Aura Goa Wellness Resort </span><span style="color:#4d4d4d" class=total-space>near R D khalp school,</span><br><span style="color:#4d4d4d" class=total-space>Mandrem,</span><br><span style="color:#4d4d4d" class=total-space>North Goa.</span><br></table></table></table><tr><td class=w320><table cellpadding=0 cellspacing=0 width=100%><tr><td class=mini-container-left><table cellpadding=0 cellspacing=0 width=100%><tr><td class=mini-block-padding><table cellpadding=0 cellspacing=0 width=100% style="border-collapse:separate!important"><tr><td class=mini-block><b>Room #</b> '+room+'<br><b>Checkin Date :</b> '+arrival_date+'<br><b>Checkout Date :</b> '+departure_date+'<br><b>Room Type :</b> '+room_type+'<br></table></table><td class=mini-container-right><table cellpadding=0 cellspacing=0 width=100%><tr><td class=mini-block-padding><table cellpadding=0 cellspacing=0 width=100% style="border-collapse:separate!important"><tr><td class=mini-block><b>Invoice #</b> '+gid+''+bkid+'<br><b>Arr. Time : </b>'+arrival_time+'<br><b>Dep. Time :</b> '+departure_time+'<br><b>Page #</b> 1</table></table></table></table></center><tr><td width=100% style="background-color:#fff;border-top:1px solid #e5e5e5;border-bottom:1px solid #e5e5e5"valign=top align=center><center><table cellpadding=0 cellspacing=0 width=600 class=w320><tr><td class=item-table><table cellpadding=0 cellspacing=0 width=100%><tr><td class=title-dark width=100>Date<td class=title-dark width=100>Description<td class=title-dark width=100>Document<td class=title-dark width=100>Debited<td class=title-dark width=100>Credited<td class=title-dark width=100>Balance<tr><td class="item-col item"><table cellpadding=0 cellspacing=0 width=100%><tr><td class=product>'+arrival_date+'</table><td class=item-col>Room Tariff<td class=item-col>1234<td class=item-col>'+str(room_tarrif)+'<td class=item-col><td class=item-col>'+str(room_tarrif)+'<tr><td class="item-col item"><table cellpadding=0 cellspacing=0 width=100%><tr><td class=product>'+arrival_date+'</table><td class=item-col>Luxury Tax<td class=item-col>1234<td class=item-col>'+str(luxury_tax)+'<td class=item-col><td class=item-col>'+str(a)+'<tr><td class="item-col item"><table cellpadding=0 cellspacing=0 width=100%><tr><td class=product>'+arrival_date+'</table><td class=item-col>Service Tax<td class=item-col>1234<td class=item-col>'+str(service_tax)+'<td class=item-col><td class=item-col>'+str(b)+'<tr><td class="item-col item"><table cellpadding=0 cellspacing=0 width=100%><tr><td class=product>'+arrival_date+'</table><td class=item-col>Discount<td class=item-col>Discount<td class=item-col><td class=item-col>'+str(discount)+'<td class=item-col>'+str(c)+'<tr><td class="item-col item"><table cellpadding=0 cellspacing=0 width=100%><tr><td class=product>05/04/2017</table><td class=item-col>In House Guest<br> F & B<td class=item-col>1234<td class=item-col>'+str(total_restaurant)+'<td class=item-col><td class=item-col>'+str(d)+'<tr><td class="item-col item"><table cellpadding=0 cellspacing=0 width=100%><tr><td class=product>05/04/2017</table><td class=item-col>In House Guest<br> F & B<td class=item-col>1234<td class=item-col>'+str(total_spa)+'<td class=item-col><td class=item-col>'+str(e)+'<tr><td class="item-col item mobile-row-padding"><td class="item-col quantity"><td class="item-col price"><tr><td class="item-col item"><td class="item-col item"><td class="item-col item"><td class="item-col item"><td class="item-col quantity" style="text-align:right;padding-right:10px;border-top:1px solid #ccc"><span class=total-space>Discount</span><br><span class=total-space>Tax</span><br><span class=total-space style="font-weight:700;color:#4d4d4d">Total</span><td class="item-col price" style="text-align:left;border-top:1px solid #ccc"><span class=total-space>4000</span><br><span class=total-space>4000</span><br><span class=total-space style="font-weight:700;color:#4d4d4d">4000</span></table></table></center><tr><td style="background-color:#344B61;height:100px;padding:20px" valign="top" width="100%" align="center"><center><table cellpadding="0" cellspacing="0" width="600" class="w320"><tbody><tr><td class="fullCenter" style="text-align:center;font-family:Helvetica,Arial,sans-serif;font-size:12px;color:white;line-height:15px;font-weight:400;padding-left:30px;line-height:2" valign="middle" width="200px">Aura Goa Wellness Resort, Mandrem, North Goa <br>+91 76653-22222 <br> <a style="text-decoration:none;color:white">info@auragoa.com </a> <br> <a href="http://auragoa.com/" style="text-decoration:none;color:white">auragoa.com </a></td><td class="mobile-header-padding-right pull-right"> <a href="https://twitter.com/aurasparetreat"> <img src="http://s3.amazonaws.com/swu-filepicker/k8D8A7SLRuetZspHxsJk_social_08.gif" alt="twitter" height="47" width="44"> </a> <a href="https://www.facebook.com/aurasparetreat"> <img src="http://s3.amazonaws.com/swu-filepicker/LMPMj7JSRoCWypAvzaN3_social_09.gif" alt="facebook" height="47" width="38"> </a></td></tr></tbody></table></center></td></tr></table></body></html>'
					html_content = '<!DOCTYPE html><html xmlns=http://www.w3.org/1999/xhtml><meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"><head><meta content="text/html; charset=UTF-8" http-equiv="Content-Type"><meta content="width=device-width,initial-scale=1" name="viewport"><title>Payment</title><head><style>img{max-width:600px;outline:0;text-decoration:none;-ms-interpolation-mode:bicubic}a img{border:none}table{border-collapse:collapse!important}#outlook a{padding:0}.ReadMsgBody{width:100%}.ExternalClass{width:100%}.backgroundTable{margin:0 auto;padding:0;width:100%!important}table td{border-collapse:collapse}.ExternalClass *{line-height:115%}.container-for-gmail-android{min-width:600px}*{font-family:Helvetica,Arial,sans-serif}body{-webkit-font-smoothing:antialiased;-webkit-text-size-adjust:none;width:100%!important;margin:0!important;height:100%;color:#676767}td{font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#777;text-align:center;line-height:21px}a{color:#676767;text-decoration:none!important}.pull-left{text-align:left}.pull-right{text-align:right}.header-lg,.header-md,.header-sm{font-size:32px;font-weight:700;line-height:normal;padding:35px 0 0;color:#4d4d4d}.header-md{font-size:24px}.header-sm{padding:5px 0;font-size:18px;line-height:1.3}.content-padding{padding:20px 0 5px}.mobile-header-padding-right{width:290px;text-align:right;padding-left:10px}.mobile-header-padding-left{width:290px;text-align:left;padding-left:10px}.free-text{width:100%!important;padding:10px 60px 0}.button{padding:30px 0}.mini-block{border:1px solid #e5e5e5;border-radius:5px;background-color:#fff;padding:12px 15px 15px;text-align:left;width:253px}.mini-container-left{width:278px;padding:10px 0 10px 15px}.mini-container-right{width:278px;padding:10px 14px 10px 15px}.product{text-align:left;vertical-align:top;width:175px}.total-space{padding-bottom:8px;display:inline-block}.item-table{padding:50px 20px;width:560px}.item{width:300px}.mobile-hide-img{text-align:left;width:125px}.mobile-hide-img img{border:1px solid #e6e6e6;border-radius:4px}.title-dark{border-bottom:1px solid #ccc;color:#4d4d4d;font-weight:700;padding-bottom:5px}.item-col{padding-top:20px;vertical-align:top}.force-width-gmail{min-width:600px;height:0!important;line-height:1px!important;font-size:1px!important}</style><style media=screen>@import url(http://fonts.googleapis.com/css?family=Oxygen:400,700);</style><style media=screen>@media screen{*{font-family:Oxygen,"Helvetica Neue",Arial,sans-serif!important}}</style><style media="only screen and (max-width:480px)">@media only screen and (max-width:480px){table[class*=container-for-gmail-android]{min-width:290px!important;width:100%!important}img[class=force-width-gmail]{display:none!important;width:0!important;height:0!important}table[class=w320]{width:320px!important}td[class*=mobile-header-padding-left]{width:160px!important;padding-left:0!important}td[class*=mobile-header-padding-right]{width:160px!important;padding-right:0!important}td[class=header-lg]{font-size:24px!important;padding-bottom:5px!important}td[class=content-padding]{padding:5px 0 5px!important}td[class=button]{padding:5px 5px 30px!important}td[class*=free-text]{padding:10px 18px 30px!important}td[class~=mobile-hide-img]{display:none!important;height:0!important;width:0!important;line-height:0!important}td[class~=item]{width:140px!important;vertical-align:top!important}td[class~=quantity]{width:50px!important}td[class~=price]{width:90px!important}td[class=item-table]{padding:30px 20px!important}td[class=mini-container-left],td[class=mini-container-right]{padding:0 15px 15px!important;display:block!important;width:290px!important}}</style></head><body bgcolor=#f7f7f7><table cellpadding=0 cellspacing=0 width=100% class=container-for-gmail-android align=center><tr><td class=content-padding width=100% style="background-color:#3BCDB0" valign=top align=center><center><table cellpadding=0 cellspacing=0 width=600 class=w320><tr><td class=w320><table cellpadding=0 cellspacing=0 width=100%><tr><td class=mini-container-left><table cellpadding=0 cellspacing=0 width=100%><tr><td class=mini-block-padding><table cellpadding=0 cellspacing=0 width=100% style="border-collapse:separate!important"><tr><td><img src=http://auragoa.com/wp-content/uploads/2017/01/aura-goa-logofinal.png></table></table><td class=mini-container-right><table cellpadding=0 cellspacing=0 width=100%><tr><td class=mini-block-padding><table cellpadding=0 cellspacing=0 width=100% style=border-collapse:separate!important><tr><td class="item-col quantity" style="text-align:center"><span class=total-space style="font-weight:700;color:#4d4d4d">Aura Goa Wellness Resort </span><span style="color:#4d4d4d" class=total-space>near R D khalp school,</span><br><span style="color:#4d4d4d" class=total-space>Mandrem,</span><br><span style="color:#4d4d4d" class=total-space>North Goa.</span><br></table></table></table><tr><td class=w320><table cellpadding=0 cellspacing=0 width=100%><tr><td class=mini-container-left><table cellpadding=0 cellspacing=0 width=100%><tr><td class=mini-block-padding><table cellpadding=0 cellspacing=0 width=100% style="border-collapse:separate!important"><tr><td class=mini-block><b>Guest:</b> '+fname+' '+lname+'<br><b>Room Type :</b> '+room_type+'<br><b>checkin Date :</b> '+arrival_date+'<br><b>Checkout Date :</b> '+departure_date+'<br></table></table><td class=mini-container-right><table cellpadding=0 cellspacing=0 width=100%><tr><td class=mini-block-padding><table cellpadding=0 cellspacing=0 width=100% style="border-collapse:separate!important"><tr><td class=mini-block><b>Invoice #</b> '+gid+''+bkid+'<br><b>Room # : </b>'+room+'<br><b>Checkin Time :</b> '+arrival_time+'<br><b>Checkout Time</b> '+departure_time+'</table></table></table></table></center><tr><td width=100% style="background-color:#fff;border-top:1px solid #e5e5e5;border-bottom:1px solid #e5e5e5"valign=top align=center><center><table cellpadding=0 cellspacing=0 width=600 class=w320><tr><td class=item-table><table cellpadding=0 cellspacing=0 width=100%><tr><td class=title-dark width=100>Date<td class=title-dark width=100>Description<td class=title-dark width=100>Debited<td class=title-dark width=100>Credited<td class=title-dark width=100>Balance<tr><td class="item-col item"><table cellpadding=0 cellspacing=0 width=100%><tr><td class=product>'+arrival_date+'</table><td class=item-col>Room Tariff<td class=item-col>'+str(room_tarrif)+'<td class=item-col><td class=item-col>'+str(room_tarrif)+'<tr><td class="item-col item"><table cellpadding=0 cellspacing=0 width=100%><tr><td class=product>'+arrival_date+'</table><td class=item-col>Luxury Tax<td class=item-col>'+str(luxury_tax)+'<td class=item-col><td class=item-col>'+str(a)+'<tr><td class="item-col item"><table cellpadding=0 cellspacing=0 width=100%><tr><td class=product>'+arrival_date+'</table><td class=item-col>Service Tax<td class=item-col>'+str(service_tax)+'<td class=item-col><td class=item-col>'+str(b)+'<tr><td class="item-col item"><table cellpadding=0 cellspacing=0 width=100%><tr><td class=product>'+arrival_date+'</table><td class=item-col>Discount<td class=item-col><td class=item-col>'+str(discount)+'<td class=item-col>'+str(c)+'<tr><td colspan="2" class=item-col>In House Guest F & B<td class=item-col>'+str(total_restaurant)+'<td class=item-col><td class=item-col>'+str(d)+'<tr><td colspan="2" class=item-col>Payment From Spa<td class=item-col>'+str(total_spa)+'<td class=item-col><td class=item-col>'+str(e)+'<tr><td class="item-col item mobile-row-padding"><td class="item-col quantity"><td class="item-col price"><tr><td class="item-col item"><td class="item-col item"><td class="item-col item"><td class="item-col quantity" style="text-align:right;padding-right:10px;border-top:1px solid #ccc"><span class=total-space style="font-weight:700;color:#4d4d4d">Total</span><td class="item-col price" style="border-top:1px solid #ccc"><span class=total-space>'+str(e)+'</span></table></table></center><tr><td style="background-color:#344B61;height:100px;padding:20px" valign="top" width="100%" align="center"><center><table cellpadding="0" cellspacing="0" width="600" class="w320"><tbody><tr><td class="fullCenter" style="text-align:center;font-family:Helvetica,Arial,sans-serif;font-size:12px;color:white;line-height:15px;font-weight:400;padding-left:30px;line-height:2" valign="middle" width="200px">Aura Goa Wellness Resort, Mandrem, North Goa <br>+91 76653-22222 <br> <a style="text-decoration:none;color:white">info@auragoa.com </a> <br> <a href="http://auragoa.com/" style="text-decoration:none;color:white">auragoa.com </a></td><td class="mobile-header-padding-right pull-right"> <a href="https://twitter.com/aurasparetreat"> <img src="http://s3.amazonaws.com/swu-filepicker/k8D8A7SLRuetZspHxsJk_social_08.gif" alt="twitter" height="47" width="44"> </a> <a href="https://www.facebook.com/aurasparetreat"> <img src="http://s3.amazonaws.com/swu-filepicker/LMPMj7JSRoCWypAvzaN3_social_09.gif" alt="facebook" height="47" width="38"> </a></td></tr></tbody></table></center></td></tr></table></body></html>'
					send_mail('Auragoa Invoice', 'Someone Just Logined from your Account if that was not you then Contact to Admin. Logined at '+str(timezone.now())+' Time ', 'Auragoa <info@bookmywp.com>', [email], html_message = html_content, fail_silently=False)
					send_mail('Feedback Report', 'Someone Just Logined from your Account if that was not you then Contact to Admin. Logined at '+str(timezone.now())+' Time ', 'Auragoa <info@bookmywp.com>', [email], html_message = html_content1, fail_silently=False)
		else:
			raise Exception('Permission Denied')
		
		return bundle

	def hydrate(self, bundle):
		request = get_current_request()
		emp = bundle.request.GET['username']
		emp1 = User.objects.get(username = emp)
		t = int(emp1.id)
		checkin = bundle.data.get('booking_checkin')
		

		 
		if request.method == 'POST':
			bundle.data['booking_track'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['booking_utrack'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['booking_referal_url'] = bundle.request.META['HTTP_REFERER']
			bundle.data['booking_ueid'] = t
			amount = bundle.data.get('booking_amount')
			disc = bundle.data.get('booking_discount')
			amount = int(amount)
			if disc:
				discount = disc
			else:
				discount = 0

			x = amount - int(discount)
			# service tax
			tax1 = (x * (float(9)/100)) 
			# luxury tax
			if amount >= 3000 and amount < 5000:
				tax2 = (amount * (float(9)/100))
			else:
				tax2 = (amount * (float(12)/100))

			bundle.data['booking_service_tax'] = tax1
			bundle.data['booking_luxury_tax'] = tax2
			bundle.data['booking_tax'] = tax1 + tax2
			bundle.data['booking_total'] = tax1 + tax2 + x
			if checkin:
				bundle.data['booking_checkin'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


		elif request.method == 'PUT':
			# emp = bundle.request.GET['username']
			# emp1 = User.objects.get(username = emp)
			# t = int(emp1.id)
			bundle.data['booking_utrack'] = request.META['REMOTE_ADDR'] #+ ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['booking_utimestamp'] = timezone.now()
			bundle.data['booking_ueid'] = t
			if checkin:
				bundle.data['booking_checkin'] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

		return bundle

	# showing guest preference in booking from gother_preferences	
	def dehydrate(self, bundle):
		gid = bundle.obj.booking_gid.guest_id
		tbid = bundle.obj.booking_id
		preferences = gother.objects.filter(gother_gid__guest_id=gid)
		travel = Travel.objects.filter(travel_bid=tbid)
		if preferences:
			for i in preferences:
				bundle.data['booking_guest_preferences'] = i.gother_preferences

		if travel:
			for i in travel:
				bundle.data['booking_travel_detail'] = {'travel_id':i.travel_id, 'travel_bid':i.travel_bid, 'travel_amode':i.travel_amode, 'travel_atitle':i.travel_atitle, 'travel_atime':i.travel_atime, 'travel_atask':i.travel_atask, 'travel_dmode':i.travel_dmode, 'travel_dtitle':i.travel_dtitle, 'travel_dtime':i.travel_dtime, 'travel_dtask':i.travel_dtask, 'travel_timestamp':i.travel_timestamp, 'travel_utimestamp':i.travel_utimestamp, 'travel_ueid':i.travel_ueid, 'travel_track':i.travel_track, 'travel_utrack':i.travel_utrack, 'travel_status':i.travel_status}
		return bundle

'''


