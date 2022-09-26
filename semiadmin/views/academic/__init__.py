from django.shortcuts import render
from django.views import View
from django.db.models import Max, Min

from management import models as user_model
from student import models as student_model
from teacher import models as teacher_model
from ... import models as semiadmin_model
from .filter import *
from .modal import *
import calendar


class DailyAttendance(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()
		try:
			max_date = semiadmin_model.Attendance.objects.aggregate(Max('the_date'))['the_date__max'].year
			min_date = semiadmin_model.Attendance.objects.aggregate(Min('the_date'))['the_date__min'].year
			year_range = range(min_date, max_date+1)
		except:
			year_range = []
		months = enumerate(calendar.month_name[1:], 1)
		return render(request, 'semiadmin/academic/attendance.html', {'the_classes': the_classes,
			'year_range': year_range, 'months': months})
		

class ClassRoutine(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()
		return render(request, 'semiadmin/academic/routine.html', {'the_classes': the_classes})
			

class Subject(View):
	def get(self, request):
		classes = student_model.JustClass.objects.all()
		return render(request, 'semiadmin/academic/subject.html', {'classes': classes})
			

class Syllabus(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()
		return render(request, 'semiadmin/academic/syllabus.html', {'the_classes': the_classes})


class Class(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()
		return render(request, 'semiadmin/academic/manage_class.html', {'the_classes': the_classes})
			

class ClassRoom(View):
	def get(self, request):
		the_classes = student_model.Class.objects.all()
		return render(request, 'semiadmin/academic/class_room.html', {'the_classes': the_classes})
			

class Department(View):
	def get(self, request):
		departments = teacher_model.Department.objects.all()
		return render(request, 'semiadmin/academic/department.html', {'departments': departments})
				

class EventCalendar(View):
	def get(self, request):
		event_calendars = semiadmin_model.EventCalendar.objects.all()
		return render(request, 'semiadmin/academic/event_calendar.html', {'event_calendars': event_calendars})
		
