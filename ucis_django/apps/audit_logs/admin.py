from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'performed_by', 'role', 'target_resource', 'target_id', 'ip_address', 'timestamp')
    list_filter = ('action', 'role', 'target_resource')
    search_fields = ('action', 'performed_by__username', 'target_resource', 'details')
    readonly_fields = ('timestamp',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
