from django.contrib import admin
from models import CaughtError


class CaughtErrorAdmin(admin.ModelAdmin):
    readonly_fields = ("user",)
    list_display = ('user', 'exception_type',"page_url", "error_time", "user_notes")
    search_fields = ('exception_type', 'page_url',)
    list_filter = ("error_time",)


admin.site.register(CaughtError, CaughtErrorAdmin)
