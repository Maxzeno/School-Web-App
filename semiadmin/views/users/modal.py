from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse

from management import models as user_model
from student import models as student_model
from teacher import models as teacher_model
from ... import models as semiadmin_model
from ...utils import DEFAULT_IMAGE_THE_URL
from utils.html import HTML
from .filter import SubjectPermissionFilter, ClassPermissionFilter, PermissionFilter

import csv
import io
import mimetypes
import os
import datetime



class PermissionSet(View):
	def post(self, request):
		"""
		WORKS FOR A, B, C ETC 
		NEED TO WORK ON ALL AND MAYBE LEFT
		"""
		class_id = request.POST.get('class_id')
		section_id = request.POST.get('section_id')
		teacher_id = request.POST.get('teacher_id')
		column_name = request.POST.get('column_name')
		value = request.POST.get('value')

		the_teacher = teacher_model.Teacher.objects.filter(pk=teacher_id).first()

		the_exact_class = student_model.Class.objects.filter(the_class=class_id, the_section=section_id).first()
		found_exact_subject = semiadmin_model.SubjectPermission.objects.filter(the_exact_class=the_exact_class, 
				the_teacher=the_teacher).first()
		if found_exact_subject:
			semiadmin_model.SubjectPermission.objects.filter(the_exact_class=the_exact_class, 
				the_teacher=the_teacher).update(**{column_name:bool(int(value))})

		else:
			semiadmin_model.SubjectPermission.objects.create(**{column_name:bool(value), 'the_teacher':the_teacher, 
				'the_exact_class':the_exact_class})

		perm = PermissionFilter()
		return perm.get(request, class_id, section_id)
		

""" Accountant SECTION """


class AccountantCreate(View):
	def get(self, request):
		html = render(request, 'semiadmin/users/modal/accountant.html', {})
		return HttpResponse(html)

	def post(self, request):
		try:
			data = {
				'name':request.POST.get('name'),
				'email':request.POST.get('email'),
				'password':request.POST.get('password'),
				'gender':request.POST.get('gender'),
				'blood_group':request.POST.get('blood_group'),
				'phone':request.POST.get('phone'),
				'address':request.POST.get('address'),
			}

			semiadmin_model.Accountant.objects.create(**data)
			return JsonResponse({"status":True,"notification":"Accountant added successfully"})
		except:
			return JsonResponse({"status":False,"notification":"Accountant not added"})

		
