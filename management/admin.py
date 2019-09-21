# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import Section, Staff

class SectionAdmin(admin.ModelAdmin):
      list_display = ('section_title','section_slug','section_description','section_timestamp','section_status')
      search_fields = ('section_title','section_slug','section_description','section_timestamp','section_status')
      list_per_page = 50 # No of records per page


class StaffAdmin(admin.ModelAdmin):
      list_display = ('staff_fname','staff_lname','staff_email','staff_mobile','staff_gender','staff_nationality','staff_status')
      search_fields = ('staff_fname','staff_lname','staff_email','staff_mobile','staff_gender','staff_nationality','staff_status')
      list_per_page = 50 # No of records per page

admin.site.register(Section,SectionAdmin)
admin.site.register(Staff,StaffAdmin)