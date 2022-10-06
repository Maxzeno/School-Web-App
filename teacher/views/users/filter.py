from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.db.models import Max, Min

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

# students = student_model.Student.objects.extra()

class ResultFilter(View):
	def get(self, request, id, exam):
		the_exam = student_model.Exam.objects.filter(pk=exam).first()
		if the_exam.exam_term.lower() == 'annual':
			html = self.get_annual(request, id, exam)
			return HttpResponse(html)
		else:
			html = self.get_term(request, id, exam)
			return HttpResponse(html)

	def get_annual(self, request, id, exam):
		school_setting = semiadmin_model.SchoolSettings.objects.last()
		the_exam = student_model.Exam.objects.filter(pk=exam).first()
		student = student_model.Student.objects.filter(pk=id.replace('-', '/')).first()
		subjects = student_model.JustClass.objects.filter(pk=student.student_class_room.the_class.the_class).first().subject.all()
		class_count = student_model.Student.objects.filter(student_class_room=student.student_class_room).count()

		exams = student_model.Exam.objects.filter(exam_session=the_exam.exam_session)
		student_domain = self.get_domain_annual(the_exam.exam_session, student)

		mat2d = []
		for subject in subjects:
			perm = help_tools.subject_perm(request, student.student_class_room, subject)
			if not perm:
				continue

			mat1d = [subject.name]
			total = 0
			count = 0
			empty_score_num = 0
			for exam in exams:
				if count >= 3:
					break
				if exam.exam_term.lower() == 'annual':
					continue
				try:
					mark = semiadmin_model.Mark.objects.filter(student=student, subject=subject, exam=exam).first()
					score = mark.total_mark()
				except AttributeError:
					score = 0
				count += 1
				total += score
				if score > 0:
					mat1d.append(score)
				else:
					if mark and mark.missed_subject():
						empty_score_num += 1
						mat1d.append('')
					elif not mark:
						empty_score_num += 1
						mat1d.append('')
					else:
						mat1d.append(0)

			if count < 3:
				blank = []
				for _ in range(3-count):
					blank.append('')
				mat1d.extend(blank)

			if empty_score_num < count:
				mat1d.extend([total, round(total/count, 1)])
				mat1d.extend(self.get_class_avg_pos_annual(subject, student.student_class_room, exam.exam_session, total))
				mat1d.extend([GetGrade().get_grade(total), GetGradeRemark().get_grade_remark(total)])
				mat2d.append(mat1d)
		num_subjects = len(mat2d)
		class_student_avg_total_pos_annual = self.get_class_student_avg_total_pos_annual(student.student_class_room, 
			exam.exam_session, student, num_subjects)
		html = render(request, 'teacher/users/filter/result_annual.html', {'mat2d': mat2d,
			'class_student_avg_total_pos_annual': class_student_avg_total_pos_annual,
			'student_domain': student_domain, 'school_setting': school_setting,
			'class_count': class_count, 'student': student, 'exam': the_exam, 'codes': self.get_code(the_exam.exam_session, student)})
		return html

	def get_code(self, exam_session, student):
		exams = student_model.Exam.objects.filter(exam_session=exam_session)
		principal_code = '-'
		teacher_code = '-'
		for exam in exams:
			if exam.exam_term.lower() == 'annual':
				continue
			domain = semiadmin_model.StudentDomainScore.objects.filter(exam=exam, student=student).first()
			if domain and domain.principal_code: 
				principal_code = domain.principal_code.code_description

			if domain and domain.teacher_code:
				teacher_code = domain.teacher_code.code_description

		return principal_code, teacher_code



	def get_domain_annual(self, exam_session, student, num_domain_types=13):
		exams = student_model.Exam.objects.filter(exam_session=exam_session)
		domains = []

		for exam in exams:
			# if exam.exam_term.lower() == 'annual':
			# 	continue

			student_domain = semiadmin_model.StudentDomainScore.objects.filter(exam=exam, student=student).values_list(
				'honesty', 'neatness', 'punctuality', 'attentiveness_in_class', 'organizational_ability', 'perseverance', 
				'self_control', 'arts_and_crafts', 'drawing_and_painting', 'labour_and_workshop', 
				'fluency', 'sport_and_gymnastics', 'handwriting') #, flat=True)
			if student_domain:
				domains.append(student_domain[0])
			
		new = []
		if domains:
			len_domain = len(domains)
			for i in range(num_domain_types):
				domain_sum = None
				for domain_list in domains:
					try:
						domain_sum += domain_list[i] if isinstance(domain_list[i], int) else '-' if domain_sum is None else 0
					except:
						domain_sum = domain_list[i]
				new.append(round(domain_sum/len_domain) if domain_sum is not None else 0)
		else:
			new = ['-'] * num_domain_types

		name_domains = ['honesty', 'neatness', 'punctuality', 'attentiveness_in_class', 'organizational_ability', 'perseverance', 
			'self_control', 'arts_and_crafts', 'drawing_and_painting', 'labour_and_workshop', 
			'fluency', 'sport_and_gymnastics', 'handwriting']
		data = {}
		for i in range(len(name_domains)):
			data[name_domains[i]] = new[i]
		return data



	def get_class_student_avg_total_pos_annual(self, class_room, exam_session, the_student, num_subjects):
		students = student_model.Student.objects.filter(student_class_room=class_room)
		exams = student_model.Exam.objects.filter(exam_session=exam_session)

		student_total = 0
		count = 0
		scores = set()
		for student in students:
			count += 1
			exam_total = 0
			for exam in exams:
				if exam.exam_term.lower() == 'annual':
					continue
				marks = semiadmin_model.Mark.objects.filter(exam=exam, student=student)
				mark_total = 0
				for mark in marks:
					mark_total += mark.total_mark()
				exam_total += mark_total
			student_total += exam_total
			scores.add(exam_total)
		class_avg = round(student_total/count, 2)

		student_exam_total = 0
		index_prime_subjects = []
		arr_mark = []
		for exam in exams:
			if exam.exam_term.lower() == 'annual':
				continue
			student_marks = semiadmin_model.Mark.objects.filter(exam=exam, student=the_student)
			student_mark_total = 0

			for index, student_mark in enumerate(student_marks):
				if student_mark.subject.name.lower() in help_tools.prime_subjects():
					index_prime_subjects.append(index)
				student_mark_total += student_mark.total_mark()
			student_exam_total += student_mark_total
			arr_mark.append(student_mark_total)
		student_avg = round(student_exam_total/num_subjects, 2) if num_subjects > 0 else 0

		if student.student_class_room.the_class.the_class[:-1].lower().startswith('ss'):
			subjects_to_pass = 6
		elif student.student_class_room.the_class.the_class[:-1].lower().startswith('js'):
			subjects_to_pass = 7

		pass_or_fail = help_tools.pass_or_fail(arr_mark, subjects_to_pass, index_prime_subjects)
		promoted_repeat = ''
		if pass_or_fail.lower() == 'pass':
			promoted_repeat = 'promoted'
		elif pass_or_fail.lower() == 'fail':
			promoted_repeat = 'repeat'

		scores_list = list(scores)
		scores_list.sort()
		scores_list.reverse()
		student_position = self.pos_th(scores_list.index(student_exam_total)+1)

		mark_obtained = f'{student_exam_total} / {num_subjects*100}'

		attended = semiadmin_model.Attendance.objects.filter(the_class=the_student.student_class_room, 
			student=the_student, attended=True).count()
		attendance = semiadmin_model.Attendance.objects.filter(the_class=the_student.student_class_room).count()
		class_attendance = f'{(attended/attendance)*100}%' if attendance > 0 else '-'

		return [num_subjects, student_position, mark_obtained, student_avg, class_avg, class_attendance, promoted_repeat]


	def get_class_avg_pos_annual(self, subject, class_room, exam_session, student_score):
		students = student_model.Student.objects.filter(student_class_room=class_room)
		exams = student_model.Exam.objects.filter(exam_session=exam_session)
		
		total = 0
		count = 0
		scores = set()
		for student in students:
			count += 1
			term_total = 0
			term_count = 0
			for exam in exams:
				# the exam with term annual is normally empty
				if exam.exam_term.lower() == 'annual':
					continue
				mark = semiadmin_model.Mark.objects.filter(exam=exam, subject=subject, student=student).first()
				try:
					term_total += mark.total_mark()
				except AttributeError:
					term_total += 0
				term_count += 1

			total += term_total
			scores.add(term_total)
		avg = round(total/count, 1)

		scores_list = list(scores)
		scores_list.sort()
		scores_list.reverse()
		subject_position = scores_list.index(student_score)+1

		return [avg, self.pos_th(subject_position)]


	def pos_th(self, val):
		if val == 1:
			return f'{val}st'
		elif val == 2:
			return f'{val}nd'
		elif val == 3:
			return f'{val}rd'
		else:
			return f'{val}th'


	def get_term(self, request, id, exam):
		school_setting = semiadmin_model.SchoolSettings.objects.last()

		exam = student_model.Exam.objects.filter(pk=exam).first()
		student = student_model.Student.objects.filter(pk=id.replace('-', '/')).first()
		students = student_model.Student.objects.filter(student_class_room=student.student_class_room.pk)
		class_count = students.count()
		student_domain = semiadmin_model.StudentDomainScore.objects.filter(exam=exam, student=student).first()

		attended = semiadmin_model.Attendance.objects.filter(the_class=student.student_class_room, 
			student=student, attended=True).count()
		attendance = semiadmin_model.Attendance.objects.filter(the_class=student.student_class_room).count()

		student_mark = student.mark_set.filter(exam=exam)
		mark_obtained = 0
		count = 0
		for one_mark in student_mark:
			mark_obtained += one_mark.total_mark()
			count += 1

		student_avg = mark_obtained/count if count > 0 else 0
		mark_obtainable = count * 100

		all_total = 0
		all_total_list = []
		for i in students:
			all_subject_mark = semiadmin_model.Mark.objects.filter(exam=exam, class_room=student.student_class_room.pk, student=i)
			subject_total = 0
			for j in all_subject_mark:
				subject_total += j.total_mark()
			all_total += subject_total
			all_total_list.append(subject_total)

		class_pos = list(set(all_total_list))
		class_pos.sort()
		class_pos.reverse()

		mark_format = semiadmin_model.MarkSheetFormat.objects.filter(session=exam.exam_session, 
			category=student.student_class_room.the_class.the_class[:-1]).first().mark_format

		if student.student_class_room.the_class.the_class[:-1].lower().startswith('ss'):
			subjects_to_pass = 6
		elif student.student_class_room.the_class.the_class[:-1].lower().startswith('js'):
			subjects_to_pass = 7

		student_subjects_marks = student.mark_set.filter(exam=exam)
		arr_mark = []
		index_prime_subjects = []
		for index, i in enumerate(student_subjects_marks):
			arr_mark.append(i.total_mark())
			if i.subject.name.lower() in help_tools.prime_subjects():
				index_prime_subjects.append(index)

		pass_or_fail = help_tools.pass_or_fail(arr_mark, subjects_to_pass, index_prime_subjects)


		""" ADDED LOGIC TO SS2 SS3/JSS3"""

		if student.student_class_room.the_class.the_class.lower() == 'ss2' and exam.exam_term.lower() == 'second':
			data_keys = ['subject_id', 'test30', 'exam70']
			theads = ['Subject', 'Test (30)', 'Exam.']

		elif student.student_class_room.the_class.the_class.lower() in {'ss3', 'jss3', 'js3'} and exam.exam_term.lower() == 'third':
			data_keys = ['subject_id', 'exam100']
			theads = ['Subject', 'Exam.']

		else:
			if mark_format == 'five_column_format':
				data_keys = ['subject_id', 'resumption_test10', 'mid_test10', 'project10', 'assignment10', 'exam60']
				theads = ['Subject', 'Resumption Test (10)', 'Mid-Term Test (10)', 'Project (10)', 'Assignment (10)', 'Exam.']

			elif mark_format == 'four_column_format':
				data_keys = ['subject_id', 'resumption_test10', 'mid_test10', 'project10', 'exam70']
				theads = ['Subject', 'Resumption Test (10)', 'Mid-Term Test (10)', 'Project (10)', 'Exam.']

			elif mark_format == 'three_column_format':
				data_keys = ['subject_id', 'resumption_test15', 'mid_test15', 'exam70']
				theads = ['Subject', 'Resumption Test (15)', 'Mid-Term Test (15)', 'Exam.']

			elif mark_format == 'two_column_format':
				data_keys = ['subject_id', 'test30', 'exam70']
				theads = ['Subject', 'Test (30)', 'Exam.']

		marks = student.mark_set.filter(exam=exam).values_list(*data_keys)
		marks = self.get_tot_grade_term(marks, exam, student, request)

		html = render(request, 'teacher/users/filter/result_term.html', {'marks': marks,
			'theads': theads, 'student_and_exam': [student,  exam],
			'school_setting': school_setting, 'student': student, 'exam': exam, 'class_count': class_count,
			'subject_count': len(marks), 'student_domain': student_domain, 
			'class_attendance': (attended/attendance)*100 if attendance > 0 else 0,
			'mark_obtained': mark_obtained, 'mark_obtainable': mark_obtainable, 'student_avg': student_avg,
			'class_avg': all_total/class_count if class_count > 0 else 0,
			'pass_or_fail': pass_or_fail, 'class_position': f"{self.pos_th(class_pos.index(mark_obtained)+1)}",})
		return html

	def get_tot_grade_term(self, marks, exam, student, request=None):
		marks = list(marks)
		for index in range(len(marks)):
			subject = student_model.Subject.objects.filter(pk=marks[index][0]).first()
			perm = help_tools.subject_perm(request, student.student_class_room, subject)
			if not perm:
				del marks[index]
				continue

			mark_sum = 0
			marks[index] = list(marks[index])
			subject_id = marks[index][0]
			marks[index][0] = student_model.Subject.objects.filter(pk=subject_id).first().name
			for i in marks[index][1:]:
				if isinstance(i, int):
					mark_sum += i

			marks[index].extend([mark_sum, *self.get_high_low_pos_term(exam, subject_id, mark_sum), 
				GetGrade().get_grade(mark_sum), GetGradeRemark().get_grade_remark(mark_sum)])

		return marks

	def get_high_low_pos_term(self, exam, subject, student_score):
		marks = semiadmin_model.Mark.objects.filter(exam=exam, subject=subject)
		high = 0
		low = 100
		scores = set()
		for mark in marks:
			high = max(high, mark.total_mark())
			low = min(low, mark.total_mark())
			scores.add(mark.total_mark())

		scores_list = list(scores)
		scores_list.sort()
		scores_list.reverse()
		position = self.pos_th(scores_list.index(student_score)+1)
		return [high, low, position]


	def get_annual_light(self, request, id, the_exam):
		student = student_model.Student.objects.filter(pk=id.replace('-', '/')).first()
		subjects = student_model.JustClass.objects.filter(pk=student.student_class_room.the_class.the_class).first().subject.all()

		exams = student_model.Exam.objects.filter(exam_session=the_exam.exam_session)

		mat2d = []
		for subject in subjects:
			perm = help_tools.subject_perm(request, student.student_class_room, subject)
			if not perm:
				continue

			mat1d = [subject.name]
			total = 0
			count = 0
			empty_score_num = 0
			for exam in exams:
				if count >= 3:
					break
				if exam.exam_term.lower() == 'annual':
					continue
				try:
					mark = semiadmin_model.Mark.objects.filter(student=student, subject=subject, exam=exam).first()
					score = mark.total_mark()
				except AttributeError:
					score = 0
				count += 1
				total += score
				if score > 0:
					mat1d.append(score)
				else:
					if mark and mark.missed_subject():
						empty_score_num += 1
						mat1d.append('')
					elif not mark:
						empty_score_num += 1
						mat1d.append('')
					else:
						mat1d.append(0)

			if count < 3:
				blank = []
				for _ in range(3-count):
					blank.append('')
				mat1d.extend(blank)

			if empty_score_num < count:
				mat1d.extend([total, round(total/count, 1)])
				mat1d.extend(self.get_class_avg_pos_annual(subject, student.student_class_room, exam.exam_session, total))
				mat1d.extend([GetGrade().get_grade(total), GetGradeRemark().get_grade_remark(total)])
				mat2d.append(mat1d)

		return [the_exam.pk, the_exam.exam_term.lower(), the_exam], mat2d

	def get_tot_grade_term_light(self, marks, exam, student, request=None):
		marks = list(marks)

		for index in range(len(marks)):
			subject = student_model.Subject.objects.filter(pk=marks[index][0]).first()
			perm = help_tools.subject_perm(request, student.student_class_room, subject)
			if not perm:
				del marks[index]
				continue

			mark_sum = 0
			marks[index] = list(marks[index])
			subject_id = marks[index][0]
			marks[index][0] = student_model.Subject.objects.filter(pk=subject_id).first().name
			for i in marks[index][1:]:
				if isinstance(i, int):
					mark_sum += i

			marks[index].extend([mark_sum, GetGrade().get_grade(mark_sum), GetGradeRemark().get_grade_remark(mark_sum)])

		return marks


	def get_term_light(self, request, id, exam):
		student = student_model.Student.objects.filter(pk=id.replace('-', '/')).first()

		mark_format = semiadmin_model.MarkSheetFormat.objects.filter(session=exam.exam_session, 
			category=student.student_class_room.the_class.the_class[:-1]).first().mark_format


		""" ADDED LOGIC TO SS2 SS3/JSS3"""

		if student.student_class_room.the_class.the_class.lower() == 'ss2' and exam.exam_term.lower() == 'second':
			data_keys = ['subject_id', 'test30', 'exam70']
			theads = ['Subject', 'Test (30)', 'Exam.', 
				'Total (100)', 'Grade', 'Remark']

		elif student.student_class_room.the_class.the_class.lower() in {'ss3', 'jss3', 'js3'} and exam.exam_term.lower() == 'third':
			data_keys = ['subject_id', 'exam100']
			theads = ['Subject', 'Exam.', 
				'Total (100)', 'Grade', 'Remark']

		else:
			if mark_format == 'five_column_format':
				data_keys = ['subject_id', 'resumption_test10', 'mid_test10', 'project10', 'assignment10', 'exam60']
				theads = ['Subject', 'Resumption Test (10)', 'Mid-Term Test (10)', 'Project (10)', 'Assignment (10)', 'Exam.', 
					'Total (100)', 'Grade', 'Remark']

			elif mark_format == 'four_column_format':
				data_keys = ['subject_id', 'resumption_test10', 'mid_test10', 'project10', 'exam70']
				theads = ['Subject', 'Resumption Test (10)', 'Mid-Term Test (10)', 'Project (10)', 'Exam.', 
					'Total (100)', 'Grade', 'Remark']

			elif mark_format == 'three_column_format':
				data_keys = ['subject_id', 'resumption_test15', 'mid_test15', 'exam70']
				theads = ['Subject', 'Resumption Test (15)', 'Mid-Term Test (15)', 'Exam.', 
					'Total (100)', 'Grade', 'Remark']

			elif mark_format == 'two_column_format':
				data_keys = ['subject_id', 'test30', 'exam70']
				theads = ['Subject', 'Test (30)', 'Exam.', 
					'Total (100)', 'Grade', 'Remark']



		marks = student.mark_set.filter(exam=exam).values_list(*data_keys)
		marks = self.get_tot_grade_term_light(marks, exam, student, request)

		return [exam.pk, exam.exam_term.lower(), exam], theads, marks



