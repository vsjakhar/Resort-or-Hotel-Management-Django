# -*- coding: utf-8 -*-
from tastypie.authorization import Authorization
from tastypie import fields
from django.db import models
from django.contrib.auth.models import User
from tastypie.resources import ModelResource,ALL, ALL_WITH_RELATIONS
from .models import Payment,Folio
from jakhar.api import urlencodeSerializer, AdminApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization, ReadOnlyAuthorization, Authorization
from Guest.api import GuestResource
from booking.api import BookingResource
from crum import get_current_request

from django.db.models import Sum
from django.core.mail import send_mail
from django.utils import timezone
#from models import sum
#from django.db.models import *

from email_cronjob.models import Email_cron


class PaymentResource(ModelResource):
	payment_gid = fields.ForeignKey(GuestResource, 'payment_gid', full=True, null=True, blank=True)
	payment_bid = fields.ForeignKey(BookingResource, 'payment_bid', full=True, null=True, blank=True)
	class Meta:
		queryset = Payment.objects.all()
		resource_name = 'payment'
		allowed_methods = ['get', 'post']
		filtering = {
			'payment_gid': ALL_WITH_RELATIONS,
			'payment_bid': ALL_WITH_RELATIONS,
			'payment_timestamp': ALL, #['ALL','contains','startswith','endswith','exact'],
			'payment_utimestamp': ALL,
			'payment_from': ALL
		}
		limit = 0
		always_return_data = True
		authentication = AdminApiKeyAuthentication()
		authorization = Authorization()
		serializer = urlencodeSerializer()

	def obj_create(self, bundle, request=None, **kwargs):
		username = bundle.request.GET['username']
		user = User.objects.get(username=username)
		guestemail = bundle.data.get('payment_gid', '')
		if user.has_perm('payment.add_payment'):  #permission checking during post
			bundle = super(PaymentResource, self).obj_create(bundle)
			bundle.obj.save()
			if guestemail:

				pay_id = str(bundle.obj.payment_id)
				amount = str(bundle.obj.payment_amount)
				discount = str(bundle.obj.payment_discount)
				total = str(bundle.obj.payment_total)
				fname = str(bundle.obj.payment_gid.guest_fname)
				lname = str(bundle.obj.payment_gid.guest_lname)
				description = str(bundle.obj.payment_description)
				email = bundle.obj.payment_gid.guest_email
				
				html_content = '<!DOCTYPE html><html xmlns=http://www.w3.org/1999/xhtml><meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"><head><meta content="text/html; charset=UTF-8" http-equiv="Content-Type"><meta content="width=device-width,initial-scale=1" name="viewport"><title>Payment</title><style>img{max-width:600px;outline:0;text-decoration:none;-ms-interpolation-mode:bicubic}a img{border:none}table{border-collapse:collapse!important}#outlook a{padding:0}.ReadMsgBody{width:100%}.ExternalClass{width:100%}.backgroundTable{margin:0 auto;padding:0;width:100%!important}table td{border-collapse:collapse}.ExternalClass *{line-height:115%}.container-for-gmail-android{min-width:600px}*{font-family:Helvetica,Arial,sans-serif}body{-webkit-font-smoothing:antialiased;-webkit-text-size-adjust:none;width:100%!important;margin:0!important;height:100%;color:#676767}td{font-family:Helvetica,Arial,sans-serif;font-size:14px;color:#777;text-align:center;line-height:21px}a{color:#676767;text-decoration:none!important}.pull-left{text-align:left}.pull-right{text-align:right}.header-lg,.header-md,.header-sm{font-size:32px;font-weight:700;line-height:normal;padding:35px 0 0;color:#4d4d4d}.header-md{font-size:24px}.header-sm{padding:5px 0;font-size:18px;line-height:1.3}.content-padding{padding:20px 0 5px}.mobile-header-padding-right{width:290px;text-align:right;padding-left:10px}.mobile-header-padding-left{width:290px;text-align:left;padding-left:10px}.free-text{width:100%!important;padding:10px 60px 0}.button{padding:30px 0}.mini-block{border:1px solid #e5e5e5;border-radius:5px;background-color:#fff;padding:12px 15px 15px;text-align:left;width:253px}.mini-container-left{width:278px;padding:10px 0 10px 15px}.mini-container-right{width:278px;padding:10px 14px 10px 15px}.product{text-align:left;vertical-align:top;width:175px}.total-space{padding-bottom:8px;display:inline-block}.item-table{padding:50px 20px;width:560px}.item{width:300px}.mobile-hide-img{text-align:left;width:125px}.mobile-hide-img img{border:1px solid #e6e6e6;border-radius:4px}.title-dark{border-bottom:1px solid #ccc;color:#4d4d4d;font-weight:700;padding-bottom:5px}.item-col{padding-top:20px;vertical-align:top}.force-width-gmail{min-width:600px;height:0!important;line-height:1px!important;font-size:1px!important}</style><style media="screen">@import url(http://fonts.googleapis.com/css?family=Oxygen:400,700);</style><style media="screen">@media screen{*{font-family:Oxygen,"Helvetica Neue",Arial,sans-serif!important}}</style><style media="only screen and (max-width:480px)">@media only screen and (max-width:480px){table[class*=container-for-gmail-android]{min-width:290px!important;width:100%!important}img[class=force-width-gmail]{display:none!important;width:0!important;height:0!important}table[class=w320]{width:320px!important}td[class*=mobile-header-padding-left]{width:160px!important;padding-left:0!important}td[class*=mobile-header-padding-right]{width:160px!important;padding-right:0!important}td[class=header-lg]{font-size:24px!important;padding-bottom:5px!important}td[class=content-padding]{padding:5px 0 5px!important}td[class=button]{padding:5px 5px 30px!important}td[class*=free-text]{padding:10px 18px 30px!important}td[class~=mobile-hide-img]{display:none!important;height:0!important;width:0!important;line-height:0!important}td[class~=item]{width:140px!important;vertical-align:top!important}td[class~=quantity]{width:50px!important}td[class~=price]{width:90px!important}td[class=item-table]{padding:30px 20px!important}td[class=mini-container-left],td[class=mini-container-right]{padding:0 15px 15px!important;display:block!important;width:290px!important}}</style></head><body bgcolor="#f7f7f7"><table cellpadding="0" cellspacing="0" width="100%" class="container-for-gmail-android" align="center"><tbody><tr><td class="content-padding" style="background-color:#3BCDB0" valign="top" width="100%" align="center"><center><table cellpadding="0" cellspacing="0" width="600" class="w320"><tbody><tr><td class="w320"><table cellpadding="0" cellspacing="0" width="100%"><tbody><tr><td class="mini-container-left"><table cellpadding="0" cellspacing="0" width="100%"><tbody><tr><td class="mini-block-padding"><table cellpadding="0" cellspacing="0" width="100%" style="border-collapse:separate!important"><tbody><tr><td> <img src="http://auragoa.com/wp-content/uploads/2017/01/aura-goa-logofinal.png"></td></tr></tbody></table></td></tr></tbody></table></td><td class="mini-container-right"><table cellpadding="0" cellspacing="0" width="100%"><tbody><tr><td class="mini-block-padding"><table cellpadding="0" cellspacing="0" width="100%" style="border-collapse:separate!important"><tbody><tr><td class="item-col quantity" style="text-align:center;color:black"> <span class="total-space" style="font-weight:700;color:#4d4d4d">Aura Goa Wellness Resort </span> <span class="total-space" style="color:#4d4d4d">near R D khalp school, </span> <br> <span class="total-space" style="color:#4d4d4d">Mandrem, </span> <br> <span class="total-space" style="color:#4d4d4d">North Goa. </span> <br></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr><tr><td class="w320"><table cellpadding="0" cellspacing="0" width="100%"><tbody><tr><td class="mini-container-right"><table cellpadding="0" cellspacing="0" width="100%"><tbody><tr><td class="mini-block-padding"><table cellpadding="0" cellspacing="0" width="100%" style="border-collapse:separate!important"><tbody><tr><td> <b style="color: #C03B3C;font-weight: bolder;font-size:24px;">Payment Confirmation </b> <br> <lable style="color:#004D40"> Payment ID # : '+pay_id+' </lable></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></center></td></tr><tr><td style="background-color:#fff;border-top:1px solid #e5e5e5;border-bottom:1px solid #e5e5e5;padding:30px 0" valign="top" width="100%" align="center"><center>Hello <strong>'+fname+' '+lname+' </strong><p>Thank You for making your payment in <b>Aura Goa Wellness Resort </b></p><table cellpadding="0" cellspacing="0" width="600" class="w320"><tbody><tr></tr></tbody></table><table cellpadding="0" cellspacing="0" width="600" class="w320"><tbody><tr><td class="mini-block-padding"><table cellpadding="0" cellspacing="0" width="100%" style="border-collapse:separate!important"><tbody><tr><td class="mini-block" style="line-height: 2;"> <b>Your Payment Description </b> <br> <lable>Payment Amount : Rs. '+amount+' </lable> <br> <lable>Discount: Rs. '+discount+' </lable> <br> <lable>Total Payble Amount: Rs. '+total+' </lable> <br> <lable>Amount Paid: Rs. '+total+' </lable> <br> <lable>Description :<p>'+description+'</p> </lable></td></tr></tbody></table></td></tr></tbody></table></center></td></tr><tr><td style="background-color:#344B61;height:100px;padding:20px" valign="top" width="100%" align="center"><center><table cellpadding="0" cellspacing="0" width="600" class="w320"><tbody><tr><td class="fullCenter" style="text-align:center;font-family:Helvetica,Arial,sans-serif;font-size:12px;color:white;line-height:15px;font-weight:400;padding-left:30px;line-height:2" valign="middle" width="200px">Aura Goa Wellness Resort, Mandrem, North Goa <br>+91 76653-22222 <br> <a style="text-decoration:none;color:white">info@auragoa.com </a> <br> <a href="http://auragoa.com/" style="text-decoration:none;color:white">auragoa.com </a></td><td class="mobile-header-padding-right pull-right"> <a href="https://twitter.com/aurasparetreat"> <img src="http://s3.amazonaws.com/swu-filepicker/k8D8A7SLRuetZspHxsJk_social_08.gif" alt="twitter" height="47" width="44"> </a> <a href="https://www.facebook.com/aurasparetreat"> <img src="http://s3.amazonaws.com/swu-filepicker/LMPMj7JSRoCWypAvzaN3_social_09.gif" alt="facebook" height="47" width="38"> </a></td></tr></tbody></table></center></td></tr></tbody></table></body></html>'
				#send_mail('Payment Summary', 'Someone Just Logined from your Account if that was not you then Contact to Admin. Logined at '+str(timezone.now())+' Time ', 'Auragoa <donotreply@auragoa.com>', [email], html_message=html_content, fail_silently=False)

				sender = 'donotreply@auragoa.com'
				receiver = email
				subject = 'Payment_Summary'
				body = html_content
				purpose = 'Payment'
				Email_cron.objects.create(email_uid_id = user.id, email_from=sender, email_to=receiver, email_subject=subject, email_body=body, email_purpose=purpose)



		else:
			raise Exception('Permission Denied')

		return bundle


	def alter_list_data_to_serialize(self, request, data):
		total_amount = 0.0
		for i in data[ 'objects' ]:
			total_amount += i.data[ 'payment_total' ]

		return { 'meta' : data[ 'meta' ], 'objects' : data[ 'objects' ], 'total_amount' : total_amount }

	def hydrate(self, bundle):
		request = get_current_request()
		emp = bundle.request.GET['username']
		emp1 = User.objects.get(username = emp)
		t = int(emp1.id)
		
		if request.method == 'POST':
			bundle.data['payment_track'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['payment_utrack'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['payment_ueid'] = t
				
		elif request.method == 'PUT':
			bundle.data['payment_utrack'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['payment_utimestamp'] = timezone.now()
			bundle.data['payment_ueid'] = t
			
		return bundle


class FolioResource(ModelResource):
	folio_gid = fields.ForeignKey(GuestResource, 'folio_gid', full=True)
	folio_bid = fields.ForeignKey(BookingResource, 'folio_bid', full=True)
	
	class Meta:
		queryset = Folio.objects.all()
		resource_name = 'folio'
		allowed_methods = ['get', 'post']
		filtering = {
			'folio_gid': ALL_WITH_RELATIONS,
			'folio_bid': ALL_WITH_RELATIONS
		}
		limit = 0
		always_return_data = True
		authentication = AdminApiKeyAuthentication()
		authorization = Authorization()
		serializer = urlencodeSerializer()

	def obj_create(self, bundle, request=None, **kwargs):
		username = bundle.request.GET['username']
		user = User.objects.get(username=username)
		if user.has_perm('payment.add_folio'):
			bundle = super(FolioResource, self).obj_create(bundle)
		else:
			raise Exception('Permission Denied')

		return bundle

	def alter_list_data_to_serialize(self, request, data):
		total_amount = 0.0
		for i in data[ 'objects' ]:
			total_amount += i.data[ 'folio_total' ]

		return { 'meta' : data[ 'meta' ], 'objects' : data[ 'objects' ], 'total_amount' : total_amount }

	def hydrate(self, bundle):
		request = get_current_request()
		emp = bundle.request.GET['username']
		emp1 = User.objects.get(username = emp)
		t = int(emp1.id)
		
		if request.method == 'POST':
			bundle.data['folio_track'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['folio_utrack'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['folio_ueid'] = t		
		elif request.method == 'PUT':
			bundle.data['folio_utrack'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['folio_utimestamp'] = timezone.now()
			bundle.data['folio_ueid'] = t
			
		return bundle
'''
	def dehydrate(self, bundle):
		request = get_current_request()
		bundle.data['sum'] = Folio.objects.aggregate(Sum('folio_total'))

		return bundle
'''
