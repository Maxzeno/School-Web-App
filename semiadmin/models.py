from django.db import models
from django.core.exceptions import ValidationError
from student.models import Class, Subject, Session, Exam, Student
from teacher.models import Teacher, Department
from django.utils import timezone
from management.models import User


# Create your models here.


class Promotion(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, related_name='student_set')
	current_session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, related_name='current_session_set')
	next_session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, related_name='next_session_set')
	promoting_from = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, related_name='promoting_from_set')
	promoting_to = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, related_name='promoting_to_set')


class Noticeboard(models.Model):
	notice_title = models.CharField(max_length=255, blank=True)
	excerpts = models.CharField(max_length=255, blank=True)
	notice = models.TextField(max_length=10000, blank=True)
	show_on_website = models.BooleanField(default=True, null=True, blank=True)
	notice_photo = models.ImageField(upload_to='images/', blank=True, null=True)
	the_date = models.DateField(default=timezone.now, blank=True, null=True)

	def date_slash(self):
		the_date = self.the_date
		if the_date:
			return f'{the_date.month}/{the_date.day}/{the_date.year}'
		return ''


class Attendance(models.Model):
	attended = models.BooleanField(default=True, null=True, blank=True)
	the_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
	student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
	the_date = models.DateField(default=timezone.now, blank=True)


class Syllabus(models.Model):
	title = models.CharField(max_length=255, blank=True)
	the_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
	file = models.FileField(upload_to='files/', blank=True, null=True) # syllabus file
	the_date = models.DateField(default=timezone.now, blank=True)

	def getfile(self):
		if self.file:
			return self.file.url
		return 'javascript:void(0);'


class Routine(models.Model):
	the_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
	day = models.CharField(max_length=255, blank=True) # sunday, monday etc
	starting_hour = models.CharField(max_length=255, blank=True)
	starting_minute = models.CharField(max_length=255, blank=True)
	ending_hour = models.CharField(max_length=255, blank=True)
	ending_minute = models.CharField(max_length=255, blank=True)


class EventCalendar(models.Model):
	title = models.CharField(max_length=255, blank=True)
	starting_date = models.DateField(default=timezone.now, blank=True)
	ending_date = models.DateField(default=timezone.now, blank=True)
	
	def date_slash(self):
		starting_date = self.starting_date
		ending_date = self.ending_date
		if starting_date and ending_date:
			return f'{starting_date.month}/{starting_date.day}/{starting_date.year}', 
			f'{ending_date.month}/{ending_date.day}/{ending_date.year}'

		elif starting_date:
			return f'{starting_date.month}/{starting_date.day}/{starting_date.year}', ''

		elif ending_date:
			return f'{ending_date.month}/{ending_date.day}/{ending_date.year}', ''

		return '', ''
	
	
class Invoice(models.Model):
	the_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
	student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
	invoice_title = models.CharField(max_length=255, blank=True)
	total_amount = models.IntegerField(blank=True)
	paid_amount = models.IntegerField(blank=True)
	status = models.CharField(max_length=255, blank=True)
	the_date = models.DateField(auto_now_add=True, blank=True)

	
class ExpenseCategory(models.Model):
	name = models.CharField(max_length=255, blank=True)


class Expense(models.Model):
	expense_category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE, null=True)
	amount = models.IntegerField(blank=True)
	the_date = models.DateField(default=timezone.now, blank=True)

	def date_slash(self):
		the_date = self.the_date
		if the_date:
			return f'{the_date.month}/{the_date.day}/{the_date.year}'
		return ''
	

class Book(models.Model):
	book_name = models.CharField(max_length=255, blank=True)
	author = models.CharField(max_length=255, blank=True)
	number_of_copy = models.IntegerField(blank=True)
	

class BookIssue(models.Model):
	the_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
	student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
	book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
	status = models.CharField(max_length=255, blank=True, default='pending')
	issue_date = models.DateField(blank=True)

	def date_slash(self):
		the_date = self.issue_date
		if the_date:
			return f'{the_date.month}/{the_date.day}/{the_date.year}'
		return ''
	
	
class Grade(models.Model):
	grade = models.CharField(max_length=255, blank=True)
	grade_point = models.CharField(max_length=255, blank=True)
	mark_from = models.CharField(max_length=255, blank=True)
	mark_upto = models.CharField(max_length=255, blank=True)
	remarks = models.CharField(max_length=255, blank=True)
	

