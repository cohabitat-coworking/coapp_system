# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from models import *

# Register your models here.

admin.site.register(Coworking)
admin.site.register(UserAddress)
admin.site.register(GenericAddress)
admin.site.register(Profile)
admin.site.register(ContactType)
admin.site.register(ContactInfo)
admin.site.register(ProfileJuridic)
admin.site.register(Plan)
admin.site.register(Resource)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(ImageRoom)
admin.site.register(ItemType)
admin.site.register(Item)
admin.site.register(PlanItem)
admin.site.register(PlanResource)
admin.site.register(ImageResource)
admin.site.register(PlanRoom)
admin.site.register(Agenda)
admin.site.register(AgendaItem)
admin.site.register(AgendaResource)
admin.site.register(AgendaRoom)
admin.site.register(ItemUnity)
admin.site.register(ImageItem)
admin.site.register(Contract)
admin.site.register(AgendaContracts)
admin.site.register(JuridicProfileDocument)
admin.site.register(UserHasPlan)
