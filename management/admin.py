from django.contrib import admin
from django.utils.html import format_html
from .models import User 
from semiadmin.models import SemiAdmin 
from teacher.models import Teacher 
from student.models import Student 

# Register your models here.

admin.site.site_title = 'CDSSE Admin'

admin.site.index_title = 'Welcome to CDSSE'
# admin.site.enable_nav_sidebar = False
admin.site.site_header = format_html('<a href="/adminuser/admin/"><img src="/static/images/logo.png" style="height: 100px"></a>')

# admin.site.register(User)



class SemiAdminAdminInline(admin.TabularInline):
    extra = 0
    model = SemiAdmin

class TeacherAdminInline(admin.TabularInline):
    extra = 0
    model = Teacher

class StudentAdminInline(admin.TabularInline):
    extra = 0
    model = Student

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [SemiAdminAdminInline, TeacherAdminInline, StudentAdminInline]
