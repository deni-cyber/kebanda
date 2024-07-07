from django.contrib import admin
from . models import Vendor, Shop, Item
# Register your models here.
admin.site.register(Vendor)
admin.site.register(Shop)
admin.site.register(Item)