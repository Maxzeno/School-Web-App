from django.contrib import admin
from django.utils.html import format_html
from .models import User 

# Register your models here.

admin.site.site_title = 'CDSSE Admin'

admin.site.index_title = 'Welcome to CDSSE'
# admin.site.enable_nav_sidebar = False
admin.site.site_header = format_html('<a href="/adminuser/admin/"><img src="/static/images/logo.png" style="height: 100px"></a>')

admin.site.register(User)
