from django.contrib import admin

from dashboard.models import PointerStatus, Browser

# Register your models here.

admin.site.register(Browser)
admin.site.register(PointerStatus)
