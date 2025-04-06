from django.contrib import admin
from .models import (
    Client,
    ServiceCompany,
    Manager,
    ReferenceItem,
    Vehicle,
    TechnicalService,
    Complaint
)
from .utils.roles import get_user_role

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    search_fields = ('name', 'user__username')

@admin.register(ServiceCompany)
class ServiceCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', 'user__username')

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    search_fields = ('name', 'user__username')

@admin.register(ReferenceItem)
class ReferenceItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'description')
    list_filter = ('type',)
    search_fields = ('name', 'description')

    def has_change_permission(self, request, obj=None):
        return get_user_role(request.user) == "manager"

    def has_add_permission(self, request):
        return get_user_role(request.user) == "manager"

    def has_delete_permission(self, request, obj=None):
        return get_user_role(request.user) == "manager"

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        'serial_number',
        'tech_model',
        'engine_model',
        'serial_engine',
        'model_transmission',
        'serial_transmission',
        'model_axle',
        'model_man_axle',
        'client',
        'service_company',
        'ship_date',
    )
    list_filter = ('ship_date', 'client', 'service_company')
    search_fields = (
        'serial_number',
        'serial_engine',
        'serial_transmission',
        'serial_axle',
        'serial_man_axle',
        'client__name',
        'service_company__name',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        role = get_user_role(request.user)

        if role == "client":
            return qs.filter(client__user=request.user)
        elif role == "service":
            return qs.filter(service_company__user=request.user)
        elif role == "manager":
            return qs
        return qs.none()

@admin.register(TechnicalService)
class TechnicalServiceAdmin(admin.ModelAdmin):
    list_display = (
        'service_type',
        'service_date',
        'operating_hours',
        'order_number',
        'order_date',
        'vehicle',
        'tech_company',
    )
    list_filter = ('service_date', 'order_date', 'tech_company', 'vehicle')
    search_fields = (
        'order_number',
        'vehicle__serial_number',
        'tech_company__name',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        role = get_user_role(request.user)

        if role == "client":
            return qs.filter(vehicle__client__user=request.user)
        elif role == "service":
            return qs.filter(service_company__user=request.user)
        elif role == "manager":
            return qs
        return qs.none()

    def has_change_permission(self, request, obj=None):
        role = get_user_role(request.user)
        return role in ["manager", "service"]

    def has_add_permission(self, request):
        role = get_user_role(request.user)
        return role in ["manager", "service"]

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = (
        'failure_date',
        'operating_hours',
        'failure_node',
        'recovery_method',
        'recovery_date',
        'vehicle',
    )
    list_filter = ('failure_date', 'recovery_date', 'vehicle')
    search_fields = (
        'vehicle__serial_number',
        'failure_node__name',
        'recovery_method__name',
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        role = get_user_role(request.user)

        if role == "client":
            return qs.filter(vehicle__client__user=request.user)
        elif role == "service":
            return qs.filter(vehicle__service_company__user=request.user)
        elif role == "manager":
            return qs
        return qs.none()

    def has_change_permission(self, request, obj=None):
        return get_user_role(request.user) in ["manager", "service"]

    def has_add_permission(self, request):
        return get_user_role(request.user) in ["manager", "service"]