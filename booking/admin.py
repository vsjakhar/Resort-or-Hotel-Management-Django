# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Source, Booking, Travel
from Guest.models import Guest
#from daterange_filter.filter import DateRangeFilter

class BookingAdmin(admin.ModelAdmin):
      list_display = ('get_name','room_name','booking_amount','booking_arrival','booking_departure','booking_messages')
      search_fields = ('get_name','room_name','booking_amount','booking_arrival','booking_departure','booking_messages')
      #list_filter = ('booking_amount', ('booking_arrival', DateRangeFilter), ('booking_departure', DateRangeFilter))
      list_per_page = 50 # No of records per page
      
      def room_name(self, obj):
        return obj.booking_rid.room_number
        
      def get_name(self, obj):
        return obj.booking_gid.guest_fname+" "+obj.booking_gid.guest_lname
      
      get_name.admin_order_field  = 'booking_gid'  #Allows column order sorting
      get_name.short_description = 'Guest Name'  #Renames column head


admin.site.register(Source)
admin.site.register(Booking,BookingAdmin)
admin.site.register(Travel)
