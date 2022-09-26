from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse

from management import models as user_model
from semiadmin import models as semiadmin_model
from student import models as student_model
from utils import help as help_tools
from ... import models as teacher_model
from collections import defaultdict
import calendar
from datetime import date


class DailyAttendanceFilter(View):
	def post(self, request):
		month = int(request.POST.get('month'))
		year = int(request.POST.get('year'))
		
		the_section = request.POST.get('section_id')
		just_class = student_model.JustClass.objects.filter(pk=request.POST.get('class_id')).first()
		the_class = student_model.Class.objects.filter(the_class=just_class, the_section=the_section).first()
		perm = help_tools.class_perm(request, the_class)
		if not perm:
			return help_tools.perm_not()
			
		students = student_model.Student.objects.filter(student_class_room=the_class).all()

		range_month = range(calendar.monthrange(year, month)[1]+1)

		new = []
		for student in students:
			found = semiadmin_model.Attendance.objects.filter(student=student, attended=True, the_date__year=year,
			the_date__month=month).values_list('the_date')
			print(found)
			if found:
				s = set()
				for i in found:
					s.add(i[0].day)
				new.append([student, s])
			else:
				new.append([student, []])

		last_update = semiadmin_model.Attendance.objects.last().the_date.strftime('%d-%b-%Y')
		month_name = calendar.month_name[month]

		html = render(request, 'teacher/academic/filter/attendance.html', {'range_month': range_month, 
			'new': new, 'the_class': the_class, 'month_name': month_name, 'last_update': last_update})
		return HttpResponse(html)


class SyllabusFilter(View):
	def get(self, request, class_id, section_id):
		just_class = student_model.JustClass.objects.filter(the_class=class_id).first()
		the_class = student_model.Class.objects.filter(the_class=just_class, the_section=section_id).first()
		perm = help_tools.class_perm(request, the_class)
		if not perm:
			return help_tools.perm_not()

		syllabuses = semiadmin_model.Syllabus.objects.filter(the_class=the_class).all()
		html = render(request, 'teacher/academic/filter/syllabus.html', {'syllabuses': syllabuses})
		return HttpResponse(html)


class ClassRoutineFilter(View):
	def get(self, request, class_id, section_id):
		the_class = student_model.Class.objects.filter(the_class=class_id.upper(), 
			the_section=section_id.upper()).first()
		
		perm = help_tools.class_perm(request, the_class)
		if not perm:
			return help_tools.perm_not()

		just_class = student_model.JustClass.objects.filter(the_class=class_id).first()
		the_class = student_model.Class.objects.filter(the_class=just_class, the_section=section_id).first()
		routines = semiadmin_model.Routine.objects.filter(the_class=the_class).all()
		dct = defaultdict(list)

		for routine in routines:
			dct[routine.day].append(routine)

		html = render(request, 'teacher/academic/filter/routine.html', {'dct': dct})
		return HttpResponse(html)


class EventCalendarEvent(View):
	def get(self, request):
		events = semiadmin_model.EventCalendar.objects.all()
		json = [{'title': data.title, 'starting_date': data.starting_date, 'ending_date': data.ending_date} for data in events]
		return JsonResponse(json, safe=False)


class EventCalendarAll(View):
	def get(self, request):
		tbodys = semiadmin_model.EventCalendar.objects.all()
		html = render(request, 'teacher/academic/filter/event_calendar.html', {'event_calendars': tbodys})
		return HttpResponse(html)


class SubjectFilter(View):
	def get(self, request, class_id):
		tbodys = student_model.JustClass.objects.filter(pk=class_id).first()
		the_classes = student_model.Class.objects.filter(the_class=class_id.upper())
		for the_class in the_classes:
			perm = help_tools.class_perm(request, the_class)
			if perm:
				html = render(request, 'teacher/academic/filter/subject.html', {'subjects': tbodys.subject, 'class': tbodys})
				return HttpResponse(html)
		return help_tools.perm_not()

		
