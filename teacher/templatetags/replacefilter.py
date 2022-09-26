# from django import template
# from django.db.models import F

# from management import models as user_model
# from student import models as student_model
# from teacher import models as teacher_model
# from .. import models as semiadmin_model
# from datetime import datetime
# register = template.Library()


# @register.filter
# def avg_by_index_three(values, index):
# 	if not values:
# 		return 0

# 	total = 0
# 	count = 0
# 	for value in values:
# 		count += 1
# 		if isinstance(value[index], int):
# 			total += value[index]
# 	return round(total/count, 2) if count > 0 else 0


# @register.filter
# def total_by_index_three(values, index):
# 	if not values:
# 		return '0/0'

# 	total = 0
# 	for value in values:
# 		if isinstance(value[index], int):
# 			total += value[index]
# 	return f'{total}/{100*len(values)}'


# @register.filter
# def avg_by_index(value, index):
# 	total = 0
# 	count = 0
# 	for i in value:
# 		count += 1
# 		total += i[index]
# 	return round(total/count, 2) if count > 0 else 0


# @register.filter
# def total_by_index(value, index):
# 	total = 0
# 	for i in value:
# 		total += i[index]
# 	return total


# @register.filter
# def none_dash(value):
# 	if value:
# 		return value
# 	return '-'

# @register.filter
# def rate_domain(value):
# 	if not isinstance(value, int):
# 		return '-'

# 	if value <= 1:
# 		return 'Poor'
# 	elif value == 2:
# 		return 'Fair'
# 	elif value == 3:
# 		return 'Good'
# 	elif value == 4:
# 		return 'Very good'
# 	else:
# 		return 'Excellent'

# @register.filter
# def subject_position(value, student_and_exam):
# 	def pos_th(val):
# 		if val == 1:
# 			return f'{val}st'
# 		elif val == 2:
# 			return f'{val}nd'
# 		elif val == 3:
# 			return f'{val}rd'
# 		else:
# 			return f'{val}th'


# 	student, exam = student_and_exam
# 	class_room = student.student_class_room
# 	the_mark = mark = student.mark_set.filter(exam=exam, subject=value['subject_id']).first()
# 	total_score = the_mark.total_mark()
	
# 	scores_set = set()
# 	marks = semiadmin_model.Mark.objects.filter(exam=exam, subject=value['subject_id'], class_room=class_room)
# 	for mark in marks:
# 		scores_set.add(mark.total_mark())

# 	scores_list = list(scores_set)
# 	scores_list.sort()
# 	scores_list.reverse()
	
# 	return f"{pos_th(scores_list.index(total_score)+1)}"


# @register.filter
# def subject_lowest(value, student_and_exam):
# 	student, exam = student_and_exam
# 	class_room = student.student_class_room
# 	lowests = semiadmin_model.Mark.objects.filter(exam=exam, subject=value['subject_id'], class_room=class_room)

# 	lowest = float('inf')
# 	for low in lowests:
# 		lowest = min(lowest, low.total_mark())

# 	return lowest if lowest != float('inf') else '-'


# @register.filter
# def subject_highest(value, student_and_exam):
# 	student, exam = student_and_exam
# 	class_room = student.student_class_room
# 	highests = semiadmin_model.Mark.objects.filter(exam=exam, subject=value['subject_id'], class_room=class_room)

# 	highest = 0
# 	for high in highests:
# 		highest = max(highest, high.total_mark())

# 	return highest


# @register.filter
# def subject_grade(value, student_and_exam):
# 	student, exam = student_and_exam
# 	mark = student.mark_set.filter(exam=exam, subject=value['subject_id']).first()
# 	return mark.get_grade()


# @register.filter
# def subject_remark(value, student_and_exam):
# 	student, exam = student_and_exam
# 	mark = student.mark_set.filter(exam=exam, subject=value['subject_id']).first()
# 	return mark.comment
	

# @register.filter
# def subject_total(value, student_and_exam):
# 	student, exam = student_and_exam
# 	mark = student.mark_set.filter(exam=exam, subject=value['subject_id']).first()
# 	return mark.total_mark()


# @register.filter
# def subject_score_hash(h, key):
# 	if key == 'subject_id':
# 		subject = student_model.Subject.objects.filter(pk=h[key]).first()
# 		return subject.name
# 	return h[key]


# @register.filter
# def hash(h, key):
# 	return h[key]


# @register.filter
# def replace_with_dash(value):
# 	return value.replace('/', '-')


# @register.filter
# def select_if_class(value):
# 	just_class = student_model.JustClass.objects.filter(pk=value).first()
# 	the_class = student_model.JustClass.objects.filter(the_class=just_class).first().pk
# 	return the_class
