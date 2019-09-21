from tastypie.authorization import Authorization
from tastypie import fields
from django.db import models
from django.contrib.auth.models import User
from tastypie.resources import ModelResource,ALL, ALL_WITH_RELATIONS
from .models import Spa_type, Equipment, Spa, Service, Service_history
from jakhar.api import urlencodeSerializer, AdminApiKeyAuthentication, UserResource
from tastypie.authorization import DjangoAuthorization, ReadOnlyAuthorization, Authorization
from Guest.api import GuestResource
from booking.api import BookingResource
from crum import get_current_request

from django.db.models import Sum
from django.utils import timezone
#from models import sum
#from django.db.models import *


class Spa_typeResource(ModelResource):
	class Meta:
		queryset = Spa_type.objects.all()
		resource_name = 'spa_type'
		allowed_methods = ['get']
		# filtering = {
		# 	'payment_gid': ALL_WITH_RELATIONS,
		# 	'payment_bid': ALL_WITH_RELATIONS
		# }
		limit = 0
		always_return_data = True
		authentication = AdminApiKeyAuthentication()
		authorization = Authorization()
		serializer = urlencodeSerializer()


class EquipmentResource(ModelResource):
	#menu_ctid = fields.ForeignKey(CategoryResource, 'menu_ctid', full=True)
	
	class Meta:
		queryset = Equipment.objects.all()
		resource_name = 'equipment'
		allowed_methods = ['get']
		# filtering = {
		# 	'folio_gid': ALL_WITH_RELATIONS,
		# 	'folio_bid': ALL_WITH_RELATIONS
		# }
		limit = 0
		always_return_data = True
		authentication = AdminApiKeyAuthentication()
		authorization = Authorization()
		serializer = urlencodeSerializer()


class SpaResource(ModelResource):
	#cuisine_mid = fields.ForeignKey(MenuResource, 'cuisine_mid', full=True)
	spa_stid = fields.ForeignKey(Spa_typeResource, 'spa_stid', full=True)
	class Meta:
		queryset = Spa.objects.all()
		resource_name = 'spa'
		allowed_methods = ['get']
		# filtering = {
		# 	'folio_gid': ALL_WITH_RELATIONS,
		# 	'folio_bid': ALL_WITH_RELATIONS
		# }
		limit = 0
		always_return_data = True
		authentication = AdminApiKeyAuthentication()
		authorization = Authorization()
		serializer = urlencodeSerializer()


