from django.contrib import admin
from .models import *

admin.site.site_header='Phone Repair Admin Dashboard'

def received(modeladmin, request, queryset):
    queryset.update(status='sub')

def started(modeladmin, request, queryset):
    queryset.update(status='sta')

def completed(modeladmin, request, queryset):
    queryset.update(status='comp')

class OrderAdmin(admin.ModelAdmin):
    list_display=('first_name', 'date_brought','status')
    list_filter=('date_brought',)
    actions=[received,started,completed]

admin.site.register(Order,OrderAdmin)


def received(modeladmin, request, queryset):
    queryset.update(status='ava')

def started(modeladmin, request, queryset):
    queryset.update(status='rec')

def completed(modeladmin, request, queryset):
    queryset.update(status='nav')

class SparepartsAdmin(admin.ModelAdmin):
    list_display=('first_name', 'spare','phone_model', 'status')
    list_filter=['spare','phone_model']
    #actions=[received, available , not_available]
    actions_on_top=True

admin.site.register(Spareparts, SparepartsAdmin)



admin.site.register(Payment)