from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse

from management import models as user_model
from student import models as student_model
from teacher import models as teacher_model
from ... import models as semiadmin_model
from utils import help as help_tools
from datetime import datetime


""" Attendance SECTION """

class TakeAttendance(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()
		return render(request, 'semiadmin/academic/modal/attendance.html', {'the_classes': the_classes})
		
	def post(self, request):
		data = dict(request.POST)
		the_date = help_tools.date_converter(request.POST.get('date'))
		the_section = request.POST.get('section_id')
		just_class = student_model.JustClass.objects.filter(pk=request.POST.get('class_id')).first()
		the_class = student_model.Class.objects.filter(the_class=just_class, the_section=the_section).first()

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
		students = student_model.Student.objects.filter(student_class_room=the_class).all()

		attendance_list = semiadmin_model.Attendance.objects.filter(the_class=the_class, the_date=the_date).all()
		attendances = set()
		for attendance in attendance_list:
			if attendance.attended:
				attendances.add(attendance.student)
		return render(request, 'semiadmin/academic/modal/attendance_list.html', {'students': students, 
			'attendances': attendances})
		
""" Attendance SECTION """


""" Syllabus SECTION """

class SyllabusCreate(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()
		return render(request, 'semiadmin/academic/modal/syllabus.html', {'the_classes': the_classes})

	def post(self, request):
		the_class_id = request.POST.get('class_id')
		the_section = request.POST.get('section_id')
		just_class = student_model.JustClass.objects.filter(pk=the_class_id).first()
		the_class = student_model.Class.objects.filter(the_class=just_class, the_section=the_section).first()
		
		subject_name = request.POST.get('subject_id')
		subject = student_model.Subject.objects.filter(name=subject_name).first()

		data = {
			'subject': subject,
			'the_class': the_class,
			'title': request.POST.get('title'),
			'file': request.FILES.get('syllabus_file'),
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.Syllabus.objects.create(**new_data)
		return JsonResponse({"status": True, "notification": "Syllabus Created Successfully"})


class SyllabusDelete(View):
	def post(self, request, id):
		semiadmin_model.Syllabus.objects.filter(pk=id).first().delete()
		return JsonResponse({"status": True, "notification": "Syllabus Deleted Successfully"})

	
""" Syllabus SECTION """

""" ClassRoutine SECTION """

class ClassRoutineCreate(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()
		teachers = teacher_model.Teacher.objects.all()

		weekdays = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']

		minutes = []
		for minute in range(0, 56, 5):
			minutes.append(str(minute))

		hours = []
		for m in ['AM', 'PM']:
			for i in range(1, 13):
				hours.append(f'{i} {m}')

		return render(request, 'semiadmin/academic/modal/routine.html', {'the_classes': the_classes,
			'teachers': teachers, 'weekdays': weekdays, 'hours': hours, 'minutes': minutes})

	def post(self, request):
		the_class_id = request.POST.get('class_id')
		the_section = request.POST.get('section_id')
		just_class = student_model.JustClass.objects.filter(pk=the_class_id).first()
		the_class = student_model.Class.objects.filter(the_class=just_class, the_section=the_section).first()
		
		subject_name = request.POST.get('subject_id')
		subject = student_model.Subject.objects.filter(name=subject_name).first()

		teacher_id = request.POST.get('teacher_id')
		teacher = teacher_model.Teacher.objects.filter(pk=teacher_id).first()

		data = {
			'subject': subject,
			'the_class': the_class,
			'teacher': teacher,
			'day': request.POST.get('day'),
			'starting_hour': request.POST.get('starting_hour'),
			'starting_minute': request.POST.get('starting_minute'),
			'ending_hour': request.POST.get('ending_hour'),
			'ending_minute': request.POST.get('ending_minute'),
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.Routine.objects.create(**new_data)
		return JsonResponse({"status": True, "notification": "Routine Created Successfully"})


class ClassRoutineEdit(View):
	def get(self, request, id):
		the_sections = sorted(student_model.Class.objects.values_list('the_section').distinct())
		the_classes = student_model.JustClass.objects.all()
		teachers = teacher_model.Teacher.objects.all()
		routine = semiadmin_model.Routine.objects.filter(pk=id).first()

		weekdays = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']

		minutes = []
		for minute in range(0, 56, 5):
			minutes.append(str(minute))

		hours = []
		for m in ['AM', 'PM']:
			for i in range(1, 13):
				hours.append(f'{i} {m}')

		return render(request, 'semiadmin/academic/modal/routine_edit.html', {'the_classes': the_classes,
			'teachers': teachers, 'routine': routine, 'the_sections': the_sections,
			'weekdays': weekdays, 'hours': hours, 'minutes': minutes})

	def post(self, request, id):
		the_class_id = request.POST.get('class_id')
		the_section = request.POST.get('section_id')
		just_class = student_model.JustClass.objects.filter(pk=the_class_id).first()
		the_class = student_model.Class.objects.filter(the_class=just_class, the_section=the_section).first()
		
		subject_name = request.POST.get('subject_id')
		subject = student_model.Subject.objects.filter(name=subject_name).first()

		teacher_id = request.POST.get('teacher_id')
		teacher = teacher_model.Teacher.objects.filter(pk=teacher_id).first()

		data = {
			'subject': subject,
			'the_class': the_class,
			'teacher': teacher,
			'day': request.POST.get('day'),
			'starting_hour': request.POST.get('starting_hour'),
			'starting_minute': request.POST.get('starting_minute'),
			'ending_hour': request.POST.get('ending_hour'),
			'ending_minute': request.POST.get('ending_minute'),
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.Routine.objects.filter(pk=id).update(**new_data)
		return JsonResponse({"status": True, "notification": "Routine Updated Successfully"})


class ClassRoutineDelete(View):
	def post(self, request, id):
		semiadmin_model.Routine.objects.filter(pk=id).first().delete()
		return JsonResponse({"status": True, "notification": "Routine Deleted Successfully"})

	
""" ClassRoutine SECTION """

""" EventCalendar SECTION """

class EventCalendarCreate(View):
	def get(self, request):
		html = render(request, 'semiadmin/academic/modal/event_calendar.html', {})
		return HttpResponse(html)

	def post(self, request):
		data = {
			'title':request.POST.get('title'),
			'starting_date': datetime.strptime(request.POST.get('starting_date').strip(), '%m/%d/%Y'),
			'ending_date': datetime.strptime(request.POST.get('ending_date').strip(), '%m/%d/%Y'),
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.EventCalendar.objects.create(**new_data)
		return JsonResponse({"status": True, "notification": "Event Calender Created Successfully"})


class EventCalendarEdit(View):
	def get(self, request, id):
		event_calendar = semiadmin_model.EventCalendar.objects.filter(pk=id).first()
		html = render(request, 'semiadmin/academic/modal/event_calendar_edit.html', {'event_calendar': event_calendar})
		return HttpResponse(html)

	def post(self, request, id):
		data = {
			'title':request.POST.get('title'),
			'starting_date': help_tools.date_converter(request.POST.get('starting_date')),
			'ending_date': help_tools.date_converter(request.POST.get('ending_date')),
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.EventCalendar.objects.filter(pk=id).update(**new_data)
		return JsonResponse({"status": True, "notification": "Event Calender Updated Successfully"})


class EventCalendarDelete(View):
	def post(self, request, id):
		semiadmin_model.EventCalendar.objects.filter(pk=id).first().delete()
		return JsonResponse({"status": True, "notification": "Event Calender Deleted Successfully"})

""" END EventCalendar SECTION """



""" JustClass SECTION """

class ClassCreate(View):
	def get(self, request):
		html = render(request, 'semiadmin/academic/modal/class.html', {})
		return HttpResponse(html)

	def post(self, request):
		data = {
			'the_class':request.POST.get('the_class').upper()
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		student_model.JustClass.objects.create(**new_data)
		return JsonResponse({"status": True, "notification": "Class Created Successfully"})


class ClassEdit(View):
	def get(self, request, id):
		the_class = student_model.JustClass.objects.filter(pk=id).first()
		html = render(request, 'semiadmin/academic/modal/class_edit.html', {'the_class': the_class})
		return HttpResponse(html)

	def post(self, request, id):
		data = {
			'the_class':request.POST.get('the_class').upper()
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		student_model.JustClass.objects.filter(pk=id).update(**new_data)
		return JsonResponse({"status": True, "notification": "Class Updated Successfully"})


class ClassDelete(View):
	def post(self, request, id):
		student_model.JustClass.objects.filter(pk=id).first().delete()
		return JsonResponse({"status": True, "notification": "Class Deleted Successfully"})

""" END JustClass SECTION """



""" Subject SECTION """

class SubjectCreate(View):
	def get(self, request):
		classes = student_model.JustClass.objects.all()
		html = render(request, 'semiadmin/academic/modal/subject.html', {'classes': classes})
		return HttpResponse(html)

	def post(self, request):
		the_class = request.POST.get('class_id')
		subject_name = request.POST.get('name')

		just_class = student_model.JustClass.objects.filter(the_class=the_class).first()
		if just_class and subject_name:
			try:
				just_class.subject.create(name=subject_name)
			except:
				subject = student_model.Subject.objects.filter(name=subject_name).first()
				just_class.subject.add(subject)
				just_class.save()

			return JsonResponse({"status": True, "notification": "Subject Created Successfully"})
		return JsonResponse({"status": False, "notification": "Subject Not Created"})



class SubjectEdit(View):
	def get(self, request, class_id, subject_id):
		classes = student_model.JustClass.objects.all()
		subject = teacher_model.Subject.objects.filter(pk=subject_id).first()
		html = render(request, 'semiadmin/academic/modal/subject_edit.html', {'subject': subject, 'classes': classes,
			'class_id': class_id})
		return HttpResponse(html)

	def post(self, request, class_id, subject_id):
		the_class = request.POST.get('class_id')
		subject_name = request.POST.get('name')

		subject = student_model.Subject.objects.filter(pk=subject_id).first()
		just_class = student_model.JustClass.objects.filter(the_class=class_id).first()

		if just_class and subject_name:
			just_class.subject.filter(pk=subject_id).update(name=subject_name)

		if the_class != class_id and just_class:
			move_class = student_model.JustClass.objects.filter(the_class=the_class).first()
			move_class.subject.add(just_class.subject.filter(pk=subject_id).first())
			just_class.subject.remove(subject)

		return JsonResponse({"status": True, "notification": "Subject Updated Successfully"})


class SubjectDelete(View):
	def post(self, request, class_id, subject_id):
		subject = student_model.Subject.objects.filter(pk=subject_id).first()
		just_class = student_model.JustClass.objects.filter(the_class=class_id).first()
		just_class.subject.remove(subject)
		return JsonResponse({"status": True, "notification": "Subject Deleted Successfully"})

""" END Subject SECTION """


""" Department SECTION """

class DepartmentCreate(View):
	def get(self, request):
		html = render(request, 'semiadmin/academic/modal/department.html', {})
		return HttpResponse(html)

	def post(self, request):
		data = {
			'name':request.POST.get('name')
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		teacher_model.Department.objects.create(**new_data)
		return JsonResponse({"status": True, "notification": "Department Created Successfully"})


class DepartmentEdit(View):
	def get(self, request, id):
		department = teacher_model.Department.objects.filter(pk=id).first()
		html = render(request, 'semiadmin/academic/modal/department_edit.html', {'department': department})
		return HttpResponse(html)

	def post(self, request, id):
		data = {
			'name':request.POST.get('name')
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		teacher_model.Department.objects.filter(pk=id).update(**new_data)
		return JsonResponse({"status": True, "notification": "Department Updated Successfully"})


class DepartmentDelete(View):
	def post(self, request, id):
		teacher_model.Department.objects.filter(pk=id).first().delete()
		return JsonResponse({"status": True, "notification": "Department Deleted Successfully"})

""" END Department SECTION """



""" Class SECTION """

class ClassRoomCreate(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()
		html = render(request, 'semiadmin/academic/modal/class_room.html', {'the_classes': the_classes})
		return HttpResponse(html)

	def post(self, request):
		data = {
			'the_section': request.POST.get('section_id').upper()
		}

		class_id = request.POST.get('class_id')
		just_class = student_model.JustClass.objects.filter(the_class=class_id).first()

		if just_class and request.POST.get('section_id'):
			data['the_class'] = just_class

			new_data = {}
			for k in data:
				if data[k]:
					 new_data[k] = data[k]

			student_model.Class.objects.create(**new_data)
			return JsonResponse({"status": True, "notification": "Class created Successfully"})
		return JsonResponse({"status": False, "notification": "Class or Room empty"})


class ClassRoomEdit(View):
	def get(self, request, id):
		the_classes = student_model.JustClass.objects.all()
		class_room = student_model.Class.objects.filter(pk=id).first()
		html = render(request, 'semiadmin/academic/modal/class_room_edit.html', {'class_room': class_room, 'the_classes': the_classes})
		return HttpResponse(html)

	def post(self, request, id):
		data = {
			'the_section': request.POST.get('section_id').upper()
		}

		class_id = request.POST.get('class_id')
		just_class = student_model.JustClass.objects.filter(the_class=class_id).first()

		if just_class and request.POST.get('section_id'):
			data['the_class'] = just_class

			new_data = {}
			for k in data:
				if data[k]:
					 new_data[k] = data[k]

			student_model.Class.objects.filter(pk=id).update(**new_data)
			return JsonResponse({"status": True, "notification": "Class Updated Successfully"})
		return JsonResponse({"status": False, "notification": "Class or Room empty"})



class ClassRoomDelete(View):
	def post(self, request, id):
		student_model.Class.objects.filter(pk=id).first().delete()
		return JsonResponse({"status": True, "notification": "Class Deleted Successfully"})

""" END Class SECTION """