class AccountantEdit(View):
	def get(self, request, id):

		accountant = semiadmin_model.Accountant.objects.filter(pk=id).first()
		html = render(request, 'semiadmin/users/modal/accountant_edit.html', {'accountant':accountant})

		return HttpResponse(html)

	def post(self, request, id):

		data = {
			'name':request.POST.get('name'),
			'email':request.POST.get('email'),
			'password':request.POST.get('password'),
			'phone':request.POST.get('phone'),
			'gender':request.POST.get('gender'),
			'blood_group':request.POST.get('blood_group'),
			'address':request.POST.get('address'),
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.Accountant.objects.filter(pk=id).update(**new_data)
		return JsonResponse({"status":True,"notification": "Accountant Updated Successfully"})


class AccountantDelete(View):
	def post(self, request, id):
		semiadmin_model.Accountant.objects.filter(pk=id).delete()
		return JsonResponse({"status":True,"notification": "Accountant Deleted"})

""" END Accountant SECTION """


""" Liberian SECTION """

class LibrarianCreate(View):
	def get(self, request):
		html = render(request, 'semiadmin/users/modal/librarian.html', {})
		return HttpResponse(html)

	def post(self, request):
		try:
			data = {
				'name':request.POST.get('name'),
				'email':request.POST.get('email'),
				'password':request.POST.get('password'),
				'gender':request.POST.get('gender'),
				'blood_group':request.POST.get('blood_group'),
				'phone':request.POST.get('phone'),
				'address':request.POST.get('address'),
			}

			semiadmin_model.Librarian.objects.create(**data)
			return JsonResponse({"status":True,"notification":"Librarian added successfully"})
		except:
			return JsonResponse({"status":False,"notification":"Librarian not added"})
		

class LibrarianEdit(View):
	def get(self, request, id):
		librarian = semiadmin_model.Librarian.objects.filter(pk=id).first()
		html = render(request, 'semiadmin/users/modal/librarian_edit.html', {'librarian':librarian})
		return HttpResponse(html)

	def post(self, request, id):
		data = {
			'name':request.POST.get('name'),
			'email':request.POST.get('email'),
			'password':request.POST.get('password'),
			'phone':request.POST.get('phone'),
			'gender':request.POST.get('gender'),
			'blood_group':request.POST.get('blood_group'),
			'address':request.POST.get('address'),
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		semiadmin_model.Librarian.objects.filter(pk=id).update(**new_data)
		return JsonResponse({"status":True,"notification": "Librarian Updated Successfully"})


class LibrarianDelete(View):
	def post(self, request, id):
		semiadmin_model.Librarian.objects.filter(pk=id).delete()
		return JsonResponse({"status":True,"notification": "Librarian Deleted"})

""" END Liberian SECTION """


""" Parent SECTION"""

class ParentCreate(View):
	def get(self, request):
		html = render(request, 'semiadmin/users/modal/parent.html', {})
		return HttpResponse(html)

	def post(self, request):
		try:
			data = {
				'name':request.POST.get('name'),
				'email_address':request.POST.get('email'),
				'password':request.POST.get('password'),
				'gender':request.POST.get('gender'),
				'blood_group':request.POST.get('blood_group'),
				'phone':request.POST.get('phone'),
				'address':request.POST.get('address'),
			}

			student = student_model.Parent.objects.create(**data)
			return JsonResponse({"status":True,"notification":"Parent added successfully"})
		except:
			return JsonResponse({"status":False,"notification":"Parent added no"})


class ParentEdit(View):
	def get(self, request, id):

		parent = student_model.Parent.objects.filter(pk=id).first()
		html = render(request, 'semiadmin/users/modal/parent_edit.html', {'parent':parent})

		return HttpResponse(html)

	def post(self, request, id):

		data = {
			'name':request.POST.get('name'),
			'email_address':request.POST.get('email'),
			'phone':request.POST.get('phone'),
			'gender':request.POST.get('gender'),
			'blood_group':request.POST.get('blood_group'),
			'address':request.POST.get('address'),
		}

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		parent = student_model.Parent.objects.filter(pk=id).update(**new_data)
		return JsonResponse({"status":True,"notification": "Parent Updated Successfully"})



class ParentDelete(View):
	def post(self, request, id):
		student_model.Parent.objects.filter(pk=id).delete()
		return JsonResponse({"status":True,"notification": "Parent Deleted"})

""" END Parent SECTION"""


""" ManagementTeam SECTION"""

class ManagementTeamCreate(View):
	def get(self, request):
		departments = teacher_model.Department.objects.all()
		html = render(request, 'semiadmin/users/modal/management_team.html', {'departments': departments})
		return HttpResponse(html)

	def post(self, request):
		# try:
		data = {
			'name':request.POST.get('name'),
			'designation':request.POST.get('designation'),
			'gender':request.POST.get('gender'),
			'phone':request.POST.get('phone'),
			'blood_group':request.POST.get('blood_group'),
			'facebook_link':request.POST.get('facebook_link'),
			'twitter_link':request.POST.get('twitter_link'),
			'linkedin_link':request.POST.get('linkedin_link'),
			'address':request.POST.get('address'),
			'about':request.POST.get('about'),
			'show_on_website':request.POST.get('show_on_website'),
			'image':request.FILES.get('image_file'),
			'management_team': True,
		}

		department = request.POST.get('department')
		if department:
			the_department = teacher_model.Department.objects.filter(name=department).first()
			if the_department:
				data['department'] = the_department
				
			else:
				the_department = teacher_model.Department.objects.create(name=department)
				data['department'] = the_department

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		user = user_model.User.objects.create(email=request.POST.get('email'), password=request.POST.get('password'), is_teacher=True)
		teacher = teacher_model.Teacher.objects.create(user=user, **data)
		return JsonResponse({"status":True,"notification":"Management Staff added successfully"})
		# except:
		# 	return JsonResponse({"status":False,"notification":"Management Staff not added"})
			



class ManagementTeamEdit(View):
	def get(self, request, id):
		departments = teacher_model.Department.objects.all()
		management_team = semiadmin_model.Teacher.objects.filter(pk=id, management_team=True).first()
		html = render(request, 'semiadmin/users/modal/management_team_edit.html', {'management_team':management_team,
			'departments': departments})
		return HttpResponse(html)

	def post(self, request, id):

		data = {
				'name':request.POST.get('name'),
				# 'email':request.POST.get('email'),
				'designation':request.POST.get('designation'),
				# 'department':request.POST.get('department'),
				'phone':request.POST.get('phone'),
				'gender':request.POST.get('gender'),
				'blood_group':request.POST.get('blood_group'),
				'facebook_link':request.POST.get('facebook_link'),
				'twitter_link':request.POST.get('twitter_link'),
				'linkedin_link':request.POST.get('linkedin_link'),
				'address':request.POST.get('address'),
				'about':request.POST.get('about'),
				'show_on_website':request.POST.get('show_on_website'),
				'image':request.FILES.get('image_file'),
		}

		department = request.POST.get('department')
		if department:
			the_department = teacher_model.Department.objects.filter(name=department).first()
			if the_department:
				data['department'] = the_department
				
			else:
				the_department = teacher_model.Department.objects.create(name=department)
				data['department'] = the_department

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		teacher = teacher_model.Teacher.objects.filter(pk=id).update(**new_data)
		if request.POST.get('password'):
			user = teacher.first().user
			user.password = request.POST.get('password')
			user.save()
		return JsonResponse({"status":True,"notification": "Management team Updated Successfully"})

class ManagementTeamDelete(View):
	def post(self, request, id):
		semiadmin_model.Teacher.objects.filter(pk=id, management_team=True).first().delete()
		return JsonResponse({"status":True,"notification": "Management team Deleted"})



class ManagementTeamUpdatePassword(View):
	def get(self, request, id):
		management_team = semiadmin_model.Teacher.objects.filter(id=id, management_team=True).first()
		html = render(request, 'semiadmin/users/modal/management_team_change_password.html', {'management_team':management_team})
		return HttpResponse(html)

	def post(self, request, id):
		# try:
		new_password = request.POST.get('new_password')
		confirm_password = request.POST.get('confirm_password')
		if new_password != confirm_password:
			return JsonResponse({"status":False,"notification": "Password didn't match confirm password"})

		if not new_password:
			return JsonResponse({"status":False, "notification":"Password is empty"})

		teacher = teacher_model.Teacher.objects.filter(id=id).first()
		user = teacher.user
		user.password = new_password
		user.save()
		return JsonResponse({"status":True,"notification":"Management Team updated successfully"})


""" END ManagementTeam SECTION"""


class CSVManagementTeamGenerate(View):
	def get(self, request):
		filename = 'csv_management_team.generate.csv'
		filepath = 'semiadmin/templates/semiadmin/users/asset/' + filename
		path = open(filepath, 'r')
		mime_type, _ = mimetypes.guess_type(filepath)
		response = HttpResponse(path, content_type=mime_type)
		response['Content-Disposition'] = "attachment; filename=%s" % filename
		return response



class CreateManagementTeamExcel(View):
	def get(self, request):
		html = render(request, 'semiadmin/users/modal/management_team_excel.html', {})
		return HttpResponse(html)

	def post(self, request):
		try:
			myfile = request.FILES['csv_file']
			file = myfile.read().decode('utf-8')
			reader = csv.DictReader(io.StringIO(file))

			for row in reader:
				vals = list(row.values())

				data = {
					'name':vals[0],
					'designation':vals[3],
					'phone':vals[4],
					'gender':vals[5],
					'show_on_website':bool(vals[6]),
				}

				user = user_model.User.objects.create(email=vals[1], password=vals[2], is_teacher=True)
				teacher = teacher_model.Teacher.objects.create(user=user, **data)
			return JsonResponse({"status": True, "notification": "Management added successfully"})
		except:
			return JsonResponse({"status": False, "notification": "Management not added"})


""" END ManagementTeam SECTION """

""" Teacher SECTION """


class TeacherCreate(View):
	def get(self, request):
		departments = teacher_model.Department.objects.all()
		html = render(request, 'semiadmin/users/modal/teacher.html', {'departments': departments})
		return HttpResponse(html)

	def post(self, request):
		# try:
		data = {
			'name':request.POST.get('name'),
			'designation':request.POST.get('designation'),
			# 'department':request.POST.get('department'),
			'phone':request.POST.get('phone'),
			'gender':request.POST.get('gender'),
			'blood_group':request.POST.get('blood_group'),
			'facebook_link':request.POST.get('facebook_link'),
			'twitter_link':request.POST.get('twitter_link'),
			'linkedin_link':request.POST.get('linkedin_link'),
			'address':request.POST.get('address'),
			'about':request.POST.get('about'),
			'show_on_website':request.POST.get('show_on_website'),
			'image':request.FILES.get('image_file'),
		}

		department = request.POST.get('department')
		if department:
			the_department = teacher_model.Department.objects.filter(name=department).first()
			if the_department:
				data['department'] = the_department
				
			else:
				the_department = teacher_model.Department.objects.create(name=department)
				data['department'] = the_department

		user = user_model.User.objects.create(email=request.POST.get('email'), password=request.POST.get('password'), is_teacher=True)
		teacher = teacher_model.Teacher.objects.create(user=user, **data)
		return JsonResponse({"status":True,"notification":"Teacher added successfully"})
		# except:
		# 	return JsonResponse({"status":False,"notification":"Teacher not added"})


class TeacherUpdatePassword(View):
	def get(self, request, id):
		teacher = teacher_model.Teacher.objects.filter(id=id).first()
		html = render(request, 'semiadmin/users/modal/teacher_change_password.html', {'teacher':teacher})
		return HttpResponse(html)

	def post(self, request, id):
		# try:
		new_password = request.POST.get('new_password')
		confirm_password = request.POST.get('confirm_password')
		if new_password != confirm_password:
			return JsonResponse({"status":False,"notification": "Password didn't match confirm password"})

		if not new_password:
			return JsonResponse({"status":False, "notification":"Password is empty"})

		teacher = teacher_model.Teacher.objects.filter(id=id).first()
		user = teacher.user
		user.password = new_password
		user.save()
		return JsonResponse({"status":True,"notification":"Teacher updated successfully"})
		# except:
			# return JsonResponse({"status":False,"notification":"Teacher not updated"})



class TeacherEdit(View):
	def get(self, request, id):
		teacher = teacher_model.Teacher.objects.filter(pk=id).first()
		departments = teacher_model.Department.objects.all()
		html = render(request, 'semiadmin/users/modal/teacher_edit.html', {'teacher':teacher, 'departments': departments})
		return HttpResponse(html)

	def post(self, request, id):
		data = {
				'name':request.POST.get('name'),
				# 'email':request.POST.get('email'),
				'designation':request.POST.get('designation'),
				# 'department':request.POST.get('department'),
				'phone':request.POST.get('phone'),
				'gender':request.POST.get('gender'),
				'blood_group':request.POST.get('blood_group'),
				'facebook_link':request.POST.get('facebook_link'),
				'twitter_link':request.POST.get('twitter_link'),
				'linkedin_link':request.POST.get('linkedin_link'),
				'address':request.POST.get('address'),
				'about':request.POST.get('about'),
				'show_on_website':request.POST.get('show_on_website'),
				'image':request.FILES.get('image_file'),
		}

		department = request.POST.get('department')
		if department:
			the_department = teacher_model.Department.objects.filter(name=department).first()
			if the_department:
				data['department'] = the_department
				
			else:
				the_department = teacher_model.Department.objects.create(name=department)
				data['department'] = the_department

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		teacher = teacher_model.Teacher.objects.filter(pk=id).update(**new_data)
		if request.POST.get('password'):
			user = teacher.first().user
			user.password = request.POST.get('password')
			user.save()
		return JsonResponse({"status":True,"notification": "Teacher Updated Successfully"})



class CSVTeacherGenerate(View):
	def get(self, request):
		filename = 'csv_teacher.generate.csv'
		filepath = 'semiadmin/templates/semiadmin/users/asset/' + filename
		path = open(filepath, 'r')
		mime_type, _ = mimetypes.guess_type(filepath)
		response = HttpResponse(path, content_type=mime_type)
		response['Content-Disposition'] = "attachment; filename=%s" % filename
		return response


class CreateTeacherExcel(View):
	def get(self, request):
		html = render(request, 'semiadmin/users/modal/teacher_excel.html', {})
		return HttpResponse(html)

	def post(self, request):
		try:
			myfile = request.FILES['csv_file']
			file = myfile.read().decode('utf-8')
			reader = csv.DictReader(io.StringIO(file))

			for row in reader:
				vals = list(row.values())

				data = {
					'name':vals[0],
					'designation':vals[3],
					'phone':vals[4],
					'gender':vals[5],
					'show_on_website':bool(vals[6]),
				}

				user = user_model.User.objects.create(email=vals[1], password=vals[2], is_teacher=True)
				teacher = teacher_model.Teacher.objects.create(user=user, **data)
			return JsonResponse({"status":True,"notification":"Teacher added successfully"})
		except:
			return JsonResponse({"status":False,"notification":"Teacher not added"})


class TeacherDelete(View):
	def post(self, request, id):
		teacher_model.Teacher.objects.filter(pk=id).delete()
		return JsonResponse({"status":True,"notification": "Teacher Deleted"})

""" END Teacher SECTION """


""" SubjectPermission SECTION """

class SubjectPermissionSet(View):
	def post(self, request):
		"""
		WORKS FOR A, B, C ETC 
		NEED TO WORN ON ALL AND MAYBE LEFT
		"""
		class_id = request.POST.get('class_id')
		section_id = request.POST.get('section_id')
		subject_name = request.POST.get('subject_id')
		subject_id = student_model.Subject.objects.filter(name=subject_name).first().pk
		teacher_id = request.POST.get('teacher_id')
		column_name = request.POST.get('column_name')
		value = request.POST.get('value')

		the_teacher = teacher_model.Teacher.objects.filter(pk=teacher_id).first()
		the_subject = student_model.Subject.objects.filter(pk=subject_id).first()

		the_exact_class = student_model.Class.objects.filter(the_class=class_id, the_section=section_id).first()
		found_exact_subject = semiadmin_model.SubjectPermission.objects.filter(the_exact_class=the_exact_class, the_subject=the_subject, 
				the_teacher=the_teacher).first()
		if found_exact_subject:
			semiadmin_model.SubjectPermission.objects.filter(the_exact_class=the_exact_class, the_subject=the_subject, 
				the_teacher=the_teacher).update(**{column_name:bool(int(value))})

		else:
			semiadmin_model.SubjectPermission.objects.create(**{column_name:bool(value), 'the_teacher':the_teacher, 
				'the_subject': the_subject, 'the_exact_class':the_exact_class})

		perm = SubjectPermissionFilter()
		return perm.get(request, class_id, section_id, subject_name)
		


class ClassPermissionSet(View):
	def post(self, request):
		"""
		WORKS FOR A, B, C ETC 
		NEED TO WORN ON ALL AND MAYBE LEFT
		"""
		class_id = request.POST.get('class_id')
		section_id = request.POST.get('section_id')
		subject_id = request.POST.get('subject_id')
		teacher_id = request.POST.get('teacher_id')
		column_name = request.POST.get('column_name')
		value = request.POST.get('value')

		the_teacher = teacher_model.Teacher.objects.filter(pk=teacher_id).first()
		the_subject = student_model.Subject.objects.filter(pk=subject_id).first()

		the_exact_class = student_model.Class.objects.filter(the_class=class_id, the_section=section_id).first()
		found_exact_subject = semiadmin_model.SubjectPermission.objects.filter(the_exact_class=the_exact_class, the_subject=the_subject, 
				the_teacher=the_teacher).first()
	
		if found_exact_subject:
			semiadmin_model.SubjectPermission.objects.filter(the_exact_class=the_exact_class, the_subject=the_subject, 
				the_teacher=the_teacher).update(**{column_name:bool(int(value))})

		else:
			semiadmin_model.SubjectPermission.objects.create(**{column_name:bool(value), 'the_teacher':the_teacher, 
				'the_subject': the_subject, 'the_exact_class':the_exact_class})

		perm = ClassPermissionFilter()
		return perm.get(request, class_id, section_id)
		
""" END SubjectPermission SECTION """


