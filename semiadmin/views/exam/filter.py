from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db.models import Avg, F, Max, Min, Sum

from management import models as user_model
from student import models as student_model
from teacher import models as teacher_model
from ... import models as semiadmin_model
from ...utils import DEFAULT_IMAGE_THE_URL
from utils.html import HTML
from utils import help as help_tools

import csv
import io
import mimetypes
import os
from collections import defaultdict
# from openpyxl import Workbook, load_workbook
from xlwt import Workbook
from excel_response import ExcelResponse


class PromotionFilter(View):
	def post(self, request):
		session_from = request.POST.get('session_from')
		session_to = request.POST.get('session_to')
		class_id_from = request.POST.get('class_id_from')
		class_id_to = request.POST.get('class_id_to')
		section_id_from = request.POST.get('section_id_from')
		section_id_to = request.POST.get('section_id_to')

		session_from = student_model.Session.objects.filter(pk=session_from).first()
		session_to = student_model.Session.objects.filter(pk=session_to).first()
		
		class_room_from = student_model.Class.objects.filter(the_class=class_id_from, the_section=section_id_from).first()
		class_room_to = student_model.Class.objects.filter(the_class=class_id_to, the_section=section_id_to).first()

		students = student_model.Student.objects.filter(student_class_room=class_room_from)

		html = render(request, 'semiadmin/exam/filter/promotion.html', {'students':students,
			'session_from': session_from, 'session_to': session_to, 
			'class_room_from': class_room_from, 'class_room_to': class_room_to})
		return HttpResponse(html)


class ManageCognitiveDomainScoreFilter(View):
	def post(self, request):
		exam_id = request.POST.get('exam_id')
		class_id = request.POST.get('class_id')
		section_id = request.POST.get('section_id')

		class_room = student_model.Class.objects.filter(the_class=class_id, the_section=section_id).first()
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

		html = render(request, 'semiadmin/exam/filter/sb_description_score_manage.html', {'domain_scores':domain_scores, 'exam_id': exam_id,
			'principal_codes': principal_codes, 'teacher_codes': teacher_codes, 'housemaster_codes': housemaster_codes,
			'subject_codes': subject_codes, 'class_room': class_room, 'exam': exam})
		return HttpResponse(html)


