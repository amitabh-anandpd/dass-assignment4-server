from django.contrib import admin

from .models import Admin as AdminUser
from .models import Configuration, Student, SystemConfiguration, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active')
    search_fields = ('username', 'email')


@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active')
    search_fields = ('username', 'email')


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'currency', 'time_zone', 'language', 'updated_at')
    search_fields = ('user__username', 'country', 'currency', 'time_zone', 'language')


@admin.register(SystemConfiguration)
class SystemConfigurationAdmin(admin.ModelAdmin):
    list_display = ('grading_system', 'auto_unique_ids', 'unique_id_prefix', 'unique_id_padding', 'updated_at')
    search_fields = ('grading_system', 'unique_id_prefix', 'default_country', 'default_currency', 'default_time_zone', 'default_language')