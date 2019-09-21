from tastypie.authorization import Authorization
from tastypie import fields
from django.db import models
from django.contrib.auth.models import User
from tastypie.resources import ModelResource,ALL, ALL_WITH_RELATIONS
from .models import Category,Menu,Cuisine,Table,Order,Order_history
from jakhar.api import urlencodeSerializer, AdminApiKeyAuthentication, UserResource
from tastypie.authorization import DjangoAuthorization, ReadOnlyAuthorization, Authorization
from Guest.api import GuestResource
from booking.api import BookingResource
from crum import get_current_request

from django.db.models import Sum
from django.utils import timezone
#from models import sum
#from django.db.models import *


class CategoryResource(ModelResource):
	class Meta:
		queryset = Category.objects.all()
		resource_name = 'category'
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

	# def dehydrate(self, bundle):
	# 	bundle.data['sum'] = 5000

	# 	return bundle


class MenuResource(ModelResource):
	menu_ctid = fields.ForeignKey(CategoryResource, 'menu_ctid', full=True)
	
	class Meta:
		queryset = Menu.objects.all()
		resource_name = 'menu'
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


class CuisineResource(ModelResource):
	cuisine_mid = fields.ForeignKey(MenuResource, 'cuisine_mid', full=True)
	
	class Meta:
		queryset = Cuisine.objects.all()
		resource_name = 'cuisine'
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


class TableResource(ModelResource):
	
	class Meta:
		queryset = Table.objects.all()
		resource_name = 'table'
		allowed_methods = ['get','put']
		# filtering = {
		# 	'folio_gid': ALL_WITH_RELATIONS,
		# 	'folio_bid': ALL_WITH_RELATIONS
		# }
		limit = 0
		always_return_data = True
		authentication = AdminApiKeyAuthentication()
		authorization = Authorization()
		serializer = urlencodeSerializer()


class OrderResource(ModelResource):
	order_uid = fields.ForeignKey(UserResource, 'order_uid', full=True)
	order_cuid = fields.ForeignKey(CuisineResource, 'order_cuid', full=True)
	order_tid = fields.ForeignKey(TableResource, 'order_tid', full=True, null=True, blank=True)
	order_gid = fields.ForeignKey(GuestResource, 'order_gid', full=True, null=True, blank=True)
	order_bid = fields.ForeignKey(BookingResource, 'order_bid', full=True, null=True, blank=True)
	
	class Meta:
		queryset = Order.objects.all()
		resource_name = 'order'
		allowed_methods = ['get', 'post', 'put']
		filtering = {
			'order_gid': ALL_WITH_RELATIONS,
			'order_bid': ALL_WITH_RELATIONS,
			'order_timestamp': ALL
		}
		limit = 0
		always_return_data = True
		authentication = AdminApiKeyAuthentication()
		authorization = Authorization()
		serializer = urlencodeSerializer()

	def obj_create(self, bundle, request=None, **kwargs):
		username = bundle.request.GET['username']
		user = User.objects.get(username=username)
		if user.has_perm('restaurant.add_order'):  #permission checking during post
			bundle = super(OrderResource, self).obj_create(bundle)
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
			bundle.data['order_track'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['order_utrack'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['order_ueid'] = t		
		elif request.method == 'PUT':
			bundle.data['order_utrack'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['order_utimestamp'] = timezone.now()
			bundle.data['order_ueid'] = t
			
		return bundle

class Order_historyResource(ModelResource):
	
	orderh_uid = fields.ForeignKey(UserResource, 'orderh_uid', full=True)
	orderh_tid = fields.ForeignKey(TableResource, 'orderh_tid', full=True, null=True, blank=True)
	orderh_gid = fields.ForeignKey(GuestResource, 'orderh_gid', full=True, null=True, blank=True)
	orderh_bid = fields.ForeignKey(BookingResource, 'orderh_bid', full=True, null=True, blank=True)
	class Meta:
		queryset = Order_history.objects.all()
		resource_name = 'order_history'
		allowed_methods = ['get', 'post', 'put']
		filtering = { 'orderh_timestamp': ALL }
		limit = 0
		always_return_data = True
		authentication = AdminApiKeyAuthentication()
		authorization = Authorization()
		serializer = urlencodeSerializer()

	def obj_create(self, bundle, request=None, **kwargs):
		username = bundle.request.GET['username']
		user = User.objects.get(username=username)
		if user.has_perm('restaurant.add_order_history'):  #permission checking during post
			bundle = super(Order_historyResource, self).obj_create(bundle)
			bundle.obj.save()
			
		else:
			raise Exception('Permission Denied')

		return bundle

	def dehydrate(self, bundle):
		#x = bundle.data.get['orderh_oid']
		x = bundle.obj.orderh_oid
		y = x.split(',')
		#bundle.data['order_count'] = len(y)
		
		n = 0
		shyam = {}
		for i in y:
			if i:
				j = Order.objects.get(order_id = i)
				shyam[n] = {'order_bid':j.order_bid, 'order_unit':j.order_unit, 'order_cuid':{'cuisine_description':j.order_cuid.cuisine_description, 'cuisine_id':j.order_cuid.cuisine_id, 'cuisine_mid':j.order_cuid.cuisine_mid, 'cuisine_slug':j.order_cuid.cuisine_slug, 'cuisine_special':j.order_cuid.cuisine_special, 'cuisine_status':j.order_cuid.cuisine_status, 'cuisine_timestamp':j.order_cuid.cuisine_timestamp, 'cuisine_title':j.order_cuid.cuisine_title, 'cuisine_track':j.order_cuid.cuisine_track, 'cuisine_ueid':j.order_cuid.cuisine_ueid, 'cuisine_utimestamp':j.order_cuid.cuisine_utimestamp, 'cuisine_utrack':j.order_cuid.cuisine_utrack, 'cuisine_discount':j.order_cuid.cuisines_discount, 'cuisine_extra':j.order_cuid.cuisines_extra, 'cuisine_price':j.order_cuid.cuisines_price, 'cuisine_tax':j.order_cuid.cuisines_tax}, 'order_customer':j.order_customer, 'order_discount':j.order_discount, 'order_extra':j.order_extra, 'order_from':j.order_from, 'order_gid':j.order_gid, 'order_id':j.order_id, 'order_price':j.order_price, 'order_status':j.order_status, 'order_tax':j.order_tax, 'order_tid':j.order_tid, 'order_timestamp':j.order_timestamp, 'order_total':j.order_total, 'order_track':j.order_track, 'order_ueid':j.order_ueid, 'order_uid':j.order_uid, 'order_utimestamp':j.order_utimestamp, 'order_utrack':j.order_utrack}
				bundle.data['orders'] = shyam
				n = n + 1
		bundle.data['order_count'] = n
		return bundle

	def hydrate(self, bundle):
		request = get_current_request()
		emp = bundle.request.GET['username']
		emp1 = User.objects.get(username = emp)
		t = int(emp1.id)
		
		if request.method == 'POST':
			bundle.data['orderh_track'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['orderh_utrack'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['orderh_ueid'] = t		
		elif request.method == 'PUT':
			bundle.data['orderh_utrack'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['orderh_utimestamp'] = timezone.now()
			bundle.data['orderh_ueid'] = t
			
		return bundle

