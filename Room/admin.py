# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Room
from .models import Room_type

class RoomAdmin(admin.ModelAdmin):
      list_display = ('room_number','room_title','user_name','room_amount','room_timestamp','room_condition','room_status')
      search_fields = ('room_number','room_title','user_name','room_amount','room_timestamp','room_condition','room_status')
      list_per_page = 50 # No of records per page
      
      def user_name(self, obj):
        return obj.room_uid.first_name+" "+obj.room_uid.last_name
      
      user_name.admin_order_field  = 'user_id'  #Allows column order sorting
      user_name.short_description = 'User Name'  #Renames column head



admin.site.register(Room,RoomAdmin)
admin.site.register(Room_type)