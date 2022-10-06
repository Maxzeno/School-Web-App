from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse

from management import models as user_model
from student import models as student_model
from teacher import models as teacher_model
from ... import models as semiadmin_model
from ...utils import DEFAULT_IMAGE_THE_URL
from utils.html import HTML
from utils import help as help_tool
from .filter import GetGradeRemark
import csv
import io
import mimetypes
import os
import datetime
from datetime import date
import openpyxl
import xlrd

"""  MarkExcel SECTION """

class MarkExcelCreate(View):
	def get(self, request):
		exam_id = request.GET.get('exam_id')
		class_id = request.GET.get('class_id')
		section_id = request.GET.get('section_id')
		subject_id = request.GET.get('subject_id')
		session_id = request.GET.get('session_id')

		html = render(request, 'semiadmin/exam/modal/mark_excel.html', {
			'exam_id': exam_id,
			'class_id': class_id,
			'section_id': section_id,
			'subject_id': subject_id,
			'session_id': session_id,
		})
		return HttpResponse(html)

	def post(self, request):
		exam_id = request.POST.get('exam_id')
		class_id = request.POST.get('class_id')
		section_id = request.POST.get('section_id')
		subject_id = request.POST.get('subject_id')
		session_id = request.POST.get('session_id')

		try:
			class_room = student_model.Class.objects.filter(the_class=class_id, the_section=section_id).first()
			subject = student_model.Subject.objects.filter(name=subject_id).first()
			exam = student_model.Exam.objects.filter(pk=exam_id).first()
			mark_sheet_format = semiadmin_model.MarkSheetFormat.objects.filter(category=class_id[:-1], session=session_id).first()

			excel_file = request.FILES["excel_file"]

			try:
				book = xlrd.open_workbook(excel_file.name, file_contents=excel_file.read())

				if excel_file:
					sh = book.sheet_by_index(0)

					# Iterate through rows, returning each as a list that you can index:
					first_row = sh.row_values(0)
					head, head_valid_len = self.map_head(first_row[1:])

					for rownum in range(1, sh.nrows):
						student_data = sh.row_values(rownum)
						update_data = self.wrap(head, student_data[1:])
						if update_data:
							student = student_model.Student.objects.filter(name=student_data[0]).first()
							semiadmin_model.Mark.objects.filter(student=student, exam=exam, class_room=class_room, subject=subject)\
							.update_or_create(defaults={'student': student, 'exam': exam, 'class_room': class_room, 'subject': subject, 
								'mark_sheet_format': mark_sheet_format, 'comment': GetGradeRemark().get_grade_remark(
									self.total(student_data[1:]))}, **update_data)

			except:
				book = openpyxl.load_workbook(excel_file)
				sheet = book.active

				val = list(sheet.values)
				first_row = val[0]
				head, head_valid_len = self.map_head(first_row[1:])

				for student_data in val[1:]:
					update_data = self.wrap(head, student_data[1:])
					if update_data:
						student = student_model.Student.objects.filter(name=student_data[0]).first()
						semiadmin_model.Mark.objects.filter(student=student, exam=exam, class_room=class_room, subject=subject)\
						.update_or_create(defaults={'student': student, 'exam': exam, 'class_room': class_room, 'subject': subject,
								'mark_sheet_format': mark_sheet_format, 'comment': GetGradeRemark().get_grade_remark(
									self.total(student_data[1:]))}, **update_data)


			return JsonResponse({"status": True, "notification": "Marked Successfully"})
		except:
			return JsonResponse({"status": False, "notification": "Either excel didn't match student format or something is empty"})


	def total(self, arr):
		summer = 0
		for i in arr:
			try:
				summer += float(i)
			except:
				continue
		return summer


	def map_head(self, head):
		len_head = len(head)
		# if head[-2].lower() == 'optional':
		# 	len_head-2

		if len_head == 5:
			mark_sheet = ['resumption_test10', 'mid_test10', 'project10', 'assignment10', 'exam60']

		elif len_head == 4:
			mark_sheet = ['resumption_test10', 'mid_test10', 'project10', 'exam70']

		elif len_head == 3:
			mark_sheet = ['resumption_test15', 'mid_test15', 'exam70']

		elif len_head == 2:
			mark_sheet = ['test30', 'exam70']

		elif len_head == 1:
			mark_sheet = ['exam100']

		return mark_sheet, len_head


	def wrap(self, a, b):
		new = {}
		print(a, b)
		for i in range(len(a)):
			if b[i]:
				new[a[i]] = b[i]
		return new

