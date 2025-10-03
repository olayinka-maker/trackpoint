from django.contrib import admin
from .models import Department, Staff, AssetType, Asset


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'position', 'hire_date', 'email']
    list_filter = ['department', 'hire_date']
    search_fields = [
        'user__username', 'user__first_name', 'user__last_name', 'position'
    ]


@admin.register(AssetType)
class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'color']


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'asset_type', 'department', 'assigned_to', 'status',
        'purchase_date', 'location'
    ]
    list_filter = ['asset_type', 'department', 'status', 'purchase_date']
    search_fields = ['name', 'serial_number']
    date_hierarchy = 'purchase_date'
