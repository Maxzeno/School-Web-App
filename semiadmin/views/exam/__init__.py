from django.shortcuts import render
from django.views import View
from .filter import *
from .modal import *
from student import models as student_model
from semiadmin import models as semiadmin_model
from datetime import date
from utils import help as help_tool


class ManageMarks(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()

		return render(request, 'semiadmin/exam/mark.html', {'sessions': help_tool.sessioner(), 
			'the_classes': the_classes})
		

class ManageExamination(View):
	def get(self, request):
		exams = student_model.Exam.objects.all()
		return render(request, 'semiadmin/exam/exam.html', {'exams': exams})
			

class Grade(View):
	def get(self, request):
		grades = semiadmin_model.Grade.objects.all()
		return render(request, 'semiadmin/exam/grade.html', {'grades': grades})
			

class PassMarks(View):
	def get(self, request):
		pass_marks = student_model.PassMark.objects.all()
		return render(request, 'semiadmin/exam/pass_mark.html', {'pass_marks': pass_marks})


class ManageCognitiveDomain(View):
	def get(self, request):
		sb_descriptions = semiadmin_model.ManageCognitiveDomain.objects.all()
		return render(request, 'semiadmin/exam/sb_description.html', {'sb_descriptions': sb_descriptions})
			

class ManageCognitiveDomainScore(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()
		return render(request, 'semiadmin/exam/sb_description_score_manage.html', {'sessions': help_tool.sessioner(), 
			'the_classes': the_classes})
			

class PrincipalCommentCode(View):
	def get(self, request):
		principal_comment_codes = semiadmin_model.PrincipalCommentCode.objects.all()
		return render(request, 'semiadmin/exam/principal_comment_code.html', {'principal_comment_codes': principal_comment_codes})
				

class TeacherCommentCode(View):
	def get(self, request):
		teacher_comment_codes = semiadmin_model.TeacherCommentCode.objects.all()
		return render(request, 'semiadmin/exam/teacher_comment_code.html', {'teacher_comment_codes': teacher_comment_codes})
		

class PrincipalSubjectCode(View):
	def get(self, request):
		principal_subject_codes = semiadmin_model.PrincipalSubjectCode.objects.all()
		return render(request, 'semiadmin/exam/principal_subject_code.html', {'principal_subject_codes': principal_subject_codes})
			

class CognitiveKeyDomainScore(View):
	def get(self, request):
		cognitive_key_domain_scores = semiadmin_model.CognitiveKeyDomainScore.objects.all()
		return render(request, 'semiadmin/exam/cognitive_key_domain_score.html', {'cognitive_key_domain_scores': cognitive_key_domain_scores})


class HouseMasterCommentCode(View):
	def get(self, request):
		housemaster_comment_codes = semiadmin_model.HousemasterCommentCode.objects.all()
		return render(request, 'semiadmin/exam/housemaster_comment_code.html', {'housemaster_comment_codes': housemaster_comment_codes})
			

class Promotion(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()
		return render(request, 'semiadmin/exam/promotion.html', {'the_classes': the_classes,
			'sessions': help_tool.sessioner()})
			

class TabulationSheetMarks(View):
	def get(self, request):
		the_classes = student_model.JustClass.objects.all()
		return render(request, 'semiadmin/exam/tabulation_sheet.html', {'sessions': help_tool.sessioner(), 'the_classes': the_classes})
				