class HousemasterCommentCode(models.Model):
	category = models.CharField(max_length=255, blank=True)
	code_number = models.CharField(max_length=255, blank=True)
	code_description = models.CharField(max_length=255, blank=True)
	

class CognitiveKeyDomainScore(models.Model):
	key = models.CharField(max_length=255, blank=True)
	score = models.IntegerField(blank=True)
	

class PrincipalSubjectCode(models.Model):
	category = models.CharField(max_length=255, blank=True)
	subject_code = models.CharField(max_length=255, blank=True)
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
	

class TeacherCommentCode(models.Model):
	category = models.CharField(max_length=255, blank=True)
	code_number = models.CharField(max_length=255, blank=True)
	code_description = models.CharField(max_length=255, blank=True)
	

class PrincipalCommentCode(models.Model):
	category = models.CharField(max_length=255, blank=True)
	code_number = models.CharField(max_length=255, blank=True)
	code_description = models.CharField(max_length=255, blank=True)


class ManageCognitiveDomain(models.Model):
	sb_type = models.CharField(max_length=255, blank=True)
	description = models.CharField(max_length=255, blank=True)


class StudentDomainScore(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)	
	exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True, blank=True)
	subject_code = models.ManyToManyField(PrincipalSubjectCode, blank=True)	
	principal_code = models.ForeignKey(PrincipalCommentCode, on_delete=models.CASCADE, null=True, blank=True)	
	teacher_code = models.ForeignKey(TeacherCommentCode, on_delete=models.CASCADE, null=True, blank=True)	
	housemaster_code = models.ForeignKey(HousemasterCommentCode, on_delete=models.CASCADE, null=True, blank=True)	
	honesty = models.IntegerField(null=True, blank=True)
	neatness = models.IntegerField(null=True, blank=True)
	punctuality = models.IntegerField(null=True, blank=True)
	attentiveness_in_class = models.IntegerField(null=True, blank=True)
	organizational_ability = models.IntegerField(null=True, blank=True)
	perseverance = models.IntegerField(null=True, blank=True)
	self_control = models.IntegerField(null=True, blank=True)
	arts_and_crafts = models.IntegerField(null=True, blank=True)
	drawing_and_painting = models.IntegerField(null=True, blank=True)
	labour_and_workshop = models.IntegerField(null=True, blank=True)
	fluency = models.IntegerField(null=True, blank=True)
	sport_and_gymnastics = models.IntegerField(null=True, blank=True)
	handwriting = models.IntegerField(null=True, blank=True)


class SubjectPermission(models.Model):
	the_exact_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
	the_subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
	the_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
	exam = models.BooleanField(default=False)
	assignment = models.BooleanField(default=False)
	mid_term = models.BooleanField(default=False)
	attendance = models.BooleanField(default=False)
	online_exam = models.BooleanField(default=False)


class MarkSheetFormat(models.Model):
	category = models.CharField(max_length=255, blank=True) # pry, jss, ss
	session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
	mark_format = models.CharField(max_length=255, blank=True)

	# class Meta:
	# 	unique_together = ('category', 'session', 'mark_format')
	# 	constraints = [
	# 		models.CheckConstraint(
	# 			name = 'check_mark_format',
	# 			check=(
	# 				models.Q(
	# 					mark_format='two_column_format'
	# 					) |
	# 				models.Q(
	# 					mark_format='three_column_format'
	# 					) |
	# 				models.Q(
	# 					mark_format='four_column_format'
	# 					) |
	# 				models.Q(
	# 					mark_format='five_column_format'
	# 					) |
	# 				models.Q(
	# 					mark_format=''
	# 					)

	# 				),
	# 			)
	# 	]

	def __str__(self):
		if self.session:
			return self.mark_format + ' - ' + self.category + ' - ' + self.session.session
		return self.mark_format + ' - ' + self.category + ' - '


class SchoolSettings(models.Model):
	school_name = models.CharField(max_length=255, blank=True)
	phone = models.CharField(max_length=150, blank=True)
	address = models.TextField(max_length=2000, blank=True)
	marksheet_format_entrys = models.ManyToManyField(MarkSheetFormat, blank=True)