class ServiceResource(ModelResource):
	service_uid = fields.ForeignKey(UserResource, 'service_uid', full=True)
	service_spid = fields.ForeignKey(SpaResource, 'service_spid', full=True)
	service_eid = fields.ForeignKey(EquipmentResource, 'service_eid', full=True, null=True, blank=True)
	service_gid = fields.ForeignKey(GuestResource, 'service_gid', full=True, null=True, blank=True)
	service_bid = fields.ForeignKey(BookingResource, 'service_bid', full=True, null=True, blank=True)
	
	class Meta:
		queryset = Service.objects.all()
		resource_name = 'service'
		allowed_methods = ['get', 'post', 'put']
		filtering = {
			'service_timestamp':ALL,
		}
		limit = 0
		always_return_data = True
		authentication = AdminApiKeyAuthentication()
		authorization = Authorization()
		serializer = urlencodeSerializer()



	def obj_create(self, bundle, request=None, **kwargs):
		username = bundle.request.GET['username']
		user = User.objects.get(username=username)
		if user.has_perm('spa.add_service'):  #permission checking during post
			bundle = super(ServiceResource, self).obj_create(bundle)
			bundle.obj.save()
			
		else:
			raise Exception('Permission Denied')

		return bundle

	def hydrate(self, bundle):
		request = get_current_request()
		emp = bundle.request.GET['username']
		emp1 = User.objects.get(username = emp)
		t = int(emp1.id)
		
		if request.method == 'POST':
			bundle.data['service_track'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['service_utrack'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['service_ueid'] = t		
		elif request.method == 'PUT':
			bundle.data['service_utrack'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['service_utimestamp'] = timezone.now()
			bundle.data['service_ueid'] = t
			
		return bundle


class Service_historyResource(ModelResource):
	serviceh_uid = fields.ForeignKey(UserResource, 'serviceh_uid', full=True)
	serviceh_eid = fields.ForeignKey(EquipmentResource, 'serviceh_eid', full=True)
	serviceh_gid = fields.ForeignKey(GuestResource, 'serviceh_gid', full=True, null=True, blank=True)
	serviceh_bid = fields.ForeignKey(BookingResource, 'serviceh_bid', full=True, null=True, blank=True)
	
	class Meta:
		queryset = Service_history.objects.all()
		resource_name = 'service_history'
		allowed_methods = ['get', 'post', 'put']
		#filtering = {'service_timestamp':ALL}
		limit = 0
		always_return_data = True
		authentication = AdminApiKeyAuthentication()
		authorization = Authorization()
		serializer = urlencodeSerializer()

	def obj_create(self, bundle, request=None, **kwargs):
		username = bundle.request.GET['username']
		user = User.objects.get(username=username)
		if user.has_perm('spa.add_service_history'):  #permission checking during post
			bundle = super(Service_historyResource, self).obj_create(bundle)
			bundle.obj.save()
			
		else:
			raise Exception('Permission Denied')

		return bundle

	def dehydrate(self, bundle):
		x = bundle.obj.serviceh_sid
		y = x.split(',')
		n = 0
		shyam = {}
		for i in y:
			if i:
				j = Service.objects.get(service_id = i)
				shyam[n] = {'service_bid':j.service_bid, 'service_uid':j.service_uid, 'service_spid':{'spa_id':j.service_spid.spa_id, 'spa_uid':j.service_spid.spa_uid, 'spa_stid':j.service_spid.spa_stid, 'spa_title':j.service_spid.spa_title, 'spa_slug':j.service_spid.spa_slug, 'spa_price':j.service_spid.spa_price, 'spa_discount':j.service_spid.spa_discount, 'spa_tax':j.service_spid.spa_tax, 'spa_special':j.service_spid.spa_special, 'spa_extra':j.service_spid.spa_extra, 'spa_description':j.service_spid.spa_description, 'spa_timestamp':j.service_spid.spa_timestamp, 'spa_utimestamp':j.service_spid.spa_utimestamp, 'spa_ueid':j.service_spid.spa_ueid, 'spa_track':j.service_spid.spa_track, 'spa_utrack':j.service_spid.spa_utrack, 'spa_status':j.service_spid.spa_status}, 'service_eid':j.service_eid, 'service_gid':j.service_gid, 'service_from':j.service_from, 'service_customer':j.service_customer, 'service_id':j.service_id, 'service_price':j.service_price, 'service_status':j.service_status, 'service_tax':j.service_tax, 'service_discount':j.service_discount, 'service_timestamp':j.service_timestamp, 'service_total':j.service_total, 'service_track':j.service_track, 'service_ueid':j.service_ueid, 'service_extra':j.service_extra, 'service_utimestamp':j.service_utimestamp, 'service_utrack':j.service_utrack}
				bundle.data['services'] = shyam
				n = n + 1
		bundle.data['service_count'] = n
		return bundle

	def hydrate(self, bundle):
		request = get_current_request()
		emp = bundle.request.GET['username']
		emp1 = User.objects.get(username = emp)
		t = int(emp1.id)
		
		if request.method == 'POST':
			bundle.data['serviceh_track'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['serviceh_utrack'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['serviceh_ueid'] = t		
		elif request.method == 'PUT':
			bundle.data['serviceh_utrack'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['serviceh_utimestamp'] = timezone.now()
			bundle.data['serviceh_ueid'] = t
			
		return bundle



