from django.contrib.admin import AdminSite
from django.utils.translation import ugettext_lazy

from .models import Assignment, CallAction, TextAction

class TransmissionAdmin(AdminSite):
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('Transmission Admin')

    # Text to put in each page's <h1> (and above login form).
    site_header = ugettext_lazy('Transmission Administration')

    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('Edit Assignments')

admin_site = TransmissionAdmin(name='assignments')

admin_site.register([Assignment, CallAction, TextAction])
