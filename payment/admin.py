# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Payment, Folio

class PaymentAdmin(admin.ModelAdmin):
      list_display = ('payment_mode','payment_total','payment_description','payment_receipt','payment_timestamp')
      search_fields = ('payment_mode','payment_total','payment_description','payment_receipt','payment_timestamp')
      list_per_page = 50 # No of records per page
      
      # def room_name(self, obj):
      #   return obj.booking_rid.room_title

      def room(self, obj):
        return obj.payment_bid.booking_rid.room_id

      def booking(self, obj):
        return obj.payment_bid.booking_id
        
      def get_name(self, obj):
        return obj.payment_gid.guest_fname+" "+obj.payment_gid.guest_lname
      
      get_name.admin_order_field  = 'payment_gid'  #Allows column order sorting
      get_name.short_description = 'Guest Name'  #Renames column head


class FolioAdmin(admin.ModelAdmin):
      list_display = ('get_name','booking','room','folio_from','folio_title','folio_unit','folio_price','folio_amount','folio_tax','folio_total','folio_timestamp')
      search_fields = ('booking','room','folio_from','folio_title','folio_unit','folio_price','folio_amount','folio_tax','folio_total','folio_timestamp')
      list_per_page = 50 # No of records per page
      
      # def room_name(self, obj):
      #   return obj.booking_rid.room_title

      def room(self, obj):
        return obj.folio_bid.booking_rid.room_id

      def booking(self, obj):
        return obj.folio_bid.booking_id
        
      def get_name(self, obj):
        return obj.folio_gid.guest_fname+" "+obj.folio_gid.guest_lname
      
      get_name.admin_order_field  = 'folio_gid'  #Allows column order sorting
      get_name.short_description = 'Guest Name'  #Renames column head


admin.site.register(Payment,PaymentAdmin)
admin.site.register(Folio,FolioAdmin)