"""  MarkExcel SECTION """


""" PromotionSet """

class PromotionSet(View):
	def post(self, request):
		student_id = request.POST.get('student_id')
		class_room_from = request.POST.get('class_room_from')
		class_room_to = request.POST.get('class_room_to')
		session_from = request.POST.get('session_from')
		session_to = request.POST.get('session_to')

		session_from = student_model.Session.objects.filter(pk=session_from).first()
		session_to = student_model.Session.objects.filter(pk=session_to).first()
		class_room_from = student_model.Class.objects.filter(pk=class_room_from).first()
		class_room_to = student_model.Class.objects.filter(pk=class_room_to).first()

		student = student_model.Student.objects.filter(pk=student_id).first()
		student.student_class_room = class_room_to
		student.save()

		found = semiadmin_model.Promotion.objects.filter(student=student, current_session=session_from, 
				next_session=session_to)
		if found:
			found.update(promoting_from=class_room_from, promoting_to=class_room_to)
		else:
			semiadmin_model.Promotion.objects.create(student=student, current_session=session_from, 
				next_session=session_to, promoting_from=class_room_from, promoting_to=class_room_to)

		return JsonResponse({'status': 'ok'})

""" END PromotionSet """

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

		student = student_model.Student.objects.filter(pk=student_id.replace('-', '/')).first()
		exam = student_model.Exam.objects.filter(pk=exam_id).first()
		class_room = student_model.Class.objects.filter(the_class=class_id, the_section=section_id).first()
		subject = student_model.Subject.objects.filter(name=subject_id).first()
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

		data = dict(request.POST)
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


""" Grade SECTION """

