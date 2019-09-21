# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import Category, Menu, Cuisine, Table, Order, Order_history

class CategoryAdmin(admin.ModelAdmin):
      list_display = ('category_title','category_slug','category_description','category_timestamp','category_status')
      search_fields = ('category_title','category_slug','category_description','category_timestamp','category_status')
      list_per_page = 50 # No of records per page

class MenuAdmin(admin.ModelAdmin):
      list_display = ('menu_title','menu_slug','rcat','menu_special','menu_description','menu_timestamp','menu_status')
      search_fields = ('menu_title','menu_slug','rcat','menu_special','menu_description','menu_timestamp','menu_status')
      list_per_page = 50 # No of records per page

      def rcat(self, obj):
        return obj.menu_ctid.category_title
      
      rcat.admin_order_field  = 'menu_ctid'  #Allows column order sorting
      rcat.short_description = 'Category'  #Renames column head

class CuisineAdmin(admin.ModelAdmin):
      list_display = ('cuisine_title','cuisine_slug','menu','cuisine_special','cuisines_extra','cuisine_description','cuisines_price','cuisines_tax','cuisine_status')
      search_fields = ('cuisine_title','cuisine_slug','menu','cuisine_special','cuisines_extra','cuisine_description','cuisines_price','cuisines_tax','cuisine_status')
      list_per_page = 50 # No of records per page

      def menu(self, obj):
        return obj.cuisine_mid.menu_title
      
      menu.admin_order_field  = 'cuisine_mid'  #Allows column order sorting
      menu.short_description = 'Menu'  #Renames column head

class TableAdmin(admin.ModelAdmin):
      list_display = ('table_no','table_capacity','table_description','table_smoking','table_liquor','table_status')
      search_fields = ('table_no','table_capacity','table_description','table_smoking','table_liquor','table_status')
      list_per_page = 50 # No of records per page

class OrderAdmin(admin.ModelAdmin):
      list_display = ('cuisine','order_customer','order_price','order_discount','order_tax','order_total','order_extra','order_from','order_timestamp','order_status')
      search_fields = ('cuisine','order_customer','order_price','order_discount','order_tax','order_total','order_extra','order_from','order_timestamp','order_status')
      list_per_page = 50 # No of records per page
      
      # def room_name(self, obj):
      #   return obj.booking_rid.room_title

      def cuisine(self, obj):
        return obj.order_cuid.cuisine_title

      # def table(self, obj):
      #   return obj.order_tid.table_no
      
      cuisine.admin_order_field  = 'order_cuid'  #Allows column order sorting
      cuisine.short_description = 'Cuisine'  #Renames column head

class Order_historyAdmin(admin.ModelAdmin):
      list_display = ('orderh_id','orderh_cuisines','orderh_prices','orderh_units','orderh_total','orderh_from')
      search_fields = ('orderh_id','orderh_cuisines','orderh_prices','orderh_units','orderh_total','orderh_from')
      list_per_page = 50 # No of records per page


admin.site.register(Category,CategoryAdmin)
admin.site.register(Menu,MenuAdmin)
admin.site.register(Cuisine,CuisineAdmin)
admin.site.register(Table,TableAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Order_history,Order_historyAdmin)
