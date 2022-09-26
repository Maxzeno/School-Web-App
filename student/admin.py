from django.contrib import admin

# Register your models here.

from .models import Student, Parent, Subject, Class, JustClass, Exam, Session

admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Subject)
admin.site.register(Class)
admin.site.register(JustClass)
admin.site.register(Exam)
admin.site.register(Session)
