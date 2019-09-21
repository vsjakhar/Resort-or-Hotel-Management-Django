# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Guest, gwork, gother

class GuestAdmin(admin.ModelAdmin):
      list_display = ('guest_fname','guest_lname','guest_email','guest_mobile','guest_gender')
      search_fields = ('guest_fname', 'guest_lname', 'guest_email','guest_mobile','guest_gender' )
      list_per_page = 50 # No of records per page

class GworkAdmin(admin.ModelAdmin):
      list_display = ('gwork_gid','gwork_organization','gwork_mobile','gwork_email')
      search_fields = ('gwork_gid', 'gwork_organization', 'gwork_mobile','gwork_email')
      list_per_page = 50 # No of records per page

class GotherAdmin(admin.ModelAdmin):
      list_display = ('gother_gid','gother_preferences','gother_spouse_title','gother_spouse_fname','gother_spouse_lname','gother_birthday')
      search_fields = ('gother_gid', 'gother_preferences', 'gother_spouse_title','gother_spouse_fname','gother_spouse_lname','gother_birthday')
      list_per_page = 50 # No of records per page

admin.site.register(Guest,GuestAdmin)
admin.site.register(gwork)
admin.site.register(gother)