class Mark(models.Model):
	exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True, blank=True)
	class_room = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
	student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
	mark_sheet_format = models.ForeignKey(MarkSheetFormat, on_delete=models.CASCADE, null=True, blank=True)
	comment = models.CharField(max_length=255, null=True, blank=True)
	resumption_test10 = models.IntegerField(null=True, blank=True)
	resumption_test15 = models.IntegerField(null=True, blank=True)
	mid_test10 = models.IntegerField(null=True, blank=True)
	mid_test15 = models.IntegerField(null=True, blank=True)
	project10 = models.IntegerField(null=True, blank=True)
	assignment10 = models.IntegerField(null=True, blank=True)
	test30 = models.IntegerField(null=True, blank=True)
	exam70 = models.IntegerField(null=True, blank=True)
	exam60 = models.IntegerField(null=True, blank=True)
	exam100 = models.IntegerField(null=True, blank=True)

	def ca40_exam60(self):
		ca40 = 0
		ca40 += self.resumption_test10 if self.resumption_test10 else 0
		ca40 += self.mid_test10 if self.mid_test10 else 0
		ca40 += self.project10 if self.project10 else 0
		ca40 += self.assignment10 if self.assignment10 else 0
		return [ca40, self.exam60 if self.exam60 != None else '']

	def ca30_exam70(self):
		total = 0
		total += self.resumption_test10 if self.resumption_test10 else 0
		total += self.mid_test10 if self.mid_test10 else 0
		ca30 += self.project10 if self.project10 else 0
		return [ca30, self.exam70 if self.exam70 != None else '']

	def total_mark(self):
		total = 0
		total += self.resumption_test10 if self.resumption_test10 else 0
		total += self.resumption_test15 if self.resumption_test15 else 0
		total += self.mid_test10 if self.mid_test10 else 0
		total += self.mid_test15 if self.mid_test15 else 0
		total += self.project10 if self.project10 else 0
		total += self.assignment10 if self.assignment10 else 0
		total += self.test30 if self.test30 else 0
		total += self.exam70 if self.exam70 else 0
		total += self.exam60 if self.exam60 else 0
		total += self.exam100 if self.exam100 else 0
		return total

	def missed_subject(self):
		if self.resumption_test10 is not None:
			return False
		elif self.resumption_test15 is not None:
			return False
		elif self.mid_test10 is not None:
			return False
		elif self.mid_test15 is not None:
			return False
		elif self.project10 is not None:
			return False
		elif self.assignment10 is not None:
			return False
		elif self.test30 is not None:
			return False
		elif self.exam70 is not None:
			return False
		elif self.exam60 is not None:
			return False
		elif self.exam100 is not None:
			return False
		else:
			return True

	def get_grade(self):
		grade = None
		total_mark = self.total_mark()
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


	def get_grade_remark(self):
		remark = None
		total_mark = self.total_mark()
		
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


	def __str__(self):
		return f"{self.exam.exam_session.session} {self.exam.exam_term} {self.class_room.the_class} {self.total_mark()}"


class SemiAdmin(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='semiadmin')
	profile_image = models.ImageField(upload_to='images/', blank=True, null=True)
	name = models.CharField(max_length=150, blank=True)
	# email = models.CharField(max_length=150, blank=True)
	phone = models.CharField(max_length=150, blank=True)
	address = models.CharField(max_length=150, blank=True)

	def get_photo(self):
		"""should reture semiadmin passport or placeholder image"""
		if self.profile_image:
			return self.profile_image.url
		return '/static/portal/uploads/users/placeholder.jpg'


	def __str__(self):
		return f'Name: <{self.name}>  Email: <{self.user.email}>'


class Accountant(models.Model):
	name = models.CharField(max_length=150, blank=True)
	gender = models.CharField(max_length=150, blank=True)
	password = models.CharField(max_length=150, blank=True)
	email = models.CharField(max_length=150, blank=True)
	phone = models.CharField(max_length=150, blank=True)
	gender = models.CharField(max_length=5, blank=True)
	blood_group = models.CharField(max_length=5, blank=True)
	address = models.TextField(max_length=3000, blank=True)
	left_school = models.BooleanField(default=False)

	def __str__(self):
		return self.name


class Librarian(models.Model):
	name = models.CharField(max_length=150, blank=True)
	gender = models.CharField(max_length=150, blank=True)
	password = models.CharField(max_length=150, blank=True)
	email = models.CharField(max_length=150, blank=True)
	phone = models.CharField(max_length=150, blank=True)
	gender = models.CharField(max_length=5, blank=True)
	blood_group = models.CharField(max_length=5, blank=True)
	address = models.TextField(max_length=3000, blank=True)
	left_school = models.BooleanField(default=False)

	def __str__(self):
		return self.name
