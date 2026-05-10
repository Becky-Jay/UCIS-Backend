from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, Education, WorkExperience, Expertise, Achievement, Relationship, StudentEngagement, AlumniEngagement, SystemAdminEngagement, CollegeAdminEngagement


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class StudentEngagementInline(admin.StackedInline):
    model = StudentEngagement
    can_delete = False
    extra = 0


class AlumniEngagementInline(admin.StackedInline):
    model = AlumniEngagement
    can_delete = False
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline, StudentEngagementInline, AlumniEngagementInline]
    list_display = ('username', 'email', 'role', 'college', 'is_active', 'last_active')
    list_filter = ('role', 'college', 'is_active')
    search_fields = ('username', 'email')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('UCIS Info', {'fields': ('role', 'college', 'fcm_tokens')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('UCIS Info', {'fields': ('role', 'college')}),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'department', 'phone')
    search_fields = ('first_name', 'last_name', 'user__username')


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('user', 'degree_course', 'college', 'start_year', 'end_year')


@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'job_title', 'industry', 'current')


@admin.register(Expertise)
class ExpertiseAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'proficiency')


@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'relationship_type')
