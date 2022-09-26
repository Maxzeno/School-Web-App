from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template

from management import models as user_model
from student import models as student_model
from ... import models as teacher_model
from semiadmin import models as semiadmin_model
from semiadmin.utils import DEFAULT_IMAGE_THE_URL
from utils.html import html
from .filter import *

from utils import help as help_tools


class Marksheet(View):
	def get(self, request, id):
		sessions = student_model.Session.objects.all()
		student = student_model.Student.objects.filter(pk=id.replace('-', '/')).first()
		return render(request, 'teacher/users/marksheet.html', {'sessions': sessions, 'student': student})


class Teacher(View):
	queryset = teacher_model.Teacher.objects.filter(management_team=False).all()
	template = 'teacher/users/teacher.html'

	def get(self, request):
		tbodys = self.queryset

		new_tbodys = []
		for tbody in tbodys:
			try:
				department = tbody.department.name
			except:
				department = 'N/A'

			new_tbodys.append([tbody.name, department, tbody.designation or 'N/A'])

		data = {
			'tbodys':new_tbodys,
			}
		return render(request, self.template, data)


class Student(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()
		return render(request, 'teacher/users/student.html', {'the_classes': the_classes})
