# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Country, State

class CountryAdmin(admin.ModelAdmin):
      list_display = ('country_title', 'country_code', 'country_iso')
      search_fields = ('country_title', 'country_code', 'country_iso')

class StateAdmin(admin.ModelAdmin):
      list_display = ('state_title', 'country_name')
      search_fields = ('state_title', 'country_name')

      def country_name(self, obj):
        return obj.state_ctid.country_title




admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)