class GradeCreate(View):
	def get(self, request):
		html = render(request, 'semiadmin/exam/modal/grade.html', {})
		return HttpResponse(html)

	def post(self, request):
		data = {
			'grade':request.POST.get('grade'),
			'grade_point':request.POST.get('grade_point'),
			'mark_from':request.POST.get('mark_from'),
			'mark_upto':request.POST.get('mark_upto'),
			'remarks':request.POST.get('remarks'),
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.Grade.objects.create(**new_data)
		return JsonResponse({"status": True, "notification": "Grade Updated Successfully"})


class GradeEdit(View):
	def get(self, request, id):
		grade = semiadmin_model.Grade.objects.filter(pk=id).first()
		html = render(request, 'semiadmin/exam/modal/grade_edit.html', 
			{'grade':grade})
		return HttpResponse(html)

	def post(self, request, id):
		data = {
			'grade':request.POST.get('grade'),
			'grade_point':request.POST.get('grade_point'),
			'mark_from':request.POST.get('mark_from'),
			'mark_upto':request.POST.get('mark_upto'),
			'remarks':request.POST.get('remarks'),
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.Grade.objects.filter(pk=id).update(**new_data)
		return JsonResponse({"status": True, "notification": "Grade Updated Successfully"})


class GradeDelete(View):
	def post(self, request, id):
		semiadmin_model.Grade.objects.filter(pk=id).first().delete()
		return JsonResponse({"status": True, "notification": "Grade Deleted Successfully"})

""" END Grade SECTION """




""" Principal Comment Code SECTION """

class HousemasterCommentCodeCreate(View):
	def get(self, request):
		html = render(request, 'semiadmin/exam/modal/housemaster_comment_code.html', {})
		return HttpResponse(html)

	def post(self, request):
		data = {
			'category':request.POST.get('category'),
			'code_number':request.POST.get('code_number'),
			'code_description':request.POST.get('code_description'),
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.HousemasterCommentCode.objects.create(**new_data)
		return JsonResponse({"status":True,"notification": "Comment Code Created Successfully"})


class HousemasterCommentCodeEdit(View):
	def get(self, request, id):
		housemaster_comment_code = semiadmin_model.HousemasterCommentCode.objects.filter(pk=id).first()
		html = render(request, 'semiadmin/exam/modal/housemaster_comment_code_edit.html', 
			{'housemaster_comment_code':housemaster_comment_code})
		return HttpResponse(html)

	def post(self, request, id):
		data = {
			'category':request.POST.get('category'),
			'code_number':request.POST.get('code_number'),
			'code_description':request.POST.get('code_description'),
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.HousemasterCommentCode.objects.filter(pk=id).update(**new_data)
		return JsonResponse({"status":True,"notification": "Comment Code Updated Successfully"})


class HousemasterCommentCodeDelete(View):
	def post(self, request, id):
		semiadmin_model.HousemasterCommentCode.objects.filter(pk=id).first().delete()
		return JsonResponse({"status":True,"notification": "Comment Code Deleted Successfully"})

""" END Principal Comment Code SECTION """


""" CognitiveKey Domain Score SECTION """

class CognitiveKeyDomainScoreCreate(View):
	def get(self, request):
		html = render(request, 'semiadmin/exam/modal/cognitive_key_domain_score.html', {})
		return HttpResponse(html)

	def post(self, request):
		data = {
			'key':request.POST.get('key'),
			'score':request.POST.get('score'),
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.CognitiveKeyDomainScore.objects.create(**new_data)
		return JsonResponse({"status":True,"notification": "Domain Score Created Successfully"})


class CognitiveKeyDomainScoreEdit(View):
	def get(self, request, id):
		cognitive_key_domain_score = semiadmin_model.CognitiveKeyDomainScore.objects.filter(pk=id).first()
		html = render(request, 'semiadmin/exam/modal/cognitive_key_domain_score_edit.html', 
			{'cognitive_key_domain_score':cognitive_key_domain_score})
		return HttpResponse(html)

	def post(self, request, id):
		data = {
			'key':request.POST.get('key'),
			'score':request.POST.get('score'),
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.CognitiveKeyDomainScore.objects.filter(pk=id).update(**new_data)
		return JsonResponse({"status":True,"notification": "Domain Score Updated Successfully"})


class CognitiveKeyDomainScoreDelete(View):
	def post(self, request, id):
		semiadmin_model.CognitiveKeyDomainScore.objects.filter(pk=id).first().delete()
		return JsonResponse({"status":True,"notification": "Domain Score Deleted Successfully"})

""" END CognitiveKey Domain Score SECTION """


""" Principal Subject Code SECTION """

class PrincipalSubjectCodeCreate(View):
	def get(self, request):
		subjects = student_model.Subject.objects.all()
		html = render(request, 'semiadmin/exam/modal/principal_subject_code.html', {'subjects': subjects})
		return HttpResponse(html)

	def post(self, request):
		data = {
			'category':request.POST.get('category'),
			'subject_code':request.POST.get('subject_code'),
		}

		subject = request.POST.get('subject')

		try:
			subject = student_model.Subject.objects.get(name=subject)
		except:
			subject = student_model.Subject.objects.create(name=subject)

		data['subject'] = subject

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.PrincipalSubjectCode.objects.create(**new_data)
		return JsonResponse({"status":True,"notification": "Subject Code Created Successfully"})


class PrincipalSubjectCodeEdit(View):
	def get(self, request, id):
		subjects = student_model.Subject.objects.all()
		principal_subject_code = semiadmin_model.PrincipalSubjectCode.objects.filter(pk=id).first()
		html = render(request, 'semiadmin/exam/modal/principal_subject_code_edit.html', 
			{'principal_subject_code':principal_subject_code, 'subjects': subjects})
		return HttpResponse(html)

	def post(self, request, id):
		data = {
			'category':request.POST.get('category'),
			'subject_code':request.POST.get('subject_code'),
		}


		subject = request.POST.get('subject')

		try:
			subject = student_model.Subject.objects.get(name=subject)
		except:
			subject = student_model.Subject.objects.create(name=subject)

		data['subject'] = subject

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.PrincipalSubjectCode.objects.filter(pk=id).update(**new_data)
		return JsonResponse({"status":True,"notification": "Subject Code Updated Successfully"})


class PrincipalSubjectCodeDelete(View):
	def post(self, request, id):
		semiadmin_model.PrincipalSubjectCode.objects.filter(pk=id).first().delete()
		return JsonResponse({"status":True,"notification": "Subject Code Deleted Successfully"})

""" END Principal Subject Code SECTION """



""" Principal Comment Code SECTION """

class TeacherCommentCodeCreate(View):
	def get(self, request):
		html = render(request, 'semiadmin/exam/modal/teacher_comment_code.html', {})
		return HttpResponse(html)

	def post(self, request):
		data = {
			'category':request.POST.get('category'),
			'code_number':request.POST.get('code_number'),
			'code_description':request.POST.get('code_description'),
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.TeacherCommentCode.objects.create(**new_data)
		return JsonResponse({"status":True,"notification": "Comment Code Created Successfully"})


class TeacherCommentCodeEdit(View):
	def get(self, request, id):
		teacher_comment_code = semiadmin_model.TeacherCommentCode.objects.filter(pk=id).first()
		html = render(request, 'semiadmin/exam/modal/teacher_comment_code_edit.html', 
			{'teacher_comment_code':teacher_comment_code})
		return HttpResponse(html)

	def post(self, request, id):
		data = {
			'category':request.POST.get('category'),
			'code_number':request.POST.get('code_number'),
			'code_description':request.POST.get('code_description'),
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.TeacherCommentCode.objects.filter(pk=id).update(**new_data)
		return JsonResponse({"status":True,"notification": "Comment Code Updated Successfully"})


class TeacherCommentCodeDelete(View):
	def post(self, request, id):
		semiadmin_model.TeacherCommentCode.objects.filter(pk=id).first().delete()
		return JsonResponse({"status":True,"notification": "Comment Code Deleted Successfully"})

""" END Principal Comment Code SECTION """



""" Principal Comment Code SECTION """

class PrincipalCommentCodeCreate(View):
	def get(self, request):
		html = render(request, 'semiadmin/exam/modal/principal_comment_code.html', {})
		return HttpResponse(html)

	def post(self, request):
		data = {
			'category':request.POST.get('category'),
			'code_number':request.POST.get('code_number'),
			'code_description':request.POST.get('code_description'),
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.PrincipalCommentCode.objects.create(**new_data)
		return JsonResponse({"status":True,"notification": "Comment Code Created Successfully"})


class PrincipalCommentCodeEdit(View):
	def get(self, request, id):
		principal_comment_code = semiadmin_model.PrincipalCommentCode.objects.filter(pk=id).first()
		html = render(request, 'semiadmin/exam/modal/principal_comment_code_edit.html', 
			{'principal_comment_code':principal_comment_code})
		return HttpResponse(html)

	def post(self, request, id):
		data = {
			'category':request.POST.get('category'),
			'code_number':request.POST.get('code_number'),
			'code_description':request.POST.get('code_description'),
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.PrincipalCommentCode.objects.filter(pk=id).update(**new_data)
		return JsonResponse({"status":True,"notification": "Comment Code Updated Successfully"})


class PrincipalCommentCodeDelete(View):
	def post(self, request, id):
		semiadmin_model.PrincipalCommentCode.objects.filter(pk=id).first().delete()
		return JsonResponse({"status":True,"notification": "Comment Code Deleted Successfully"})

""" END Principal Comment Code SECTION """


""" EXAM SECTION """

class ManageExaminationCreate(View):
	def get(self, request):
		html = render(request, 'semiadmin/exam/modal/exam.html', {'sessions': help_tool.sessioner()})

		return HttpResponse(html)

	def post(self, request):

		data = {
			'exam_name':request.POST.get('exam_name'),
			'exam_term':request.POST.get('exam_term'),
			'exam_starts':request.POST.get('starting_date'),
			'exam_ends':request.POST.get('ending_date'),
			'next_term_begins':request.POST.get('next_term_begins'),
			'next_term_ends':request.POST.get('next_term_ends'),
			'comment':request.POST.get('exam_comment'),
		}

		exam_session = request.POST.get('exam_session')

		try:
			session = student_model.Session.objects.get(session=exam_session.upper())
		except:
			if help_tool.is_date_range(exam_session):
				session = student_model.Session.objects.create(session=exam_session.upper())
			else:
				return JsonResponse({"status":False,"notification": f"Invalid Session {exam_session}"})


		data['exam_session'] = session

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]
		student_model.Exam.objects.create(**new_data)
		
		return JsonResponse({"status":True,"notification": "Exam Created Successfully"})


class ManageExaminationEdit(View):
	def get(self, request, id):
		exam = student_model.Exam.objects.filter(pk=id).first()
		default_date = datetime.date.today().strftime('%d/%m/%Y')
		html = render(request, 'semiadmin/exam/modal/exam_edit.html', {'exam':exam, 'sessions': help_tool.sessioner(), 
			'default_date': default_date})
		return HttpResponse(html)

	def post(self, request, id):

		data = {
			'exam_name':request.POST.get('exam_name'),
			'exam_term':request.POST.get('exam_term'),
			'exam_starts':request.POST.get('starting_date'),
			'exam_ends':request.POST.get('ending_date'),
			'next_term_begins':request.POST.get('next_term_begins'),
			'next_term_ends':request.POST.get('next_term_ends'),
			'comment':request.POST.get('exam_comment'),
		}

		exam_session = request.POST.get('exam_session')

		try:
			session = student_model.Session.objects.get(session=exam_session.upper())
		except:
			session = student_model.Session.objects.create(session=exam_session.upper())

		data['exam_session'] = session

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		student_model.Exam.objects.filter(pk=id).update(**new_data)
		
		return JsonResponse({"status":True,"notification": "Exam Updated Successfully"})


class ManageExaminationDelete(View):
	def post(self, request, id):
		student_model.Exam.objects.filter(pk=id).first().delete()
		
		return JsonResponse({"status":True,"notification": "Exam Deleted Successfully"})

""" END EXAM SECTION """


""" PASS MARK SECTION """

class PassMarkCreate(View):
	def get(self, request):
		subjects = student_model.Subject.objects.all()

		html = render(request, 'semiadmin/exam/modal/pass_mark.html', {'sessions': help_tool.sessioner(), 
			'subjects': subjects})

		return HttpResponse(html)

	def post(self, request):

		data = {
			'mark':request.POST.get('mark'),
			'period':request.POST.get('period'),
			'category':request.POST.get('category'),
		}

		session = request.POST.get('session')
		subject = request.POST.get('subject')

		try:
			session = student_model.Session.objects.get(session=session.upper())
		except:
			session = student_model.Session.objects.create(session=session.upper())

		try:
			subject = student_model.Subject.objects.get(name=subject)
		except:
			subject = student_model.Subject.objects.create(name=subject)

		data['session'] = session
		data['subject'] = subject

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]
		student_model.PassMark.objects.create(**new_data)
		
		return JsonResponse({"status":True,"notification": "Pass Mark Updated Successfully"})


class PassMarkEdit(View):
	def get(self, request, id):
		subjects = student_model.Subject.objects.all()

		pass_mark = student_model.PassMark.objects.filter(pk=id).first()

		html = render(request, 'semiadmin/exam/modal/pass_mark_edit.html', {'pass_mark':pass_mark, 
			'sessions': help_tool.sessioner(), 'subjects': subjects})
		return HttpResponse(html)

	def post(self, request, id):

		data = {
			'mark':request.POST.get('mark'),
			'period':request.POST.get('period'),
			'category':request.POST.get('category'),
		}

		session = request.POST.get('session')
		subject = request.POST.get('subject')

		try:
			session = student_model.Session.objects.get(session=session.upper())
		except:
			# session = student_model.Session.objects.create(session=session.upper()
			session = ''

		try:
			subject = student_model.Subject.objects.get(name=subject)
		except:
			subject = student_model.Subject.objects.create(name=subject)

		data['session'] = session
		data['subject'] = subject


		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		student_model.PassMark.objects.filter(pk=id).update(**new_data)
		
		return JsonResponse({"status":True,"notification": "Pass Mark Updated Successfully"})


class PassMarkDelete(View):
	def post(self, request, id):
		student_model.PassMark.objects.filter(pk=id).first().delete()
		return JsonResponse({"status":True,"notification": "Pass Mark Deleted Successfully"})

""" END PASS MARK SECTION """


""" Manage Cognitive Domain SECTION """

class ManageCognitiveDomainCreate(View):
	def get(self, request):
		html = render(request, 'semiadmin/exam/modal/sb_description.html', {})
		return HttpResponse(html)

	def post(self, request):
		data = {
			'sb_type':request.POST.get('sb_type'),
			'description':request.POST.get('description'),
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.ManageCognitiveDomain.objects.create(**new_data)
		return JsonResponse({"status":True,"notification": "Domain Created Successfully"})


class ManageCognitiveDomainEdit(View):
	def get(self, request, id):
		sb_description = semiadmin_model.ManageCognitiveDomain.objects.filter(pk=id).first()
		html = render(request, 'semiadmin/exam/modal/sb_description_edit.html', {'sb_description':sb_description})
		return HttpResponse(html)

	def post(self, request, id):

		data = {
			'sb_type':request.POST.get('sb_type'),
			'description':request.POST.get('description'),
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.ManageCognitiveDomain.objects.filter(pk=id).update(**new_data)
		
		return JsonResponse({"status":True,"notification": "Domain Updated Successfully"})


class ManageCognitiveDomainDelete(View):
	def post(self, request, id):
		semiadmin_model.ManageCognitiveDomain.objects.filter(pk=id).first().delete()
		return JsonResponse({"status":True,"notification": "Domain Deleted Successfully"})

""" END Manage Cognitive Domain SECTION """
