from django.contrib import admin

from .models import ReportRequest


@admin.register(ReportRequest)
class ReportRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_kind', 'created_at')
    search_fields = ('title', 'report_kind')