class TabulationSheetFilter(View):
	extra_context = {}
	def tot_per_pos_re(self, data, exact_class, index_prime_subjects):
		row = 0
		scores = set()
		while row < len(data):
			res = help_tools.sum_avg(data[row][1:])
			scores.add(res[0])
			data[row].extend(res)
			row += 1

		scores_list = list(scores)
		scores_list.sort()
		scores_list.reverse()
		row = 0
		if exact_class.the_class.the_class[:-1].lower().startswith('ss'):
			subjects_to_pass = 6
		elif exact_class.the_class.the_class[:-1].lower().startswith('js'):
			subjects_to_pass = 7

		while row < len(data):
			promote_repeat = help_tools.pass_or_fail(data[row][1:-2], subjects_to_pass, index_prime_subjects=index_prime_subjects, 
				pass_mark=50, ret_pass='PROMOTE', ret_fail='REPEAT')
			position = help_tools.pos_th(scores_list.index(data[row][-2])+1)
			data[row].append(position)
			data[row].append(promote_repeat)
			row += 1
		return data

	def post_annual(self, request, exam, exact_class):
		""" IF EXAM TERM IS ANNUAL """
		exams = student_model.Exam.objects.filter(exam_session=exam.exam_session).exclude(exam_term__contains='annual')
		
		students = student_model.Student.objects.filter(student_class_room=exact_class)
		subject_pk_name = exact_class.the_class.subject.values_list('pk', 'name')

		prime_subjects = help_tools.prime_subjects()
		index_prime_subjects = []
		head_data = [[], [], []]
		data = []
		for student in students:
			data.append([student])

		head_table = []
		count_index_subjects = 0
		for subject, name in subject_pk_name:
			head_table.append(name)
			if name in prime_subjects:
				index_prime_subjects.append(count_index_subjects)
			count_index_subjects += 1
			high = 0
			low = 101
			total = 0
			count = 0
			student_arr_index = -1
			for student in students:
				student_arr_index += 1
				count += 1
				student_exams = student.mark_set.filter(exam__in=exams, subject=subject)
				if student_exams:
					student_total = 0
					for student_exam in student_exams:
						student_total += student_exam.total_mark()

					high = max(high, student_total)
					low = min(low, student_total)
					total += student_total
					data[student_arr_index].append(student_total)
				else:
					data[student_arr_index].append('-')


			avg = round(total / count, 2) if count > 0 else 0
			head_data[0].append(high)
			head_data[1].append(low if low < 101 else 0)
			head_data[2].append(avg)

		return {'head_table': head_table, 'head_data': head_data, 'data': self.tot_per_pos_re(data, exact_class, index_prime_subjects)}


	def post_term(self, request, exam, exact_class):
		""" IF EXAM TERM IS TERM """
		
		students = student_model.Student.objects.filter(student_class_room=exact_class)
		subject_pk_name = exact_class.the_class.subject.values_list('pk', 'name')

		prime_subjects = help_tools.prime_subjects()
		index_prime_subjects = []
		head_data = [[], [], []]
		data = []
		for student in students:
			data.append([student])

		head_table = []
		count_index_subjects = 0
		for subject, name in subject_pk_name:
			head_table.append(name)
			if name in prime_subjects:
				index_prime_subjects.append(count_index_subjects)
			count_index_subjects += 1
			high = 0
			low = 101
			total = 0
			count = 0
			student_arr_index = -1
			for student in students:
				student_arr_index += 1
				count += 1
				student_exam = student.mark_set.filter(exam=exam, subject=subject).first()
				if student_exam:
					student_total = student_exam.total_mark()

					high = max(high, student_total)
					low = min(low, student_total)
					total += student_total
					data[student_arr_index].append(student_total)
				else:
					data[student_arr_index].append('-')


			avg = round(total / count, 2) if count > 0 else 0
			head_data[0].append(high if low < 101 else '-')
			head_data[1].append(low if low < 101 else '-')
			head_data[2].append(avg if low < 101 else '-')

		return {'head_table': head_table, 'head_data': head_data, 'data': self.tot_per_pos_re(data, exact_class, index_prime_subjects)}

			

	def post(self, request):
		class_id = request.POST.get('class_id')
		section_id = request.POST.get('section_id')
		session_id = request.POST.get('session_id')
		exam_id = request.POST.get('exam_id')
		return self.result(request, class_id, section_id, session_id, exam_id)

	def result(self, request, class_id, section_id, session_id, exam_id, template_path='/filter/tabulation_sheet.html'):
		exact_class = student_model.Class.objects.filter(the_class=class_id, the_section=section_id).first()

		exam = student_model.Exam.objects.filter(pk=exam_id).first()
		if exam.exam_term.lower() == 'annual':
			data = self.post_annual(request, exam, exact_class)
			marks_obtainable = 300
		else:
			data = self.post_term(request, exam, exact_class) 
			marks_obtainable = 100


		html = render(request, f'semiadmin/exam{template_path}', {'class_id':class_id, 
			'section_id': section_id, 'exam_id': exam_id,
			'exact_class': exact_class,
			'data': data, 'marks_obtainable': marks_obtainable,
			'exam': exam, 'session_slash': exam.exam_session.session.replace('-', '/'),
			**self.extra_context,
			})
		return HttpResponse(html)


class TabulationSheetPrintView(TabulationSheetFilter):
	def get(self, request, class_id, section_id, exam_id):
		school_setting = semiadmin_model.SchoolSettings.objects.last()
		self.extra_context['school_setting'] = school_setting
		exam = student_model.Exam.objects.filter(pk=exam_id).first()

		return self.result(request, class_id, section_id, exam.exam_session.pk, exam_id,
			template_path='/tabulation_sheet_print_view.html')

		

class GradeAll(View):
	def get(self, request):
		tbodys = semiadmin_model.Grade.objects.all()
		html = render(request, 'semiadmin/exam/filter/grade.html', {'grades':tbodys})
		return HttpResponse(html)


