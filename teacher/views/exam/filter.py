from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db.models import Avg, F, Max, Min, Sum

from semiadmin.views import GetGrade, GetGradeRemark
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
from collections import defaultdict


class ManageCognitiveDomainScoreFilter(View):
	def post(self, request):
		exam_id = request.POST.get('exam_id')
		class_id = request.POST.get('class_id')
		section_id = request.POST.get('section_id')

		class_room = student_model.Class.objects.filter(the_class=class_id, the_section=section_id).first()

		perm = help_tools.class_perm(request, class_room)
		if not perm:
			return help_tools.perm_not()

		students = student_model.Student.objects.filter(student_class_room=class_room).all()

		exam = student_model.Exam.objects.filter(pk=exam_id).first()
		student_domains = semiadmin_model.StudentDomainScore.objects.filter(exam=exam_id).all()
		subject_code_student = {}
		for student_domain in student_domains:
			subject_code_student[student_domain.student.pk] = {i[0] for i in student_domain.subject_code.values_list('pk')}

		domains = student_domains.values_list('student', 'honesty', 'neatness', 'punctuality',
			'attentiveness_in_class', 'organizational_ability', 'perseverance', 'self_control', 'arts_and_crafts', 'drawing_and_painting',
			'labour_and_workshop', 'fluency', 'sport_and_gymnastics', 'handwriting', 'housemaster_code', 'teacher_code', 'principal_code', 'pk') #, 'subject_code')
		domains_dict = {}
		domain_scores = []
		for domain in domains:
			domains_dict[domain[0]] = domain

		for student in students:
			if student.pk in domains_dict:
				domain_scores.append([student, *domains_dict[student.pk], subject_code_student[student.pk]])
			else:
				domain_scores.append([student, student.pk, *['']*13, {}])

		principal_codes = semiadmin_model.PrincipalCommentCode.objects.all()
		teacher_codes = semiadmin_model.TeacherCommentCode.objects.all()
		housemaster_codes = semiadmin_model.HousemasterCommentCode.objects.all()
		subject_codes = semiadmin_model.PrincipalSubjectCode.objects.all()

		html = render(request, 'teacher/exam/filter/sb_description_score_manage.html', {'domain_scores':domain_scores, 'exam_id': exam_id,
			'principal_codes': principal_codes, 'teacher_codes': teacher_codes, 'housemaster_codes': housemaster_codes,
			'subject_codes': subject_codes, 'class_room': class_room, 'exam': exam})
		return HttpResponse(html)


