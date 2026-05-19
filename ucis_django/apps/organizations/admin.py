from django.contrib import admin
from .models import StudentsOrganization, OrganizationMember


class OrganizationMemberInline(admin.TabularInline):
    model = OrganizationMember
    extra = 0
    readonly_fields = ('joined_at',)


@admin.register(StudentsOrganization)
class StudentsOrganizationAdmin(admin.ModelAdmin):
    inlines = [OrganizationMemberInline]
    list_display = ('org_name', 'status', 'contact_email', 'created_at')
    list_filter = ('status',)
    search_fields = ('org_name', 'description')
    readonly_fields = ('created_at',)


@admin.register(OrganizationMember)
class OrganizationMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'org', 'role', 'joined_at')
    list_filter = ('org',)
    search_fields = ('user__username', 'org__org_name', 'role')
    readonly_fields = ('joined_at',)