class GetGrade(View):
	def get(self, request, total_mark):
		return HttpResponse(self.get_grade(total_mark))
		
	def get_grade(self, total_mark):
		grade = None
		
		if total_mark >= 80:
			grade = 'A1'

		elif total_mark >= 75:
			grade = 'B2'

		elif total_mark >= 70:
			grade = 'B3'

		elif total_mark >= 65:
			grade = 'C4'

		elif total_mark >= 60:
			grade = 'C5'

		elif total_mark >= 50:
			grade = 'C6'

		elif total_mark >= 45:
			grade = 'D7'

		elif total_mark >= 40:
			grade = 'E8'

		else:
			grade = 'F9'

		return grade


class GetGradeRemark(View):
	def get(self, request, total_mark):
		return HttpResponse(self.get_grade_remark(total_mark))

	def get_grade_remark(self, total_mark):
		remark = None
		
		if total_mark >= 80:
			remark = 'EXCELLENT'

		elif total_mark >= 75:
			remark = 'VERY GOOD'

		elif total_mark >= 70:
			remark = 'GOOD'

		elif total_mark >= 65:
			remark = 'UPPER CREDIT'

		elif total_mark >= 60:
			remark = 'CREDIT'

		elif total_mark >= 50:
			remark = 'LOWER CREDIT'

		elif total_mark >= 45:
			remark = 'PASS'

		elif total_mark >= 40:
			remark = 'PASS'

		else:
			remark = 'FAIL'

		return remark


class MarkJson(View):
	def get(self, request):
		exam_id = request.GET.get('exam_id')
		class_id = request.GET.get('class_id')
		section_id = request.GET.get('section_id')
		subject_id = request.GET.get('subject_id')
		session_id = request.GET.get('session_id')
		html = ''
		try:
			exam = student_model.Exam.objects.filter(pk=exam_id).first()
		except:
			return HttpResponse(html)
		else:
			if exam:
				pass
			else:
				return HttpResponse(html)

		class_room = student_model.Class.objects.filter(the_class=class_id, the_section=section_id).first()
		subject = student_model.Subject.objects.filter(name=subject_id).first()
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
				fnd.insert(0, student.name)
				marks_list.append(fnd)
			else:
				marks_list.append(self.empties_in_list(len(format_values), student.name))

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



		theads = ['Student name', *mark_sheet]

		# book = Workbook(encoding='utf-8')
		# sheet = book.add_sheet('User data')
		# row = 0
		# for col in range(len(theads)):
		# 	sheet.write(row, col, theads[col])

		# for i, line in enumerate(marks_list):
		# 	for j, ms in enumerate(line):
		# 		sheet.write(i+1, j, marks_list[i][j])

		# response = HttpResponse(content_type='application/ms-excel')
		# response['Content-Disposition'] = 'attachment; filename="student_mark_excel.xls"'
		# print(response)
		# book.save(response)
		# return response


		marks_list.insert(0, theads)
		# marks_list = [
		# 	['aaa', 'bbb'],
		# 	[2, 3],
		# 	[9, 8]
		# ]
		print(marks_list)
		return ExcelResponse(marks_list, 'ssss')

		# name = 'aaaa.xlsx'
		# help_tools.write_excel(name, marks_list)

		# print([i for i in help_tools.read_excel(name)])
		# print([i for i in help_tools.read_excel(name)])
		# print([i for i in help_tools.read_excel(name)])

		# response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
		# # response = HttpResponse(content_type='application/ms-excel')

		# response['Content-Disposition'] = f'attachment; filename="{name}"'
		
		# return response

		


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
		return [insert_before, *['']*num]





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
		session = semiadmin_model.Session.objects.filter(pk=session_id).first()
		mark_sheet_format = semiadmin_model.MarkSheetFormat.objects.filter(category=class_id[:-1], session=session).first()
		students = student_model.Student.objects.filter(student_class_room=class_room).all()

		students_pk = student_model.Student.objects.filter(student_class_room=class_room).values_list('pk')
		students_pk = [i[0] for i in students_pk]
		try:
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
		except:
			html = """
			<div class="col-md-12 text-center">
			    <div class="alert alert-danger" role="alert">
					<h4 class="alert-heading">No Mark Format!</h4>
					<hr>
					<p class="mb-0">Sorry you have to create mark format <br>In settings.</p>
			    </div>
			</div>"""
		return HttpResponse(html)

	def template(self, num_of_col):
		return f'semiadmin/exam/filter/mark/mark_col{num_of_col}.html'

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


