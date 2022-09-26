from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.db.models import Q

from .academic import *
from .back_office import *
from .exam import *
from .users import *

from semiadmin import models as semiadmin_model
from student import models as student_model
from .. import models as teacher_model
from management import models as user_model
from semiadmin.utils import DEFAULT_IMAGE_THE_URL
from datetime import date
import calendar

# Create your views here.

class Dashboard(View):
	def get(self, request):
		day = date.today()
		num_attendance = semiadmin_model.Attendance.objects.filter(the_date=day).count()
		num_teachers = teacher_model.Teacher.objects.filter(management_team=False).count()
		num_staffs = teacher_model.Teacher.objects.count()
		num_parents = student_model.Parent.objects.count()
		event_calendars = semiadmin_model.EventCalendar.objects.all()[:5]
		return render(request, 'teacher/dashboard.html', {
			'num_teachers': num_teachers,
			'num_staffs': num_staffs,
			'num_parents': num_parents,
			'num_attendance': num_attendance,
			'event_calendars': event_calendars,

		})
		

class TeacherAccount(View):
	def get(self, request):
		img_url = DEFAULT_IMAGE_THE_URL
		return render(request, 'teacher/profile.html', {'img_url': img_url})
		
	def post(self, request):
		profile_image = request.POST.get('profile_image')
		name = request.POST.get('name')
		email = request.POST.get('email')
		phone = request.POST.get('phone')
		address = request.POST.get('address')
		user = user_model.User.objects.filter(pk=request.user.pk).first()
		if email:
			user.email = email
			user.save()

		auth_user = user.teacher
		auth_user.name = name
		auth_user.phone = phone
		auth_user.address = address
		auth_user.image = profile_image
		auth_user.save()
		return JsonResponse({"status":True,"notification":"profile updated successfully"})



class TeacherChangePassword(View):
	def post(self, request):
		current_password = request.POST.get('current_password')
		new_password = request.POST.get('new_password')
		confirm_password = request.POST.get('confirm_password')

		auth_user = request.user
		verified = auth_user.check_password(current_password)
		if verified:
			if new_password == confirm_password:
				auth_user.password = new_password
				auth_user.save()
				return JsonResponse({"status":True,"notification": "Password changed successfully"})
			return JsonResponse({"status":False,"notification": "Password two password did not match"})
		return JsonResponse({"status":False, "notification": "Invalid current password"})


class Logout(View):
	def get(self, request):
		logout(request)
		return redirect('registration:portal_login')