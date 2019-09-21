# -*- coding: utf-8 -*-
from tastypie.authorization import Authorization
from tastypie import fields
from tastypie.fields import ForeignKey
from django.db import models
from django.contrib.auth.models import User
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from .models import Guest, gwork, gother
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication, MultiAuthentication
from jakhar.api import urlencodeSerializer, AdminApiKeyAuthentication, UserResource
from tastypie.authorization import DjangoAuthorization, ReadOnlyAuthorization
from booking.models import Booking
from Room.models import Room
from django.core.mail import send_mail
from django.utils import timezone
import datetime
import dateutil.parser
from dateutil.parser import parse
from crum import get_current_request
from country.api import CountryResource, StateResource

from email_cronjob.models import Email_cron

class GuestResource(ModelResource):
	guest_uid = fields.ForeignKey(UserResource, 'guest_uid', full=True)
	guest_country = fields.ForeignKey(CountryResource, 'guest_country', full=True, blank=True, null=True)
	guest_state = fields.ForeignKey(StateResource, 'guest_state', full=True, blank=True, null=True)
	class Meta:
		queryset = Guest.objects.all()
		resource_name = 'guest'
		#allowed_methods = ['get', 'post', 'delete', 'put','patch']

		limit = 0
		always_return_data = True
		#authentication = AdminApiKeyAuthentication()
		#authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
		#authorization = DjangoAuthorization()
		authentication = AdminApiKeyAuthentication()
		authorization = Authorization()
		serializer = urlencodeSerializer()
		filtering = {
			'guest_id' : ALL,
			'guest_fname' : ALL, 
			'guest_lname' : ALL,
			'guest_email' : ALL,
			'guest_mobile' : ALL,
			'guest_nationality' : ALL,
			'guest_address' : ALL,
			'guest_country' : ALL_WITH_RELATIONS,
			'guest_state' : ALL_WITH_RELATIONS,
			'guest_city' : ALL,
			'guest_type' : ALL
		}

	def obj_create(self, bundle, request=None, **kwargs):
		username = bundle.request.GET['username']
		user = User.objects.get(username=username)
		email1 = bundle.data.get('guest_email', '')
		name = bundle.data.get('guest_fname', '')

		if user.has_perm('Guest.add_guest'):  #permission checking during post
			bundle = super(GuestResource, self).obj_create(bundle)
			bundle.obj.save()
			email = email1
			#html_content = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><title>payment aura</title><style type="text/css">/* Take care of image borders and formatting */img{max-width: 600px;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;}a img{border: none;}table{border-collapse: collapse !important;}#outlook a{padding:0;}.ReadMsgBody{width: 100%;}.ExternalClass{width:100%;}.backgroundTable{margin:0 auto; padding:0; width:100%;}table td{border-collapse: collapse;}.ExternalClass *{line-height: 115%;}/* General styling */td{font-family: Arial, sans-serif;color: #6f6f6f;}body{-webkit-font-smoothing:antialiased;-webkit-text-size-adjust:none;width: 100%;height: 100%;color: #6f6f6f;font-weight: 400;font-size: 18px;}h1{margin: 10px 0;}a{color: #27aa90;text-decoration: none;}.force-full-width{width: 100% !important;}.force-width-80{width: 80% !important;}.body-padding{padding: 0 75px;}.mobile-align{text-align: right;}</style><style type="text/css" media="screen">@media screen{@import url(http://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600,900);/* Thanks Outlook 2013! */*{font-family: "Source Sans Pro", "Helvetica Neue", "Arial", "sans-serif" !important;}.w280{width: 280px !important;}}</style><style type="text/css" media="only screen and (max-width: 480px)">/* Mobile styles */@media only screen and (max-width: 480px){table[class*="w320"]{width: 320px !important;}td[class*="w320"]{width: 280px !important;padding-left: 20px !important;padding-right: 20px !important;}img[class*="w320"]{width: 250px !important;height: 67px !important;}td[class*="mobile-spacing"]{padding-top: 10px !important;padding-bottom: 10px !important;}*[class*="mobile-hide"]{display: none !important;}*[class*="mobile-br"]{font-size: 12px !important;}td[class*="mobile-w20"]{width: 20px !important;}img[class*="mobile-w20"]{width: 20px !important;}td[class*="mobile-center"]{text-align: center !important;}table[class*="w100p"]{width: 100% !important;}td[class*="activate-now"]{padding-right: 0 !important;padding-top: 20px !important;}td[class*="mobile-block"]{display: block !important;}td[class*="mobile-align"]{text-align: left !important;}}</style></head><body offset="0" class="body" style="padding:0; margin:0; display:block; -webkit-text-size-adjust:none" bgcolor="#eeebeb"><table align="center" cellpadding="0" cellspacing="0" width="100%" height="100%" ><tr><td align="center" valign="top" width="100%"><center style="font-family: Calibri, Verdana, Ariel, sans-serif;"><table cellspacing="0" cellpadding="0" width="600" class="w320"><tr><td align="center" valign="top"><table cellspacing="0" cellpadding="0" width="100%" style="background-color:#3bcdb0;"><tr><td style="background-color:#3bcdb0;"><table style="margin:0 auto;" cellspacing="0" cellpadding="0" width="100%"></table><table cellspacing="0" cellpadding="0" width="100%"><tr><td style="font-size:20px; font-weight: 600; color: #ffffff; text-align:center;" class="mobile-spacing"><div class="mobile-br">&nbsp;</div>Thank you for choosing Auragoa Spa Retreat Resort.<br></td></tr><tr><td style="font-size:16px; text-align:center; padding: 5px 75px; color: #6f6f6f;" class="w320 mobile-spacing">We are pleased to confirm your Payment as under:</td></tr></table><table cellspacing="0" cellpadding="0" width="100%"><tr><td><img src="http://demodevelopment.in/mail_img/s_design12.png" style="max-width:100%; display:block;"></td></tr></table></td></tr></table><table cellspacing="0" cellpadding="0" width="100%" bgcolor="#ffffff" ><tr><td style="background-color:#ffffff;"><table style=" text-align: center; margin-top:48px;margin-bottom:48px; font-size: 13px;" cellspacing="0" cellpadding="0" border="0" width="100%"><tbody><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Transaction ID</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">123456789</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Booking No.</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">0123456789</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Date of Arrival</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">9th September, 2014</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Date of Departure</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">9th September, 2014</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Accommodation</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">Deluxe Suite</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Amount to be pay</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">Rs.4000/-(excluding of taxes)</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Check In</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">9:00 am, 9th September, 2014</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="20%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Check Out</b></td><td width="20%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">9:00 am, 9th September, 2014</td><td width="20%"></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td valign="top" bgcolor="#344b61" align="center" width="100%"><table class="mobile" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td align="center"><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="10" width="100%"></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="600"><tbody><tr><td align="center" width="100%"><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="fullCenter" cellspacing="0" cellpadding="0" align="left" border="0" width="140"><tbody><tr><td style="text-align: center; font-family: Helvetica, Arial, sans-serif; font-size: 12px; color: #ffffff; line-height: 15px; font-weight: 400;padding-left: 30px;" class="fullCenter" valign="middle" width="100%">Aura Goa Wellness Resort, Mandrem, North Goa<br>+91 76653-22222<br>info@auragoa.com<br><a href="http://auragoa.com/" style="text-decoration: none; color: #ffffff;">auragoa.com</a></td></tr></tbody></table><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="full" cellspacing="0" cellpadding="0" align="left" border="0" width="20"><tbody><tr><td height="1" width="100%"></td></tr></tbody></table><table style="text-align: right; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="buttonScale" cellspacing="0" cellpadding="0" align="right" border="0" width="96"><tbody><tr><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"><a href="https://twitter.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_1.png" alt="" class="hover" border="0" width="17"></a></td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://www.facebook.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_2.png" alt="" class="hover" border="0" width="17"></a></td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://plus.google.com/u/0/103796393489619851236" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_3.png" alt="" class="hover" border="0" width="17"></a></td></tr></tbody></table></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="10" width="100%"></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></table></td></tr></table></center></td></tr></table></body></html>'
			html_content = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><title>booking aura</title><style type="text/css">/* Take care of image borders and formatting */img{max-width: 600px;outline: none;text-decoration: none;-ms-interpolation-mode:bicubic;}a img{border: none;}table{border-collapse: collapse !important;}#outlook a{padding:0;}.ReadMsgBody{width: 100%;}.ExternalClass{width:100%;}.backgroundTable{margin:0 auto; padding:0; width:100%;}table td{border-collapse: collapse;}.ExternalClass *{line-height: 115%;}/* General styling */td{font-family: Arial, sans-serif;color: #6f6f6f;}body{-webkit-font-smoothing:antialiased;-webkit-text-size-adjust:none;width: 100%;height: 100%;color: #6f6f6f;font-weight: 400;font-size: 18px;}h1{margin: 10px 0;}a{color: #27aa90;text-decoration: none;}.force-full-width{width: 100% !important;}.force-width-80{width: 80% !important;}.body-padding{padding: 0 75px;}.mobile-align{text-align: right;}</style><style type="text/css" media="screen">@media screen{@import url(http://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600,900);/* Thanks Outlook 2013! */*{font-family: "Source Sans Pro", "Helvetica Neue", "Arial", "sans-serif" !important;}.w280{width: 280px !important;}}</style><style type="text/css" media="only screen and (max-width: 480px)">/* Mobile styles */@media only screen and (max-width: 480px){table[class*="w320"]{width: 320px !important;}td[class*="w320"]{width: 280px !important;padding-left: 20px !important;padding-right: 20px !important;}img[class*="w320"]{width: 250px !important;height: 67px !important;}td[class*="mobile-spacing"]{padding-top: 10px !important;padding-bottom: 10px !important;}*[class*="mobile-hide"]{display: none !important;}*[class*="mobile-br"]{font-size: 12px !important;}td[class*="mobile-w20"]{width: 20px !important;}img[class*="mobile-w20"]{width: 20px !important;}td[class*="mobile-center"]{text-align: center!important;}table[class*="w100p"]{width: 100% !important;}td[class*="activate-now"]{padding-right: 0 !important;padding-top: 20px !important;}td[class*="mobile-block"]{display: block !important;}td[class*="mobile-align"]{text-align: left !important;}}</style></head><body offset="0" class="body" style="padding:0; margin:0; display:block; -webkit-text-size-adjust:none" bgcolor="#eeebeb"><table align="center" cellpadding="0" cellspacing="0" width="100%" height="100%" ><tr><td align="center" valign="top" width="100%"><center style="font-family: Calibri, Verdana, Ariel, sans-serif;"><table cellspacing="0" cellpadding="0" width="600" class="w320"><tr><td align="center" valign="top"><table cellspacing="0" cellpadding="0" width="100%" style="background-color:#3bcdb0;"><tr><td style="background-color:#3bcdb0;"><table style="margin:0 auto;" cellspacing="0" cellpadding="0" width="100%"></table><table cellspacing="0" cellpadding="0" width="100%"><tr><td><img src="http://demodevelopment.in/mail_img/s_design12.png" style="max-width:100%; display:block;"></td></tr></table></td></tr></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td valign="top" align="center" width="100%"><table class="mobile" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td align="center" style="background-color:#ffffff;"><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="60" width="100%"></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="600"><tbody><tr><td align="center" width="100%"><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="fullCenter" cellspacing="0" cellpadding="0" align="center" border="0" width="600"><tbody><tr><td style="text-align: center; font-size: 20px; color: #444444; line-height: 32px; font-weight: 700;" class="fullCenter" valign="middle" width="100%">Hi '+name+',</td></tr><tr><td height="30" width="100%"></td></tr><tr><td width="100%"><table cellspacing="0" cellpadding="0" align="center" border="0" width="100"><tbody><tr><td style="font-size: 1px; line-height: 1px;" bgcolor="#808080" height="1" width="100">&nbsp;</td></tr></tbody></table></td></tr><tr><td height="30" width="100%"></td></tr><tr><td style="text-align: center; font-size: 14px; color: #808080; line-height: 22px; font-weight: 400;" class="fullCenter" valign="middle" width="100%">Are you still looking to book a room at our hotel. We hope to serve you better at our hotel. Please click on our website link below to book.</td></tr><tr><td height="25" width="100%"></td></tr><tr><td style="text-align: center; font-size: 14px; color: #808080; line-height: 22px; font-weight: 400;" class="fullCenter" valign="middle" width="100%">Booking cancelled after 60 days of confirmation one day retention will be charged for all the rooms confirmed.</td></tr><tr><td height="25" width="100%"></td></tr><tr><td style="text-align: center; font-size: 14px; color: #808080; line-height: 22px; font-weight: 400;" class="fullCenter" valign="middle" width="100%">The no of rooms cancelled two weeks prior to the conference full retention for the entire period of booking will be charged.</td></tr><tr><td height="25" width="100%"></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td valign="top" bgcolor="#344b61" align="center" width="100%"><table class="mobile" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td align="center"><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="10" width="100%"></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="600"><tbody><tr><td align="center" width="100%"><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="fullCenter" cellspacing="0" cellpadding="0" align="left" border="0" width="140"><tbody><tr><td style="text-align: center;font-family: Helvetica, Arial, sans-serif;font-size: 12px;color: #ffffff;line-height: 15px;font-weight: 400;padding-left: 30px;" class="fullCenter" valign="middle" width="200px">Aura Goa Wellness Resort, Mandrem, North Goa<br>+91 76653-22222<br><a>info@auragoa.com</a><br><a href="http://auragoa.com/" style="text-decoration: none; color: #ffffff;">auragoa.com</a></td></tr></tbody></table><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="full" cellspacing="0" cellpadding="0" align="left" border="0" width="20"><tbody><tr><td height="1" width="100%"></td></tr></tbody></table><table style="text-align: right; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="buttonScale" cellspacing="0" cellpadding="0" align="right" border="0" width="96"><tbody><tr><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"><a href="https://twitter.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_1.png" alt="" class="hover" border="0" width="17"></a></td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://www.facebook.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_2.png" alt="" class="hover" border="0" width="17"></a></td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://plus.google.com/u/0/103796393489619851236" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_3.png" alt="" class="hover" border="0" width="17"></a></td></tr></tbody></table></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="10" width="100%"></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></table></center></td></tr></table></body></html>'
			#send_mail('Successfully Registered', 'Someone Just Logined from your Account if that was not you then Contact to Admin. Logined at '+str(timezone.now())+' Time ', 'Auragoa <donotreply@auragoa.com>', [email], html_message=html_content, fail_silently=False)

			sender = 'donotreply@auragoa.com'
			receiver = email
			subject = 'Guest Registration'
			body = html_content
			purpose = 'Registration'
			Email_cron.objects.create(email_uid_id = user.id, email_from=sender, email_to=receiver, email_subject=subject, email_body=body, email_purpose=purpose)

		else:
			raise Exception('Permission Denied')
		return bundle

	def obj_update(self, bundle, request=None, **kwargs):
		username = bundle.request.GET['username']
		user = User.objects.get(username=username)
		if user.has_perm('Guest.change_guest'):
			user_bundle = super(GuestResource, self).obj_update(bundle, request=None, **kwargs)
		else:
			raise Exception('Permission Denied')

		return user_bundle

	def hydrate(self, bundle):
		request = get_current_request()
		email = bundle.data.get('guest_email')
		
		if request.method == 'POST':
			bundle.data['guest_track'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family 
			bundle.data['guest_utrack'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family 
			bundle.data['guest_email'] = bundle.data['guest_email'].lower()
			bundle.data['guest_referal_url'] = request.META['HTTP_REFERER']

		elif request.method == 'PUT':
			bundle.data['guest_utrack'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family 
			bundle.data['guest_utimestamp'] = timezone.now()
			if email:
				bundle.data['guest_email'] = bundle.data['guest_email'].lower()
			
		return bundle





class GworkResource(ModelResource):
	gwork_gid = fields.ForeignKey(GuestResource, 'gwork_gid', full=True)
	gwork_country = fields.ForeignKey(CountryResource, 'gwork_country', full=True, blank=True, null=True)
	gwork_state = fields.ForeignKey(StateResource, 'gwork_state', full=True, blank=True, null=True)
	class Meta:
		queryset = gwork.objects.all()
		resource_name = 'gwork'
		filtering = {
			'gwork_id' : ALL
		}
		limit = 0
		always_return_data = True
		authentication = AdminApiKeyAuthentication()
		authorization = Authorization()
		serializer = urlencodeSerializer()

	def obj_create(self, bundle, request=None, **kwargs):
		username = bundle.request.GET['username']
		user = User.objects.get(username=username)
		if user.has_perm('Guest.add_gwork'):
			bundle = super(GworkResource, self).obj_create(bundle)
		else:
			raise Exception('Permission Denied')

		return bundle

	def obj_update(self, bundle, request=None, **kwargs):
		username = bundle.request.GET['username']
		user = User.objects.get(username=username)
		if user.has_perm('Guest.change_gwork'):
			user_bundle = super(GworkResource, self).obj_update(bundle, request=None, **kwargs)
		else:
			raise Exception('Permission Denied')

		return user_bundle

	def hydrate(self, bundle):
		request = get_current_request()
		email = bundle.data.get('gwork_email')
		
		if request.method == 'POST':
			bundle.data['gwork_track'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['gwork_utrack'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			if email:
				bundle.data['gwork_email'] = bundle.data['gwork_email'].lower()	
		elif request.method == 'PUT':
			bundle.data['gwork_utrack'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['gwork_utimestamp'] = timezone.now()
			if email:
				bundle.data['gwork_email'] = bundle.data['gwork_email'].lower()
			
		return bundle

class GotherResource(ModelResource):
	gother_gid = fields.ForeignKey(GuestResource, 'gother_gid', full=True)
	class Meta:
		queryset = gother.objects.all()
		resource_name = 'gother'
		filtering = {
			'gother_gid' : ALL_WITH_RELATIONS
		}
		limit = 0
		always_return_data = True
		authentication = AdminApiKeyAuthentication()
		authorization = Authorization()
		serializer = urlencodeSerializer()

	def obj_create(self, bundle, request=None, **kwargs):
		username = bundle.request.GET['username']
		user = User.objects.get(username=username)
		if user.has_perm('Guest.add_gother'):
			bundle = super(GotherResource, self).obj_create(bundle)
		else:
			raise Exception('Permission Denied')

		return bundle

	def obj_update(self, bundle, request=None, **kwargs):
		username = bundle.request.GET['username']
		user = User.objects.get(username=username)
		if user.has_perm('Guest.change_gother'):
			user_bundle = super(GotherResource, self).obj_update(bundle, request=None, **kwargs)
		else:
			raise Exception('Permission Denied')

		return user_bundle

	def hydrate(self, bundle):
		request = get_current_request()
		
		if request.method == 'POST':
			bundle.data['gother_track'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['gother_utrack'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
				
		elif request.method == 'PUT':
			bundle.data['gother_utrack'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['gother_utimestamp'] = timezone.now()
			
		return bundle

class Guest_detailResource(ModelResource):
	
	class Meta:
		queryset = Guest.objects.all()
		resource_name = 'guest_detail'
		filtering = {
			'guest_id' : ALL,
			'guest_fname' : ALL,
			'guest_lname' : ALL,
			'guest_email' : ALL,
			'guest_mobile' : ALL,
			'guest_nationality' : ALL,
			'guest_address' : ALL,
			'guest_country' : ALL,
			'guest_state' : ALL, 
			'guest_city' : ALL, 
			'guest_type' : ALL
		}
		limit = 0
		always_return_data = True
		authentication = AdminApiKeyAuthentication()
		authorization = Authorization()
		serializer = urlencodeSerializer()

	def dehydrate(self, bundle):
		x = bundle.obj.pk
		if x:
			booking = Booking.objects.filter(booking_gid__guest_id=x)
			bundle.data['booking_count'] = booking.count()
			shyam = {}
			n = 0
			for i in booking:
				shyam[n] = {'booking_advance':i.booking_advance, 'booking_adult':i.booking_adult, 'booking_amount':i.booking_amount, 'booking_arrival':i.booking_arrival, 'booking_checkin':i.booking_checkin, 'booking_checkin_type':i.booking_checkin_type, 'booking_checkout':i.booking_checkout, 'booking_child':i.booking_child, 'booking_departure':i.booking_departure, 'booking_discount':i.booking_discount, 'booking_duration':i.booking_duration, 'booking_expected_checkin':i.booking_expected_checkin, 'booking_expected_checkout':i.booking_expected_checkout, 'booking_id':i.booking_id, 'booking_messages':i.booking_messages, 'booking_note':i.booking_note, 'booking_rid':i.booking_rid, 'booking_room_count':i.booking_room_count, 'booking_status':i.booking_status, 'booking_tentative_arrival':i.booking_tentative_arrival, 'booking_tentative_departure':i.booking_tentative_departure, 'booking_timestamp':i.booking_timestamp, 'booking_track':i.booking_track, 'booking_ueid':i.booking_ueid, 'booking_utimestamp':i.booking_utimestamp, 'booking_utrack':i.booking_utrack}
				bundle.data['bookings'] = shyam
				n = n + 1

		else:
			booking = Booking.objects.filter(booking_gid__guest_id=bundle.obj.guest_id)
			bundle.data['booking_count'] = booking.count()
			shyam = {}
			n = 0
			for i in booking:
				shyam[n] = {'booking_advance':i.booking_advance, 'booking_adult':i.booking_adult, 'booking_amount':i.booking_amount, 'booking_arrival':i.booking_arrival, 'booking_checkin':i.booking_checkin, 'booking_checkin_type':i.booking_checkin_type, 'booking_checkout':i.booking_checkout, 'booking_child':i.booking_child, 'booking_departure':i.booking_departure, 'booking_discount':i.booking_discount, 'booking_duration':i.booking_duration, 'booking_expected_checkin':i.booking_expected_checkin, 'booking_expected_checkout':i.booking_expected_checkout, 'booking_id':i.booking_id, 'booking_messages':i.booking_messages, 'booking_note':i.booking_note, 'booking_rid':i.booking_rid, 'booking_room_count':i.booking_room_count, 'booking_status':i.booking_status, 'booking_tentative_arrival':i.booking_tentative_arrival, 'booking_tentative_departure':i.booking_tentative_departure, 'booking_timestamp':i.booking_timestamp, 'booking_track':i.booking_track, 'booking_ueid':i.booking_ueid, 'booking_utimestamp':i.booking_utimestamp, 'booking_utrack':i.booking_utrack}
				bundle.data['bookings'] = shyam
				n = n + 1

		return bundle

class Guest_fullResource(ModelResource):
	guest_country = fields.ForeignKey(CountryResource, 'guest_country', full=True, blank=True, null=True)
	guest_state = fields.ForeignKey(StateResource, 'guest_state', full=True, blank=True, null=True)
	
	class Meta:
		queryset = Guest.objects.all()
		resource_name = 'guest_full'
		limit = 0
		always_return_data = True
		
	def dehydrate(self, bundle):
		i = gwork.objects.filter(gwork_gid__guest_id=bundle.obj.guest_id)
		j = gother.objects.filter(gother_gid__guest_id=bundle.obj.guest_id)

		if i:
			for l in i:
				if l.gwork_country:
					bundle.data['gwork'] = {'gwork_address':l.gwork_address, 'gwork_city':l.gwork_city, 'gwork_country':l.gwork_country.country_id, 'gwork_designation':l.gwork_designation, 'gwork_email':l.gwork_email, 'gwork_fax':l.gwork_fax, 'gwork_id':l.gwork_id, 'gwork_mobile':l.gwork_mobile, 'gwork_organization':l.gwork_organization, 'gwork_phone':l.gwork_phone, 'gwork_state':l.gwork_state.state_id, 'gwork_timestamp':l.gwork_timestamp, 'gwork_track':l.gwork_timestamp, 'gwork_utimestamp':l.gwork_utimestamp, 'gwork_utrack':l.gwork_utrack, 'gwork_zipcode':l.gwork_zipcode}

				else:
					bundle.data['gwork'] = {'gwork_address':l.gwork_address, 'gwork_city':l.gwork_city, 'gwork_country':l.gwork_country, 'gwork_designation':l.gwork_designation, 'gwork_email':l.gwork_email, 'gwork_fax':l.gwork_fax, 'gwork_id':l.gwork_id, 'gwork_mobile':l.gwork_mobile, 'gwork_organization':l.gwork_organization, 'gwork_phone':l.gwork_phone, 'gwork_state':l.gwork_state, 'gwork_timestamp':l.gwork_timestamp, 'gwork_track':l.gwork_timestamp, 'gwork_utimestamp':l.gwork_utimestamp, 'gwork_utrack':l.gwork_utrack, 'gwork_zipcode':l.gwork_zipcode}
		if j:
			for m in j:
				bundle.data['gother'] = {'gother_anniversory':m.gother_anniversory, 'gother_birthday':m.gother_birthday, 'gother_details':m.gother_details, 'gother_id':m.gother_id, 'gother_preferences':m.gother_preferences, 'gother_spouse_fname':m.gother_spouse_fname, 'gother_spouse_lname':m.gother_spouse_lname, 'gother_spouse_title':m.gother_spouse_title, 'gother_status':m.gother_status, 'gother_timestamp':m.gother_timestamp, 'gother_track':m.gother_track, 'gother_utimestamp':m.gother_utimestamp, 'gother_utrack':m.gother_utrack}

		return bundle

class GuestgroupResource(ModelResource):
	guest_uid = fields.ForeignKey(UserResource, 'guest_uid', full=True)
	class Meta:
		queryset = Guest.objects.all()
		resource_name = 'guestgroup'
		#allowed_methods = ['get', 'post', 'delete', 'put','patch']

		limit = 0
		always_return_data = True
		#authentication = AdminApiKeyAuthentication()
		#authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
		#authorization = DjangoAuthorization()
		authentication = AdminApiKeyAuthentication()
		authorization = Authorization()
		serializer = urlencodeSerializer()
		filtering = {
			'guest_id' : ALL,
			'guest_fname' : ALL, 
			'guest_lname' : ALL,
			'guest_email' : ALL,
			'guest_mobile' : ALL,
			'guest_nationality' : ALL,
			'guest_address' : ALL,
			'guest_country' : ALL,
			'guest_state' : ALL,
			'guest_city' : ALL,
			'guest_type' : ALL
		}

	def obj_create(self, bundle, request=None, **kwargs):
		request = get_current_request()
		username = bundle.request.GET['username']
		user = User.objects.get(username=username)
		email1 = bundle.data.get('guest_email', '')
		name = bundle.data.get('guest_fname', '')

		#booking detail getting
		roomid = bundle.data.get('booking_rid', '')
		#amount = bundle.data.get('booking_amount', '')
		arrival = bundle.data.get('booking_arrival', '')
		departure = bundle.data.get('booking_departure', '')

		#checking for departue not less than or equal to arrival
		if departure <= arrival:
			raise Exception("Give appropriate date for departure")

		#duration  calculation according to booking_arrival and booking_departure
		arrival_date = dateutil.parser.parse(arrival).date()
		departure_date = dateutil.parser.parse(departure).date()
		duration = (departure_date - arrival_date).days
		
		#tracking while object creation of booking
		track = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
		utrack = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family

		if user.has_perm('Guest.add_guest'):  #permission checking during post
			bundle = super(GuestgroupResource, self).obj_create(bundle)
			#del bundle.data['booking_rid']

			bundle.obj.save()

			#booking_rid in the form of id splitting
			rid = str(roomid)
			ridsplit = rid.split(',')
			count = len(ridsplit)
			
			total_amount = 0
			for i in range(count):
				room_detail = Room.objects.get(room_id=ridsplit[i])
				room_price = room_detail.room_type_id.room_type_price
				amount = room_price * duration

				#amount = bundle.data.get('booking_amount')
				disc = bundle.data.get('booking_discount')
				amount = int(amount)
				if disc:
					discount = disc
				else:
					discount = 0

				x = amount - int(discount)
				tax1 = (x * (float(9)/100))
				if amount >= 3000 and amount < 5000:
					tax2 = (amount * (float(9)/100))
				else:
					tax2 = (amount * (float(12)/100))

				# bundle.data['booking_tax'] = tax1 + tax2
				# bundle.data['booking_total'] = tax1 + tax2 + x
				tax = tax1 + tax2
				total = tax + x
				total_amount = total_amount + total

				Booking.objects.bulk_create([
					Booking(booking_gid_id=bundle.obj.guest_id, booking_rid_id=ridsplit[i], booking_amount=amount, booking_arrival=arrival, booking_departure=departure, booking_duration=duration, booking_track=track, booking_utrack=utrack, booking_tax=tax, booking_total=total, booking_ueid=user.id )
					])

			grp_book = Booking.objects.filter(booking_gid_id=bundle.obj.guest_id).filter(booking_arrival=arrival)
			bkid = []
			typess = []
			for j in grp_book:
				bkid.append(j.booking_id)
				typess.append(j.booking_rid.room_type_id.room_type_title)

			bkid_string = ",".join(str(elm) for elm in bkid)
			typess_string = ",".join(str(elmn) for elmn in typess)
			
			del bundle.data['booking_rid']
			#del bundle.data['booking_amount']
			del bundle.data['booking_arrival']
			del bundle.data['booking_departure']

			amount = str(total_amount)
			bkid = str(bkid_string)
			arrival = str(arrival_date)
			departure = str(departure_date)
			fname = str(bundle.obj.guest_fname)
			lname = str(bundle.obj.guest_lname)
			title = str(bundle.obj.guest_title)
			types = str(typess_string)
			#raise Exception(title)
				

			email = email1
			#html_content = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><title>payment aura</title><style type="text/css">/* Take care of image borders and formatting */img{max-width: 600px;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;}a img{border: none;}table{border-collapse: collapse !important;}#outlook a{padding:0;}.ReadMsgBody{width: 100%;}.ExternalClass{width:100%;}.backgroundTable{margin:0 auto; padding:0; width:100%;}table td{border-collapse: collapse;}.ExternalClass *{line-height: 115%;}/* General styling */td{font-family: Arial, sans-serif;color: #6f6f6f;}body{-webkit-font-smoothing:antialiased;-webkit-text-size-adjust:none;width: 100%;height: 100%;color: #6f6f6f;font-weight: 400;font-size: 18px;}h1{margin: 10px 0;}a{color: #27aa90;text-decoration: none;}.force-full-width{width: 100% !important;}.force-width-80{width: 80% !important;}.body-padding{padding: 0 75px;}.mobile-align{text-align: right;}</style><style type="text/css" media="screen">@media screen{@import url(http://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600,900);/* Thanks Outlook 2013! */*{font-family: "Source Sans Pro", "Helvetica Neue", "Arial", "sans-serif" !important;}.w280{width: 280px !important;}}</style><style type="text/css" media="only screen and (max-width: 480px)">/* Mobile styles */@media only screen and (max-width: 480px){table[class*="w320"]{width: 320px !important;}td[class*="w320"]{width: 280px !important;padding-left: 20px !important;padding-right: 20px !important;}img[class*="w320"]{width: 250px !important;height: 67px !important;}td[class*="mobile-spacing"]{padding-top: 10px !important;padding-bottom: 10px !important;}*[class*="mobile-hide"]{display: none !important;}*[class*="mobile-br"]{font-size: 12px !important;}td[class*="mobile-w20"]{width: 20px !important;}img[class*="mobile-w20"]{width: 20px !important;}td[class*="mobile-center"]{text-align: center !important;}table[class*="w100p"]{width: 100% !important;}td[class*="activate-now"]{padding-right: 0 !important;padding-top: 20px !important;}td[class*="mobile-block"]{display: block !important;}td[class*="mobile-align"]{text-align: left !important;}}</style></head><body offset="0" class="body" style="padding:0; margin:0; display:block; -webkit-text-size-adjust:none" bgcolor="#eeebeb"><table align="center" cellpadding="0" cellspacing="0" width="100%" height="100%" ><tr><td align="center" valign="top" width="100%"><center style="font-family: Calibri, Verdana, Ariel, sans-serif;"><table cellspacing="0" cellpadding="0" width="600" class="w320"><tr><td align="center" valign="top"><table cellspacing="0" cellpadding="0" width="100%" style="background-color:#3bcdb0;"><tr><td style="background-color:#3bcdb0;"><table style="margin:0 auto;" cellspacing="0" cellpadding="0" width="100%"></table><table cellspacing="0" cellpadding="0" width="100%"><tr><td style="font-size:20px; font-weight: 600; color: #ffffff; text-align:center;" class="mobile-spacing"><div class="mobile-br">&nbsp;</div>Thank you for choosing Auragoa Spa Retreat Resort.<br></td></tr><tr><td style="font-size:16px; text-align:center; padding: 5px 75px; color: #6f6f6f;" class="w320 mobile-spacing">We are pleased to confirm your Payment as under:</td></tr></table><table cellspacing="0" cellpadding="0" width="100%"><tr><td><img src="http://demodevelopment.in/mail_img/s_design12.png" style="max-width:100%; display:block;"></td></tr></table></td></tr></table><table cellspacing="0" cellpadding="0" width="100%" bgcolor="#ffffff" ><tr><td style="background-color:#ffffff;"><table style=" text-align: center; margin-top:48px;margin-bottom:48px; font-size: 13px;" cellspacing="0" cellpadding="0" border="0" width="100%"><tbody><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Transaction ID</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">123456789</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Booking No.</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">0123456789</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Date of Arrival</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">9th September, 2014</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Date of Departure</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">9th September, 2014</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Accommodation</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">Deluxe Suite</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Amount to be pay</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">Rs.4000/-(excluding of taxes)</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Check In</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">9:00 am, 9th September, 2014</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="20%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Check Out</b></td><td width="20%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">9:00 am, 9th September, 2014</td><td width="20%"></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td valign="top" bgcolor="#344b61" align="center" width="100%"><table class="mobile" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td align="center"><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="10" width="100%"></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="600"><tbody><tr><td align="center" width="100%"><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="fullCenter" cellspacing="0" cellpadding="0" align="left" border="0" width="140"><tbody><tr><td style="text-align: center; font-family: Helvetica, Arial, sans-serif; font-size: 12px; color: #ffffff; line-height: 15px; font-weight: 400;padding-left: 30px;" class="fullCenter" valign="middle" width="100%">Aura Goa Wellness Resort, Mandrem, North Goa<br>+91 76653-22222<br>info@auragoa.com<br><a href="http://auragoa.com/" style="text-decoration: none; color: #ffffff;">auragoa.com</a></td></tr></tbody></table><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="full" cellspacing="0" cellpadding="0" align="left" border="0" width="20"><tbody><tr><td height="1" width="100%"></td></tr></tbody></table><table style="text-align: right; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="buttonScale" cellspacing="0" cellpadding="0" align="right" border="0" width="96"><tbody><tr><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"><a href="https://twitter.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_1.png" alt="" class="hover" border="0" width="17"></a></td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://www.facebook.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_2.png" alt="" class="hover" border="0" width="17"></a></td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://plus.google.com/u/0/103796393489619851236" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_3.png" alt="" class="hover" border="0" width="17"></a></td></tr></tbody></table></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="10" width="100%"></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></table></td></tr></table></center></td></tr></table></body></html>'
			#html_content = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><title>booking aura</title><style type="text/css">/* Take care of image borders and formatting */img{max-width: 600px;outline: none;text-decoration: none;-ms-interpolation-mode:bicubic;}a img{border: none;}table{border-collapse: collapse !important;}#outlook a{padding:0;}.ReadMsgBody{width: 100%;}.ExternalClass{width:100%;}.backgroundTable{margin:0 auto; padding:0; width:100%;}table td{border-collapse: collapse;}.ExternalClass *{line-height: 115%;}/* General styling */td{font-family: Arial, sans-serif;color: #6f6f6f;}body{-webkit-font-smoothing:antialiased;-webkit-text-size-adjust:none;width: 100%;height: 100%;color: #6f6f6f;font-weight: 400;font-size: 18px;}h1{margin: 10px 0;}a{color: #27aa90;text-decoration: none;}.force-full-width{width: 100% !important;}.force-width-80{width: 80% !important;}.body-padding{padding: 0 75px;}.mobile-align{text-align: right;}</style><style type="text/css" media="screen">@media screen{@import url(http://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600,900);/* Thanks Outlook 2013! */*{font-family: "Source Sans Pro", "Helvetica Neue", "Arial", "sans-serif" !important;}.w280{width: 280px !important;}}</style><style type="text/css" media="only screen and (max-width: 480px)">/* Mobile styles */@media only screen and (max-width: 480px){table[class*="w320"]{width: 320px !important;}td[class*="w320"]{width: 280px !important;padding-left: 20px !important;padding-right: 20px !important;}img[class*="w320"]{width: 250px !important;height: 67px !important;}td[class*="mobile-spacing"]{padding-top: 10px !important;padding-bottom: 10px !important;}*[class*="mobile-hide"]{display: none !important;}*[class*="mobile-br"]{font-size: 12px !important;}td[class*="mobile-w20"]{width: 20px !important;}img[class*="mobile-w20"]{width: 20px !important;}td[class*="mobile-center"]{text-align: center!important;}table[class*="w100p"]{width: 100% !important;}td[class*="activate-now"]{padding-right: 0 !important;padding-top: 20px !important;}td[class*="mobile-block"]{display: block !important;}td[class*="mobile-align"]{text-align: left !important;}}</style></head><body offset="0" class="body" style="padding:0; margin:0; display:block; -webkit-text-size-adjust:none" bgcolor="#eeebeb"><table align="center" cellpadding="0" cellspacing="0" width="100%" height="100%" ><tr><td align="center" valign="top" width="100%"><center style="font-family: Calibri, Verdana, Ariel, sans-serif;"><table cellspacing="0" cellpadding="0" width="600" class="w320"><tr><td align="center" valign="top"><table cellspacing="0" cellpadding="0" width="100%" style="background-color:#3bcdb0;"><tr><td style="background-color:#3bcdb0;"><table style="margin:0 auto;" cellspacing="0" cellpadding="0" width="100%"></table><table cellspacing="0" cellpadding="0" width="100%"><tr><td><img src="http://demodevelopment.in/mail_img/s_design12.png" style="max-width:100%; display:block;"></td></tr></table></td></tr></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td valign="top" align="center" width="100%"><table class="mobile" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td align="center" style="background-color:#ffffff;"><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="60" width="100%"></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="600"><tbody><tr><td align="center" width="100%"><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="fullCenter" cellspacing="0" cellpadding="0" align="center" border="0" width="600"><tbody><tr><td style="text-align: center; font-size: 20px; color: #444444; line-height: 32px; font-weight: 700;" class="fullCenter" valign="middle" width="100%">Hi '+name+',</td></tr><tr><td height="30" width="100%"></td></tr><tr><td width="100%"><table cellspacing="0" cellpadding="0" align="center" border="0" width="100"><tbody><tr><td style="font-size: 1px; line-height: 1px;" bgcolor="#808080" height="1" width="100">&nbsp;</td></tr></tbody></table></td></tr><tr><td height="30" width="100%"></td></tr><tr><td style="text-align: center; font-size: 14px; color: #808080; line-height: 22px; font-weight: 400;" class="fullCenter" valign="middle" width="100%">Are you still looking to book a room at our hotel. We hope to serve you better at our hotel. Please click on our website link below to book.</td></tr><tr><td height="25" width="100%"></td></tr><tr><td style="text-align: center; font-size: 14px; color: #808080; line-height: 22px; font-weight: 400;" class="fullCenter" valign="middle" width="100%">Booking cancelled after 60 days of confirmation one day retention will be charged for all the rooms confirmed.</td></tr><tr><td height="25" width="100%"></td></tr><tr><td style="text-align: center; font-size: 14px; color: #808080; line-height: 22px; font-weight: 400;" class="fullCenter" valign="middle" width="100%">The no of rooms cancelled two weeks prior to the conference full retention for the entire period of booking will be charged.</td></tr><tr><td height="25" width="100%"></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td valign="top" bgcolor="#344b61" align="center" width="100%"><table class="mobile" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td align="center"><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="10" width="100%"></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="600"><tbody><tr><td align="center" width="100%"><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="fullCenter" cellspacing="0" cellpadding="0" align="left" border="0" width="140"><tbody><tr><td style="text-align: center;font-family: Helvetica, Arial, sans-serif;font-size: 12px;color: #ffffff;line-height: 15px;font-weight: 400;padding-left: 30px;" class="fullCenter" valign="middle" width="200px">Aura Goa Wellness Resort, Mandrem, North Goa<br>+91 76653-22222<br><a>info@auragoa.com</a><br><a href="http://auragoa.com/" style="text-decoration: none; color: #ffffff;">auragoa.com</a></td></tr></tbody></table><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="full" cellspacing="0" cellpadding="0" align="left" border="0" width="20"><tbody><tr><td height="1" width="100%"></td></tr></tbody></table><table style="text-align: right; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="buttonScale" cellspacing="0" cellpadding="0" align="right" border="0" width="96"><tbody><tr><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"><a href="https://twitter.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_1.png" alt="" class="hover" border="0" width="17"></a></td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://www.facebook.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_2.png" alt="" class="hover" border="0" width="17"></a></td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://plus.google.com/u/0/103796393489619851236" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_3.png" alt="" class="hover" border="0" width="17"></a></td></tr></tbody></table></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="10" width="100%"></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></table></center></td></tr></table></body></html>'
			html_content = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><title>welcome aura</title><style type="text/css">/* Take care of image borders and formatting */img{max-width: 600px;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;}a img{border: none;}table{border-collapse: collapse !important;}#outlook a{padding:0;}.ReadMsgBody{width: 100%;}.ExternalClass{width:100%;}.backgroundTable{margin:0 auto; padding:0; width:100%;}table td{border-collapse: collapse;}.ExternalClass *{line-height: 115%;}/* General styling */td{font-family: Arial;color: #6f6f6f;}body{-webkit-font-smoothing:antialiased;-webkit-text-size-adjust:none;width: 100%;height: 100%;color: #6f6f6f;font-weight: 400;font-size: 18px;}h1{margin: 10px 0;}a{color: #27aa90;text-decoration: none;}.force-full-width{width: 100% !important;}.force-width-80{width: 80% !important;}.body-padding{padding: 0 75px;}.mobile-align{text-align: right;}</style><style type="text/css" media="screen">@media screen{@import url(http://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600,900);/* Thanks Outlook 2013! */*{font-family: "Arial" !important;}.w280{width: 280px !important;}}</style><style type="text/css" media="only screen and (max-width: 480px)">/* Mobile styles */@media only screen and (max-width: 480px){table[class*="w320"]{width: 320px !important;}td[class*="w320"]{width: 280px !important;padding-left: 20px !important;padding-right: 20px !important;}img[class*="w320"]{width: 250px !important;height: 67px !important;}td[class*="mobile-spacing"]{padding-top: 10px !important;padding-bottom: 10px !important;}*[class*="mobile-hide"]{display: none !important;}*[class*="mobile-br"]{font-size: 12px !important;}td[class*="mobile-w20"]{width: 20px !important;}img[class*="mobile-w20"]{width: 20px !important;}td[class*="mobile-center"]{text-align: center !important;}table[class*="w100p"]{width: 100% !important;}td[class*="activate-now"]{padding-right: 0 !important;padding-top: 20px !important;}td[class*="mobile-block"]{display: block !important;}td[class*="mobile-align"]{text-align: left !important;}}</style></head><body offset="0" class="body" style="padding:0; margin:0; display:block; -webkit-text-size-adjust:none" bgcolor="#eeebeb"><table align="center" cellpadding="0" cellspacing="0" width="100%" height="100%" ><tr><td align="center" valign="top" width="100%"><center style="font-family: Arial;"><table cellspacing="0" cellpadding="0" width="600" class="w320"><tr><td align="center" valign="top"><table cellspacing="0" cellpadding="0" width="100%" style="background-color:#3bcdb0;"><tr><td style="background-color:#3bcdb0;"><table style="margin:0 auto;" cellspacing="0" cellpadding="0" width="100%"></table><table cellspacing="0" cellpadding="0" width="100%"><tr><td style="font-size:20px; font-weight: 600; color: #ffffff; text-align:center;" class="mobile-spacing"><div class="mobile-br">&nbsp;</div>Thank you for choosing Auragoa Spa Retreat Resort.<br></td></tr><tr><td style="font-size:16px; text-align:center; padding: 5px 75px; color: #6f6f6f;" class="w320 mobile-spacing">We are pleased to confirm your reservation as under:</td></tr></table><table cellspacing="0" cellpadding="0" width="100%"><tr><td><img src="http://demodevelopment.in/mail_img/s_design12.png" style="max-width:100%; display:block;"></td></tr></table><table class="mobile" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td class="icon54" align="center"><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="170"><tbody><tr><td class="icon34" valign="top" align="center" width="100%"><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="fullCenter" cellspacing="0" cellpadding="0" align="right" border="0" width="175"><tbody><tr><td height="25" width="100%"></td></tr><tr><td style="text-align: center; font-family:Arial; font-size: 18px; color: #ffffff; line-height: 18px; font-weight: 600;" class="fullCenter" valign="middle" width="100%">Booking id: '+bkid+'</td></tr><tr><td height="10" width="100%"></td></tr><tr><td style="text-align: center; font-family:Arial; font-size: 15px; color: #ffffff; line-height: 24px; font-weight: 600;" class="fullCenter" valign="middle" width="100%">Dear '+title+'. '+fname+' '+lname+'</td></tr></tbody></table></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="60" width="100%"></td></tr></tbody></table></td></tr></tbody></table></td></tr></table><table cellspacing="0" cellpadding="0" width="100%" bgcolor="#ffffff" ><tr><td style="background-color:#ffffff;"><table style=" text-align: center; margin-top:48px;margin-bottom:48px; font-size: 13px;" cellspacing="0" cellpadding="0" border="0" width="100%"><tbody><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Name of Guest</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+title+'. '+fname+' '+lname+'</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Date of Arrival</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+arrival+'</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Date of Departure</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+departure+'</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Accommodation</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+types+'</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Amount to be pay</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+amount+'/-(excluding of taxes)</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="30%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Check In</b></td><td width="30%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+arrival+'</td><td width="20%"></td></tr><tr valign="middle"><td height="24px" width="32px"></td></tr><tr valign="middle"><td width="20%"></td><td width="20%" align="left" style="border-bottom:1px solid #e3e3e3;"><b>Check Out</b></td><td width="20%" style="line-height:1.2; text-align:center;border-bottom:1px solid #e3e3e3;">'+departure+'</td><td width="20%"></td></tr></tbody></table><table style="margin:0 auto;" cellspacing="0" cellpadding="10" width="100%"><tr><td style="text-align:center; margin:0 auto;"><br><div><a href="http://"style="background-color:#f5774e;color:#ffffff;display:inline-block;font-family:Arial;font-size:18px;font-weight:400;line-height:45px;text-align:center;text-decoration:none;width:180px;-webkit-text-size-adjust:none;border-radius:20px;">Term & Conditions</a></div><br></td></tr></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td valign="top" bgcolor="#344b61" align="center" width="100%"><table class="mobile" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td align="center"><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="10" width="100%"></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="600"><tbody><tr><td align="center" width="100%"><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="fullCenter" cellspacing="0" cellpadding="0" align="left" border="0" width="140"><tbody><tr><td style="text-align: center;font-family: Helvetica, Arial, sans-serif;font-size: 12px;color: #ffffff;line-height: 15px;font-weight: 400;padding-left: 30px;" class="fullCenter" valign="middle" width="200px">Aura Goa Wellness Resort, Mandrem, North Goa<br>+91 76653-22222<br>info@auragoa.com<br><a href="http://auragoa.com/" style="text-decoration: none; color: #ffffff;">auragoa.com</a></td></tr></tbody></table><table style="border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="full" cellspacing="0" cellpadding="0" align="left" border="0" width="20"><tbody><tr><td height="1" width="100%"></td></tr></tbody></table><table style="text-align: right; border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt;" class="buttonScale" cellspacing="0" cellpadding="0" align="right" border="0" width="96"><tbody><tr><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"><a href="https://twitter.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_1.png" alt="" class="hover" border="0" width="17"></a></td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://www.facebook.com/aurasparetreat" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_2.png" alt="" class="hover" border="0" width="17"></a></td><td class="icons17" style="text-align: left;" valign="middle" align="center" height="45" width="32"> <a href="https://plus.google.com/u/0/103796393489619851236" style="text-decoration: none;"><img src="http://demodevelopment.in/mail_img/social_icon_3.png" alt="" class="hover" border="0" width="17"></a></td></tr></tbody></table></td></tr></tbody></table><table class="full" cellspacing="0" cellpadding="0" align="center" border="0" width="100%"><tbody><tr><td height="10" width="100%"></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></table></td></tr></table></center></td></tr></table></body></html>'
			send_mail('Successfully Registered', 'Someone Just Logined from your Account if that was not you then Contact to Admin. Logined at '+str(timezone.now())+' Time ', 'Auragoa <donotreply@auragoa.com>', [email], html_message=html_content, fail_silently=False)
		else:
			raise Exception('Permission Denied')
		return bundle

	def obj_update(self, bundle, request=None, **kwargs):
		username = bundle.request.GET['username']
		user = User.objects.get(username=username)
		if user.has_perm('Guest.change_guest'):
			user_bundle = super(GuestgroupResource, self).obj_update(bundle, request=None, **kwargs)
		else:
			raise Exception('Permission Denied')

		return user_bundle

	def hydrate(self, bundle):
		request = get_current_request()
		
		if request.method == 'POST':
			bundle.data['guest_track'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['guest_utrack'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
				
		elif request.method == 'PUT':
			bundle.data['guest_utrack'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['guest_utimestamp'] = timezone.now()
			
		return bundle






		


