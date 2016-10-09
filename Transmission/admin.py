from django.contrib import admin
from django.utils.translation import ugettext_lazy

from .models import Assignment, CallAction, TextAction


class TransmissionAdmin(admin.AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('Transmission Admin')
    # Text to put in each page's <h1> (and above login form).
    site_header = ugettext_lazy('Transmission Administration')
    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('Edit Assignments')
    site_url = None

admin_site = TransmissionAdmin(name='assignments')


@admin.register(CallAction, site=admin_site)
class CallActionAdmin(admin.ModelAdmin):
    list_display = ['name', 'call_script']
    search_fields = ['name', 'call_script']


@admin.register(TextAction, site=admin_site)
class TextActionAdmin(admin.ModelAdmin):
    list_display = ['name', 'message_content']
    search_fields = ['name', 'message_content']


@admin.register(Assignment, site=admin_site)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'expiration', 'expired', 'priority', 'active']
    list_filter = ['active', 'expiration', 'call_actions', 'text_actions']
    search_fields = ['name', 'description', 'instructions']
    fieldsets = [
        (None, {
            'fields': ['name', 'description', 'instructions']
        }),
        ('Actions', {
            'fields': [('call_actions', 'text_actions'), 'require_call_first'],
        }),
        ('Availability & Sorting', {
            'classes': ['collapse'],
            'fields': ['active', 'expiration', 'priority'],
        }),
    ]
