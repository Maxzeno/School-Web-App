from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse

from management import models as user_model
from student import models as student_model
from ... import models as teacher_model
from semiadmin import models as semiadmin_model
from semiadmin.utils import DEFAULT_IMAGE_THE_URL
from utils.html import HTML
from utils import help as help_tools

import csv
import io
import mimetypes
import os
import datetime
from datetime import date


""" Mark """

class MarkSet(View):
	def post(self, request):
		data = {}
		for k in request.POST:
			data[k] = request.POST[k]

		student_id = data.pop('student_id')
		class_id = data.pop('class_id')
		section_id = data.pop('section_id')
		subject_id = data.pop('subject_id')
		exam_id = data.pop('exam_id')
		session_id = data.pop('session_id')
		comment = data.pop('comment')
		del data['csrfmiddlewaretoken']

		new_data = {}
		emptys = []
		for k in data:
			if data[k] == '':
				emptys.append(k)
				continue
			else:
				new_data[k] = data[k] 

		class_room = student_model.Class.objects.filter(the_class=class_id, the_section=section_id).first()
		subject = student_model.Subject.objects.filter(name=subject_id).first()
		
		perm = help_tools.subject_perm(request, class_room, subject)
		if not perm:
			return JsonResponse({'status': 'not ok'})

		student = student_model.Student.objects.filter(pk=student_id.replace('-', '/')).first()
		exam = student_model.Exam.objects.filter(pk=exam_id).first()
		session = semiadmin_model.Session.objects.filter(pk=session_id).first()
		mark_sheet_format = semiadmin_model.MarkSheetFormat.objects.filter(category=class_id[:-1], session=session).first()

		found_mark = semiadmin_model.Mark.objects.filter(exam=exam, class_room=class_room, subject=subject,
				mark_sheet_format=mark_sheet_format, student=student)
		if found_mark:
			upt = found_mark.values(*data.keys())[0]
			for empty in emptys:
				if isinstance(upt[empty], (int, float)):
					new_data[empty] = 0
			found_mark.update(exam=exam, class_room=class_room, subject=subject,
				mark_sheet_format=mark_sheet_format, student=student, comment=comment, **new_data)
			return JsonResponse({'status': 'ok'})

		mark = semiadmin_model.Mark.objects.create(exam=exam, class_room=class_room, subject=subject,
				mark_sheet_format=mark_sheet_format, student=student, comment=comment, **new_data)
		return JsonResponse({'status': 'ok'})

""" END Mark """

""" ManageCognitiveDomainScore SSCTION """

class ManageCognitiveDomainScoreSet(View):
	def post(self, request):
		honesty = request.POST.getlist('honesty')
		exam_id = int(request.POST.get('exam_id'))
		class_id = int(request.POST.get('class_id'))

		the_class = student_model.Class.objects.filter(pk=class_id).first()

		perm = help_tools.class_perm(request, the_class)
		if not perm:
			return JsonResponse({"status": False, "notification": "Permission denied"})

		data = dict(request.POST)
		data.pop('class_id')
		subject_code_dict = {}

		for key_code in data:
			if key_code.startswith('subject_code'):
				sc = request.POST.getlist(key_code)
				new = []
				for i in sc:
					new.append(semiadmin_model.PrincipalSubjectCode.objects.filter(pk=i).first())
				key_domain = ''.join(key_code.split('--')[1:])
				subject_code_dict[key_domain] = new

		for i in range(len(honesty)):
			create_dict = {}
			for key in data:
				if key == 'csrfmiddlewaretoken' or key == 'session' or key == 'exam_id' or key.startswith('subject_code'):
					pass
				elif key == 'student':
					create_dict[key] = student_model.Student.objects.filter(pk=data[key][i]).first()
				elif key == 'principal_code':
					if data[key][i].isdigit():
						create_dict[key] = semiadmin_model.PrincipalCommentCode.objects.filter(pk=data[key][i]).first()
				elif key == 'teacher_code':
					if data[key][i].isdigit():
						create_dict[key] = semiadmin_model.TeacherCommentCode.objects.filter(pk=data[key][i]).first()
				elif key == 'housemaster_code':
					if data[key][i].isdigit():
						create_dict[key] = semiadmin_model.HousemasterCommentCode.objects.filter(pk=data[key][i]).first()
				elif key == 'housemaster_code':
					if data[key][i].isdigit():
						create_dict[key] = semiadmin_model.HousemasterCommentCode.objects.filter(pk=data[key][i]).first()

				else:
					if data[key][i].isdigit():
						create_dict[key] = int(data[key][i])

			domains = semiadmin_model.StudentDomainScore.objects.filter(exam=exam_id, student=create_dict['student'])
			if domains:
				domains.update(**create_dict)
				for domain in domains:
					domain.subject_code.clear()
					if subject_code_dict.get(create_dict['student'].pk):
						for code_of_student in subject_code_dict[create_dict['student'].pk]:
							domain.subject_code.add(code_of_student)

			else:
				create_dict['exam'] = student_model.Exam.objects.filter(pk=exam_id).first()
				new_domain = semiadmin_model.StudentDomainScore.objects.create(**create_dict)
				new_domain.subject_code.clear()

				if subject_code_dict.get(create_dict['student'].pk):
					for code_of_student in subject_code_dict[create_dict['student'].pk]:
						new_domain.subject_code.add(code_of_student)
						new_domain.save()

		return JsonResponse({"status": True, "notification": "Domain Score Set"})

