# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Spa_type, Equipment, Spa, Service, Service_history

admin.site.register(Spa_type)
admin.site.register(Equipment)
admin.site.register(Spa)
admin.site.register(Service)
admin.site.register(Service_history)