class MarksheetFilter(ResultFilter):
	def get(self, request, id, session):
		student = student_model.Student.objects.filter(pk=id.replace('-', '/')).first()
		session = student_model.Session.objects.filter(pk=session).first()
		exams = student_model.Exam.objects.filter(exam_session=session).all()
		heavy = []
		for exam in exams:
			if exam.exam_term.lower() == 'annual':
				heavy.append(self.get_annual_light(request, id, exam))
			else:
				heavy.append(self.get_term_light(request, id, exam))

		html = render(request, 'teacher/users/filter/marksheet.html', {'heavy': heavy, 'student_id': id})
		return HttpResponse(html)
		


class StudentFilter(View):
	def get(self, request, student_class, student_class_room):
		the_class = student_model.Class.objects.filter(the_class=student_class.upper(), 
			the_section=student_class_room.upper()).first()

		perm = help_tools.class_perm(request, the_class)
		if not perm:
			return help_tools.perm_not()

		students = student_model.Student.objects.filter(student_class_room=the_class).all()

		new_students = []
		for student in students:
			try:
				img_url = student.get_photo()
			except:
				img_url = DEFAULT_IMAGE_THE_URL
			new_students.append([student.student_id, img_url, student.name, student.mark_set.count() > 0, student.student_id.replace('/', '-')])

		theads = ['Srno.', 'Student id', 'Photo', 'Name', 'Result', 'Options']

		data = {
			'theads':theads,
			'tbodys':new_students,
			 'student_class': student_class, 
			 'student_class_room': student_class_room
			}
		html = render(request, 'teacher/users/filter/student.html', data)
		return HttpResponse(html)
		
