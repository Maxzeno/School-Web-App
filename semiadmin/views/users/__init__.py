from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template

from management import models as user_model
from student import models as student_model
from teacher import models as teacher_model
from ... import models as semiadmin_model
from ...utils import DEFAULT_IMAGE_THE_URL
from utils.html import html
from .filter import *
from .modal import *

from utils import help as help_tools



class Marksheet(View):
	def get(self, request, id):
		sessions = student_model.Session.objects.all()
		student = student_model.Student.objects.filter(pk=id.replace('-', '/')).first()
		return render(request, 'semiadmin/users/marksheet.html', {'sessions': sessions, 'student': student})


class Teacher(View):
	queryset = teacher_model.Teacher.objects.filter(management_team=False).all()
	template = 'semiadmin/users/teacher.html'

	def get(self, request):
		tbodys = self.queryset

		new_tbodys = []
		for tbody in tbodys:
			try:
				img_url = tbody.image.url
			except:
				img_url = DEFAULT_IMAGE_THE_URL

			try:
				department = tbody.department.name
			except:
				department = 'N/A'

			new_tbodys.append([img_url, tbody.name, department, tbody.designation, tbody.id])

		data = {
			'tbodys':new_tbodys,
			}
		return render(request, self.template, data)

class ManagementTeam(Teacher):
	queryset = teacher_model.Teacher.objects.filter(management_team=True).all()
	template = 'semiadmin/users/management_team.html'


class StudentEdit(View):
	def get(self, request, student_class, student_class_room, id):
		student = student_model.Student.objects.filter(pk=id.replace('-', '/')).first()
		the_class = student.student_class_room
		the_classes = student_model.Class.objects.filter(the_class=the_class.the_class).values_list('the_section').distinct()
		# the_classes = [i[0] for i in the_classes]
		# student_class_rooms = student_model.Student.objects.filter(student_class_room=the_class).values_list('student_class_room').distinct()
		student_rooms = [i[0] for i in the_classes]


		parents = student_model.Parent.objects.all()
		the_classes = student_model.JustClass.objects.all()
		return render(request, 'semiadmin/users/student_update.html', {'student': student, 'parents': parents,
			'student_class': student_class, 
			'student_class_room': student_class_room,
			'id':id,
			'student_rooms':student_rooms,
			'the_classes': the_classes})


	def post(self, request, student_class, student_class_room, id):
		# try:
		data = {
			'name':request.POST.get('name'),
			# 'email':request.POST.get('email'),
			'student_id':request.POST.get('student_id'),
			'birthday':request.POST.get('birthday'),
			'gender':request.POST.get('gender'),
			'blood_group':request.POST.get('blood_group'),
			'phone':request.POST.get('phone'),
			'address':request.POST.get('address'),
			'passport_photo':request.FILES.get('student_image')

		}

		student_class = request.POST.get('class_id').upper()
		student_class_room = request.POST.get('section_id').upper()
		class_room = student_model.Class.objects.filter(the_class=student_class, 
			the_section=student_class_room).first()
		if class_room:
			data['student_class_room'] = class_room

		if request.POST.get('parent_id'):
			parent = student_model.Parent.objects.filter(pk=request.POST.get('parent_id')).first()
			if parent:
				data['parent'] = parent

		new_data = {}
		for k in data:
			if data[k]:
				 new_data[k] = data[k]

		student = student_model.Student.objects.filter(pk=id.replace('-', '/')).update(**new_data)
		return JsonResponse({"status":True,"notification":"Student Updated Successfully"})
		# except:
		# 	return JsonResponse({"status":False,"notification":"Student not added"})



