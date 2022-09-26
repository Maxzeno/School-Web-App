from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse

from management import models as user_model
from semiadmin import models as semiadmin_model
from student import models as student_model
from utils import help as help_tools
from ... import models as teacher_model
from datetime import datetime


""" Attendance SECTION """

class TakeAttendance(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()
		return render(request, 'teacher/academic/modal/attendance.html', {'the_classes': the_classes})
		
	def post(self, request):
		data = dict(request.POST)
		the_date = help_tools.date_converter(request.POST.get('date'))
		the_section = request.POST.get('section_id')
		just_class = student_model.JustClass.objects.filter(pk=request.POST.get('class_id')).first()
		the_class = student_model.Class.objects.filter(the_class=just_class, the_section=the_section).first()

		perm = help_tools.class_perm(request, the_class)
		if not perm:
			return JsonResponse({"status": False, "notification": "Permission denied"})

		for k in data:
			if k.startswith('status'):
				student = student_model.Student.objects.filter(pk=k.split('-')[1]).first()
				found = semiadmin_model.Attendance.objects.filter(student=student, the_class=the_class, the_date=the_date).first()
				if data[k][0] == '1':
					if found:
						if found.attended:
							pass
						else:
							found.attended = True
							found.save()
					else:
						semiadmin_model.Attendance.objects.create(student=student, the_class=the_class, the_date=the_date)
				else:
					if found:
						if found.attended:
							found.attended = False
							found.save()
						else:
							pass
					else:
						pass

		return JsonResponse({"status": True, "notification": "Attendance Updated Successfully"})


class AttendanceList(View):
	def post(self, request):
		the_date = help_tools.date_converter(request.POST.get('date'))
		the_section = request.POST.get('section_id')
		just_class = student_model.JustClass.objects.filter(pk=request.POST.get('class_id')).first()
		the_class = student_model.Class.objects.filter(the_class=just_class, the_section=the_section).first()
		perm = help_tools.class_perm(request, the_class)
		if not perm:
			return help_tools.perm_not()

		students = student_model.Student.objects.filter(student_class_room=the_class).all()

		attendance_list = semiadmin_model.Attendance.objects.filter(the_class=the_class, the_date=the_date).all()
		attendances = set()
		for attendance in attendance_list:
			if attendance.attended:
				attendances.add(attendance.student)
		return render(request, 'teacher/academic/modal/attendance_list.html', {'students': students, 
			'attendances': attendances})
		
""" Attendance SECTION """

