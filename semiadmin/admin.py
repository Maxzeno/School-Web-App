from django.contrib import admin
from .models import (
	SemiAdmin, SubjectPermission, SchoolSettings, MarkSheetFormat, Mark, Grade, BookIssue, Invoice,
	EventCalendar, StudentDomainScore, Routine, Syllabus, Attendance, Noticeboard, Promotion, Book,
	)

# Register your models here.

admin.site.register(SemiAdmin)
admin.site.register(Book)
admin.site.register(Promotion)
admin.site.register(Routine)
admin.site.register(Noticeboard)
admin.site.register(Attendance)
admin.site.register(Syllabus)
admin.site.register(EventCalendar)
admin.site.register(StudentDomainScore)
admin.site.register(Mark)
admin.site.register(SubjectPermission)
admin.site.register(SchoolSettings)
admin.site.register(MarkSheetFormat)
admin.site.register(Grade)
admin.site.register(BookIssue)
admin.site.register(Invoice)