class ExamTerm(View):
	def get(self, request, session_id):
		session_id = student_model.Session.objects.filter(pk=session_id).first()
		terms = student_model.Exam.objects.filter(exam_session=session_id).values_list('pk', 'exam_term')

		html = HTML()
		select = html.select(name="exam", id="exam_id", klass="form-control select2 select2-hidden-accessible", data_toggle="select2", required="", data_select2_id="exam_id", tabindex="-1", aria_hidden="true")
		for term in terms:
			select.option(term[1], value=str(term[0]), data_select2_id=term[1].upper())
		
		return HttpResponse(html)


class ExamTermNoAnnual(View):
	def get(self, request, session_id):
		session_id = student_model.Session.objects.filter(pk=session_id).first()
		terms = student_model.Exam.objects.filter(exam_session=session_id).values_list('pk', 'exam_term')

		html = HTML()
		select = html.select(name="exam", id="exam_id", klass="form-control select2 select2-hidden-accessible", data_toggle="select2", required="", data_select2_id="exam_id", tabindex="-1", aria_hidden="true")
		for term in terms:
			if term[1].lower() == 'annual':
				continue
			select.option(term[1], value=str(term[0]), data_select2_id=term[1].upper())
		
		return HttpResponse(html)



class HousemasterCommentCodeAll(View):
	def get(self, request):
		tbodys = semiadmin_model.HousemasterCommentCode.objects.all()
		html = render(request, 'semiadmin/exam/filter/housemaster_comment_code.html', {'housemaster_comment_codes':tbodys})
		return HttpResponse(html)


class CognitiveKeyDomainScoreAll(View):
	def get(self, request):
		tbodys = semiadmin_model.CognitiveKeyDomainScore.objects.all()
		html = render(request, 'semiadmin/exam/filter/cognitive_key_domain_score.html', {'cognitive_key_domain_scores':tbodys})
		return HttpResponse(html)


class PrincipalSubjectCodeAll(View):
	def get(self, request):
		tbodys = semiadmin_model.PrincipalSubjectCode.objects.all()
		html = render(request, 'semiadmin/exam/filter/principal_subject_code.html', {'principal_subject_codes':tbodys})
		return HttpResponse(html)


class TeacherCommentCodeAll(View):
	def get(self, request):
		tbodys = semiadmin_model.TeacherCommentCode.objects.all()
		html = render(request, 'semiadmin/exam/filter/teacher_comment_code.html', {'teacher_comment_codes':tbodys})
		return HttpResponse(html)


class PrincipalCommentCodeAll(View):
	def get(self, request):
		tbodys = semiadmin_model.PrincipalCommentCode.objects.all()
		html = render(request, 'semiadmin/exam/filter/principal_comment_code.html', {'principal_comment_codes':tbodys})
		return HttpResponse(html)


class ManageCognitiveDomainAll(View):
	def get(self, request):
		tbodys = semiadmin_model.ManageCognitiveDomain.objects.all()
		html = render(request, 'semiadmin/exam/filter/sb_description.html', {'sb_descriptions':tbodys})
		return HttpResponse(html)


class PassMarkAll(View):
	def get(self, request):
		tbodys = student_model.PassMark.objects.all()
		html = render(request, 'semiadmin/exam/filter/pass_mark.html', {'pass_marks':tbodys})
		return HttpResponse(html)


class ManageExaminationAll(View):
	def get(self, request):
		tbodys = student_model.Exam.objects.all()
		html = render(request, 'semiadmin/exam/filter/exam.html', {'exams':tbodys})
		return HttpResponse(html)

