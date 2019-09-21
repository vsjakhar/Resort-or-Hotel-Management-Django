from django.contrib.auth.models import User
from tastypie.authorization import Authorization
from tastypie import fields
from tastypie.resources import ModelResource
from jakhar.api import urlencodeSerializer, AdminApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization, ReadOnlyAuthorization, Authorization

from .models import Room_type, Room
from management.api import StaffResource
from crum import get_current_request
from django.utils import timezone
import ast


class Room_typeResource(ModelResource):
    
    class Meta:
        queryset = Room_type.objects.all()
        resource_name = 'room_type'
        authorization = Authorization()
        
class RoomResource(ModelResource):
	room_sid = fields.ForeignKey(StaffResource, 'room_sid', full=True, blank=True, null=True)
	room_type_id = fields.ForeignKey(Room_typeResource, 'room_type_id', full=True)
	class Meta:
		queryset = Room.objects.all()
		resource_name = 'room'
		limit = 0
		always_return_data = True
		authentication = AdminApiKeyAuthentication()
		authorization = Authorization()
		serializer = urlencodeSerializer()

	def hydrate(self, bundle):
		request = get_current_request()
		if request.method == 'POST':
			bundle.data['room_track'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['room_utrack'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['room_timestamp'] = timezone.now()
			bundle.data['room_utimestamp'] = timezone.now()

		if request.method == 'PUT':
			bundle.data['room_utrack'] = request.META['REMOTE_ADDR'] + ',' + request.user_agent.browser.family + ',' + request.user_agent.os.family + ',' + request.user_agent.device.family
			bundle.data['room_utimestamp'] = timezone.now()
			ram = bundle.obj.room_sid
			
			if ram:
				if bundle.obj.room_history:
					history = ast.literal_eval(bundle.obj.room_history)
					history.append((int(bundle.obj.room_sid.staff_id), str(bundle.obj.room_condition), str(bundle.obj.room_sid.staff_fname)))

					if len(history) == 11:
						del history[0]
					bundle.data['room_history'] = history
				else:
					bundle.data['room_history'] = [(int(bundle.obj.room_sid.staff_id), str(bundle.obj.room_condition), str(bundle.obj.room_sid.staff_fname))]

		return bundle


class Room_detailResource(ModelResource):
	class Meta:
		queryset = Room_type.objects.all()
		resource_name = 'room_detail'
		authorization = Authorization()

	def dehydrate(self, bundle):
		
		room = Room.objects.filter(room_type_id__room_type_id=bundle.obj.room_type_id)
		bundle.data['room_count'] = room.count()
		shyam = {}
		a=0

		for i in room:
			shyam[a] = {'room_amount':i.room_amount, 'room_condition':i.room_condition, 'room_id':i.room_id, 'room_number':i.room_number, 'room_slug':i.room_slug, 'room_status':i.room_status, 'room_timestamp':i.room_timestamp, 'room_title':i.room_title, 'room_track':i.room_track, 'room_type':i.room_type, 'room_utimestamp':i.room_utimestamp, 'room_utrack':i.room_utrack}
			bundle.data['rooms'] = shyam
			a+=1
		
		return bundle