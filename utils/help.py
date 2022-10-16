from datetime import datetime, date
from django.http import HttpResponse

import calendar
from management import models as user_model
from student import models as student_model
from teacher import models as teacher_model
from semiadmin import models as semiadmin_model
from openpyxl import load_workbook
from io import BytesIO


def read_excel(path: str, sheet: str=None):
	""" Return 2D array -- inform of Generator"""
	path = BytesIO(path)
	book = load_workbook(filename=path)
	sheet = book.active
	gen = sheet.values
	return gen

def subject_perm(request, the_exact_class, subject):
	try:
		perms = semiadmin_model.SubjectPermission.objects.filter(the_teacher=request.user.teacher, 
			the_exact_class=the_exact_class, the_subject=subject).values_list('exam', 'assignment', 'mid_term', 'attendance', 'online_exam')
		return any(perms[0])
	except IndexError:
		return False


def class_perm(request, the_exact_class):
	try:
		perms = semiadmin_model.SubjectPermission.objects.filter(the_teacher=request.user.teacher, 
			the_exact_class=the_exact_class).values_list('exam', 'assignment', 'mid_term', 'attendance', 'online_exam')
		for perm in perms:
			if any(perm):
				return True
		return False
	except:
		return False


def perm_not():
	return HttpResponse("""
	<div class="col-md-12 text-center">
	    <div class="alert alert-danger" role="alert">
			<h4 class="alert-heading">Access denied!</h4>
			<hr>
			<p class="mb-0">Sorry you are not permitted to access this view. <br>Admin handles it.</p>
	    </div>
	</div>""")


def pos_th(val):
	if val == 1:
		return f'{val}st'
	elif val == 2:
		return f'{val}nd'
	elif val == 3:
		return f'{val}rd'
	else:
		return f'{val}th'


def sum_avg(arr):
	s = 0
	count = 0
	for i in arr:
		if isinstance(i, (int, float)):
			s += i
			count += 1

	return [s, round(s/count, 2) if count > 0 else 0]



def sessioner():
	""" Returns and updated the Academic session model"""
	sessions = student_model.Session.objects.all()
	year = date.today().year

	if not sessions:
		student_model.Session.objects.create(session=f'{year-1}-{year}')
		student_model.Session.objects.create(session=f'{year}-{year+1}')

	else:
		year2_str, year3_str = sessions.last().session.split('-')
		year2, year3 = int(year2_str), int(year3_str)
		max_go_back = 5
		create_years = min(year-year3, max_go_back)
		if year > year3:
			for num in range(create_years-1, -1, -1):
				student_model.Session.objects.create(session=f'{year-num}-{(year-num)+1}')

		elif year == year3:
			student_model.Session.objects.create(session=f'{year}-{year+1}')

	sessions = student_model.Session.objects.all()
	return sessions


def prime_subjects():
	""" Returns the main subjects like english and math it queries the PassMark db"""
	the_subject = set()
	passmarks = student_model.PassMark.objects.all()
	for passmark in passmarks:
		the_subject.add(passmark.get_subject().lower())
	return the_subject

def num_len(num):
	"""return the length of a number eg. 44 == 2, 839 == 3"""
	return (num.bit_length() // 3) + 1


def is_date_range(date_range):
	""" return True if "date_range like" 2021-2022 else False"""
	try:
		arr_year = date_range.split('-')
		if len(arr_year) == 2:
			for i in arr_year:
				if num_len(int(i)) != 4:
					return False
			return True
		else:
			return False
	except ValueError:
		return False


def date_range():
	day = date.today()
	range_month = calendar.monthrange(day.year, day.month)
	first = date(day.year, day.month, range_month[0]+1)
	last = date(day.year, day.month, range_month[1])
	first_day = first.strftime('%B %d, %Y')
	last_day = last.strftime('%B %d, %Y')
	return f'{first_day} - {last_day}'

	
def new_id():
	"""Returns a unique unused student id (it queries db and gets the last id then increments it)"""
	last_students = reversed(student_model.Student.objects.all())
	new_student_id = 0
	year_now = date.today().strftime('%y')
	cdsse = 'CDSSE'

	if last_students:
		for last_student in last_students:
			try:
				cdsse_file, year, student_id = last_student.pk.split('/')
			except:
				continue

			if student_id.isdigit() and year == year_now:
				student_id = int(student_id) + 1
				student_id = str(student_id)
				new_id = f'{cdsse}/{year_now}/{student_id.zfill(4)}'
			elif year < year_now:
				new_student_id += 1
				new_student_id_str = str(new_student_id)
				new_id = f'{cdsse}/{year_now}/{new_student_id_str.zfill(4)}'
			else:
				continue

			exists = student_model.Student.objects.filter(pk=new_id).exists()
			if exists:
				continue
			else:
				return new_id
		else:
			return f'{cdsse}/{year_now}/0001'
	else:
		return f'{cdsse}/{year_now}/0001'


def date_converter(date_str):
	"""Converts string to date objects"""
	if '/' in date_str:
		date_object = datetime.strptime(date_str.lower().strip(), '%m/%d/%Y')
	elif ',' in date_str:
		date_object = datetime.strptime(date_str.lower().strip(), '%b. %d, %Y')
	else:
		date_object = date_str
	return date_object


def date_range_from_string(date_str):
	"""arg str. return list of date usually to and can be used as date range"""
	date_list = date_str.split(' - ')
	new = []
	for date_item in date_list:
		date_object = datetime.strptime(date_item.lower().strip(), '%B %d, %Y')
		new.append(date_object)
	return new


def sum_and_max(d_itr):
	res = float('-inf')
	for itr in d_itr:
		if res < itr.total_mark():
			res = itr.total_mark()
	return res if res != float('-inf') else '-'


def sum_and_min(d_itr):
	res = float('inf')
	for itr in d_itr:
		if res > itr.total_mark():
			res = itr.total_mark()
	return res if res != float('inf') else '-'


def sum_and_avg(d_itr):
	res = 0
	count = 0
	for itr in d_itr:
		res += itr.total_mark()
		count += 1
	return round(float(res/count), 1) if res else '-'


def sum_arr_wrong_type(arr):
	sum_arr = 0
	for i in arr:
		if i != '-':
			sum_arr += i
	return sum_arr


def percent_arr(arr):
	sum_arr = 0
	count = 0
	for i in arr:
		if i != '-':
			sum_arr += i
			count += 1
	return round(sum_arr/count, 2) if sum_arr else sum_arr


def pass_or_fail(arr, subjects_to_pass, index_prime_subjects=None, pass_mark=50, ret_pass='PASS', ret_fail='FAIL'):
	good = 0
	prime_subjects_pos = []
	for i, mark in enumerate(arr):
		if isinstance(mark, int):
			if mark >= pass_mark:
				good += 1

		if i in index_prime_subjects:
			if isinstance(mark, int):
				if mark >= pass_mark:
					prime_subjects_pos.append(True)
				else:
					prime_subjects_pos.append(False)
			else:
				prime_subjects_pos.append(False)

	if good >= subjects_to_pass:
		return ret_pass
	elif good+1 >= subjects_to_pass:
		if prime_subjects_pos and all(prime_subjects_pos):
			return ret_pass
		else:
			return ret_fail
	else:
		return ret_fail




