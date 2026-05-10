from django.contrib import admin
from .models import JobOpportunity, JobApplication


class JobApplicationInline(admin.TabularInline):
    model = JobApplication
    extra = 0
    readonly_fields = ('applied_at',)


@admin.register(JobOpportunity)
class JobOpportunityAdmin(admin.ModelAdmin):
    inlines = [JobApplicationInline]
    list_display = ('title', 'company', 'job_type', 'industry', 'is_active', 'application_deadline', 'created_at')
    list_filter = ('job_type', 'industry', 'is_active')
    search_fields = ('title', 'company', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'job', 'status', 'applied_at')
    list_filter = ('status',)
    search_fields = ('applicant__username', 'job__title')
