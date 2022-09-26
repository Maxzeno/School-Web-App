from django.shortcuts import render
from django.views import View
from django.db.models import Max, Min


from .filter import *
from .modal import *

from management import models as user_model
from student import models as student_model
from utils import help as help_tools
from ... import models as teacher_model
from semiadmin import models as semiadmin_model

import calendar


class DailyAttendance(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()
		max_date = semiadmin_model.Attendance.objects.aggregate(Max('the_date'))['the_date__max'].year
		min_date = semiadmin_model.Attendance.objects.aggregate(Min('the_date'))['the_date__min'].year
		year_range = range(min_date, max_date+1)
		months = enumerate(calendar.month_name[1:], 1)
		return render(request, 'teacher/academic/attendance.html', {'the_classes': the_classes,
			'year_range': year_range, 'months': months})
		

class ClassRoutine(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()
		return render(request, 'teacher/academic/routine.html', {'the_classes': the_classes})
			

class Subject(View):
	def get(self, request):
		classes = student_model.JustClass.objects.all()
		return render(request, 'teacher/academic/subject.html', {'classes': classes})
			

class Syllabus(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()
		return render(request, 'teacher/academic/syllabus.html', {'the_classes': the_classes})	


class EventCalendar(View):
	def get(self, request):
		event_calendars = semiadmin_model.EventCalendar.objects.all()
		return render(request, 'teacher/academic/event_calendar.html', {'event_calendars': event_calendars})
		
