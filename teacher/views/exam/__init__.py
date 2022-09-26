from django.shortcuts import render
from django.views import View
from .filter import *
from .modal import *
from student import models as student_model
from semiadmin import models as semiadmin_model
from datetime import date
from utils import help as help_tools


class ManageMarks(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()

		return render(request, 'teacher/exam/mark.html', {'sessions': help_tools.sessioner(), 
			'the_classes': the_classes})
		

class ManageExamination(View):
	def get(self, request):
		exams = student_model.Exam.objects.all()
		return render(request, 'teacher/exam/exam.html', {'exams': exams})
	
	
class ManageCognitiveDomainScore(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()
		return render(request, 'teacher/exam/sb_description_score_manage.html', {'sessions': help_tools.sessioner(), 
			'the_classes': the_classes})
			
