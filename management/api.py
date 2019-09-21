from tastypie.authorization import Authorization
from tastypie import fields
from django.db import models
from tastypie.resources import ModelResource,ALL, ALL_WITH_RELATIONS
from .models import Staff
from jakhar.api import urlencodeSerializer, AdminApiKeyAuthentication, UserResource
from tastypie.authorization import DjangoAuthorization, ReadOnlyAuthorization, Authorization
from Guest.api import GuestResource
from crum import get_current_request

#from models import sum
#from django.db.models import *


class StaffResource(ModelResource):
	class Meta:
		queryset = Staff.objects.all()
		resource_name = 'staff'
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

	def hydrate(self, bundle):
		request = get_current_request()
		
		if request.method == 'POST':
			bundle.data['staff_track'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['staff_utrack'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
				
		elif request.method == 'PUT':
			bundle.data['staff_utrack'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['staff_utimestamp'] = timezone.now()
			
		return bundle