class MarkFilter(View):
	def post(self, request):
		exam_id = request.POST.get('exam')
		class_id = request.POST.get('class_id')
		section_id = request.POST.get('section_id')
		subject_id = request.POST.get('subject')
		session_id = request.POST.get('session')
		html = """
			<div class="col-md-12 text-center">
			    <div class="alert alert-danger" role="alert">
					<h4 class="alert-heading">Fill all fields!</h4>
					<hr>
					<p class="mb-0">With the appropriate values.</p>
			    </div>
			</div>"""
		try:
			exam = student_model.Exam.objects.filter(pk=exam_id).first()
		except:
			return HttpResponse(html, status=400)
		else:
			if exam:
				pass
			else:
				return HttpResponse(html, status=406)

		class_room = student_model.Class.objects.filter(the_class=class_id, the_section=section_id).first()
		subject = student_model.Subject.objects.filter(name=subject_id).first()

		perm = help_tools.subject_perm(request, class_room, subject)
		if not perm:
			return help_tools.perm_not()

		session = semiadmin_model.Session.objects.filter(pk=session_id).first()
		mark_sheet_format = semiadmin_model.MarkSheetFormat.objects.filter(category=class_id[:-1], session=session).first()
		students = student_model.Student.objects.filter(student_class_room=class_room).all()

		students_pk = student_model.Student.objects.filter(student_class_room=class_room).values_list('pk')
		students_pk = [i[0] for i in students_pk]
		# try:
		format_values = self.formart_of_values(mark_sheet_format.mark_format, class_room, exam)
		marks_list = []

		for student in students:
			mark = semiadmin_model.Mark.objects.filter(exam=exam, class_room=class_room, subject=subject,
				mark_sheet_format=mark_sheet_format, student=student).values_list(*format_values).first()
			if mark:
				fnd = list(mark)
				fnd.insert(0, student)
				marks_list.append(fnd+self.calc(mark))
			else:
				marks_list.append(self.empties_in_list(len(format_values), student))

		if class_room.the_class.the_class.lower() == 'ss2' and exam.exam_term.lower() == 'second':
			mark_sheet = ['Test (30)', 'Examination (70)']

		elif class_room.the_class.the_class.lower() in {'ss3', 'jss3', 'js3'} and exam.exam_term.lower() == 'third':
			mark_sheet = ['Examination (100)']

		else:
			if mark_sheet_format.mark_format == 'five_column_format':
				mark_sheet = ['Resumption test (10)', 'Midterm** test (10)', 'Project** (10)', 'Assignment (10)', 'Examination (60)']

			elif mark_sheet_format.mark_format == 'four_column_format':
				mark_sheet = ['Resumption test (10)', 'Midterm** test (10)', 'Project** (10)', 'Examination (70)']

			elif mark_sheet_format.mark_format == 'three_column_format':
				mark_sheet = ['Resumption test (15)', 'Midterm** test (15)', 'Examination (70)']

			elif mark_sheet_format.mark_format == 'two_column_format':
				mark_sheet = ['Test (30)', 'Examination (70)']

		theads = ['Student name', *mark_sheet, 'Total score', 'Grade point', 'Comment', 'Action']

		tbodys = ''
		html = render(request, self.template(len(format_values)), {'tbodys':tbodys, 'theads': theads, 
			'the_format': mark_sheet_format.mark_format, 'the_class': class_id, 'the_section': section_id,
			'subject': subject.name, 'exam': exam, 'exam_year_slash': exam.exam_session.session.replace('-', '/'),
			'marks_list': marks_list
			})
		# except:
		# 	html = """
		# 	<div class="col-md-12 text-center">
		# 	    <div class="alert alert-danger" role="alert">
		# 			<h4 class="alert-heading">No Mark Format!</h4>
		# 			<hr>
		# 			<p class="mb-0">Sorry you have to create mark format <br>In settings.</p>
		# 	    </div>
		# 	</div>"""
		return HttpResponse(html)

	def template(self, num_of_col):
		return f'teacher/exam/filter/mark/mark_col{num_of_col}.html'

	def calc(self, marks):
		total_mark = 0
		for mark in marks:
			if mark:
				total_mark += int(mark)
		return [total_mark, GetGrade().get_grade(total_mark), GetGradeRemark().get_grade_remark(total_mark)]


	def formart_of_values(self, mark_format, class_room, exam):
		if class_room.the_class.the_class.lower() == 'ss2' and exam.exam_term.lower() == 'second':
			mark_sheet = ['test30', 'exam70']

		elif class_room.the_class.the_class.lower() in {'ss3', 'jss3', 'js3'} and exam.exam_term.lower() == 'third':
			mark_sheet = ['exam100']

		else:
			if mark_format == 'five_column_format':
				mark_sheet = ['resumption_test10', 'mid_test10', 'project10', 'assignment10', 'exam60']

			elif mark_format == 'four_column_format':
				mark_sheet = ['resumption_test10', 'mid_test10', 'project10', 'exam70']

			elif mark_format == 'three_column_format':
				mark_sheet = ['resumption_test15', 'mid_test15', 'exam70']

			elif mark_format == 'two_column_format':
				mark_sheet = ['test30', 'exam70']
				
		return mark_sheet

	def empties_in_list(self, num, insert_before=None):
		return [insert_before, *['']*num, 0, 'N/A', '']