class AdmissionExcel(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()
		return render(request, 'semiadmin/users/create_student_excel.html', {'the_classes': the_classes})


	def post(self, request):
		try:
			myfile = request.FILES['csv_file']
			file = myfile.read().decode('utf-8')
			reader = csv.DictReader(io.StringIO(file))
			class_id = request.POST.get('class_id').upper()
			section_id = request.POST.get('section_id').upper()

			for row in reader:
				vals = list(row.values())
				print(vals)
				data = {
					'name':vals[0],
					# 'email':vals[1],
					'phone':vals[3],
					'gender':vals[5],
					'student_id':vals[6],
					# 'student_class': class_id,
					# 'student_class_room': section_id
				}

				student_class = request.POST.get('class_id').upper()
				student_class_room = request.POST.get('section_id').upper()
				class_room = student_model.Class.objects.filter(the_class=student_class, 
					the_section=student_class_room).first()
				if class_room:
					data['student_class_room'] = class_room
				if vals[4]:
					parent = student_model.Parent.objects.filter(pk=vals[4]).first()
					if parent:
						data['parent'] = parent

				user = user_model.User(is_student=True, email=vals[1], password=vals[2])
				user.save()
				student = student_model.Student.objects.create(user=user, **data)
			return JsonResponse({"status":True,"notification":"Student added successfully"})
		except:
			return JsonResponse({"status":False,"notification":"Student not added"})


class AdmissionBulk(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()
		parents = student_model.Parent.objects.all()
		new_id = help_tools.new_id()
		return render(request, 'semiadmin/users/create_bulk.html', {'parents': parents, 'the_classes': the_classes,
			'new_id': new_id})

	def post(self, request):
		try:
			student_class = request.POST.get('class_id').upper()
			student_class_room = request.POST.get('section_id').upper()

			names = request.POST.getlist('name[]')
			emails = request.POST.getlist('email[]')
			student_ids = request.POST.getlist('student_id[]')
			passwords = request.POST.getlist('password[]')
			genders = request.POST.getlist('gender[]')
			parent_ids = request.POST.getlist('parent_id[]')

			class_room = student_model.Class.objects.filter(the_class=student_class, 
				the_section=student_class_room).first()

			for i in range(len(names)):
				if student_ids[i]:
					user = user_model.User.objects.create(email=emails[i], password=passwords[i], is_student=True)

					if class_room:
						student = student_model.Student(user=user, name=names[i], student_id=student_ids[i].upper(),
							gender=genders[i], student_class_room=class_room)
					else:
						student = student_model.Student(user=user, name=names[i], student_id=student_ids[i].upper(),
						 gender=genders[i])

					if parent_ids[i]:
						parent = student_model.Parent.objects.filter(pk=parent_ids[i]).first()
						if parent:
							student.parent = parent
					student.save()
			return JsonResponse({"status":True,"notification":"Students added Successfully"})
		except:
			return JsonResponse({"status":False,"notification":"Students Not added"})



class Admission(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()
		parents = student_model.Parent.objects.all()
		new_id = help_tools.new_id()
		return render(request, 'semiadmin/users/create.html', {'parents': parents, 'the_classes': the_classes,
			'new_id': new_id})

	def post(self, request):
		try:
			data = {
				'name':request.POST.get('name'),
				# 'email':request.POST.get('email'),
				'student_id':request.POST.get('student_id').upper(),
				'birthday':request.POST.get('birthday'),
				'gender':request.POST.get('gender'),
				'blood_group':request.POST.get('blood_group'),
				'phone':request.POST.get('phone'),
				'address':request.POST.get('address'),
				'passport_photo':request.FILES.get('student_image')
			}

			student_class = request.POST.get('class_id').upper()
			student_class_room = request.POST.get('section_id').upper()
			class_room = student_model.Class.objects.filter(the_class=student_class, 
				the_section=student_class_room).first()
			if class_room:
				data['student_class_room'] = class_room

			if request.POST.get('parent_id'):
				parent = student_model.Parent.objects.filter(pk=request.POST.get('parent_id')).first()
				if parent:
					data['parent'] = parent

			user = user_model.User.objects.create(email=request.POST.get('email'), password=request.POST.get('password'), is_student=True)
			print(data)

			student = student_model.Student.objects.create(user=user, **data)
			return JsonResponse({"status":True,"notification":"Student added successfully"})
		except:
			return JsonResponse({"status":False,"notification":"Student not added"})


class Student(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()
		return render(request, 'semiadmin/users/student.html', {'the_classes': the_classes})


class SubjectPermission(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()
		return render(request, 'semiadmin/users/subject_permission.html', {'the_classes': the_classes})

		

class ReturnStudent(View):
	def get(self, request, student_class, student_class_room):
		class_id = student_model.JustClass.objects.filter(the_class=student_class.upper()).first()
		the_classes = student_model.Class.objects.filter(the_class=class_id).values_list('the_section').distinct()
		student_rooms = [i[0] for i in the_classes]

		the_classes = student_model.JustClass.objects.all()

		return render(request, 'semiadmin/users/return_student.html', {'student_rooms': student_rooms, 
			'student_class': student_class,
			'student_class_room': student_class_room,
			'the_classes': the_classes})


class TeacherPermission(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()
		return render(request, 'semiadmin/users/permission.html', {'the_classes': the_classes})
			

class Parent(View):
	def get(self, request):
		tbodys = student_model.Parent.objects.all()
		theads = ['Srno.', 'name', 'email', 'Options']

		new_tbodys = []
		for tbody in tbodys:
			new_tbodys.append([tbody.name, tbody.email_address, tbody.pk])

		data = {
			'theads':theads,
			'tbodys':new_tbodys,
			}

		return render(request, 'semiadmin/users/parent.html', data)
		

class Accountant(View):
	def get(self, request):
		tbodys = semiadmin_model.Accountant.objects.all()
		theads = ['Srno.', 'name', 'email', 'Options']

		new_tbodys = []
		for tbody in tbodys:
			new_tbodys.append([tbody.name, tbody.email, tbody.pk])

		data = {
			'theads':theads,
			'tbodys':new_tbodys,
		}
		return render(request, 'semiadmin/users/accountant.html', data)
	

class Librarian(View):
	def get(self, request):
		tbodys = semiadmin_model.Librarian.objects.all()
		theads = ['Srno.', 'name', 'email', 'Options']

		new_tbodys = []
		for tbody in tbodys:
			new_tbodys.append([tbody.name, tbody.email, tbody.pk])

		data = {
			'theads':theads,
			'tbodys':new_tbodys,
		}
		return render(request, 'semiadmin/users/librarian.html', data)
				
	