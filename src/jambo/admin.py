from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from .models import BusinessCategory, Business, Item, BusinessItem

admin.site.register(BusinessCategory)
admin.site.register(Business)
admin.site.register(Item)
admin.site.register(BusinessItem)