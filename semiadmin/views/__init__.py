from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import logout
from django.db.models import Q

from .academic import *
from .accounting import *
from .back_office import *
from .exam import *
from .settings import *
from .users import *
from .. import models as semiadmin_model
from student import models as student_model
from teacher import models as teacher_model
from management import models as user_model
from ..utils import DEFAULT_IMAGE_THE_URL
from datetime import date
import calendar

# Create your views here.


class GetTemplate(TemplateView):
	def get(self, request, name):
		data = dict(request.GET)
		template_dict = {
			'parent': 'semiadmin/users/modal/parent.html',
			'teacher': 'semiadmin/users/modal/teacher.html',
			'management_team': 'semiadmin/users/modal/management_team.html',
			'accountant': 'semiadmin/users/modal/accountant.html',
			'librarian': 'semiadmin/users/modal/librarian.html',
		}
		if template_dict.get(name):
			html = render(request, template_dict[name], data)
			return HttpResponse(html)
		return None
		

class Dashboard(View):
	def get(self, request):
		day = date.today()
		range_month = calendar.monthrange(day.year, day.month)
		less = date(day.year, day.month, range_month[0]+1)
		great = date(day.year, day.month, range_month[1])

		num_attendance = semiadmin_model.Attendance.objects.filter(the_date=day).count()

		num_students = student_model.Student.objects.count()
		num_left_school = student_model.Student.objects.filter(left_school=True).count()
		num_teachers = teacher_model.Teacher.objects.filter(management_team=False).count()
		num_staffs = teacher_model.Teacher.objects.count()
		num_parents = student_model.Parent.objects.count()
		event_calendars = semiadmin_model.EventCalendar.objects.all()[:5]


		expenses = semiadmin_model.Expense.objects.filter(Q(the_date__lte=great) & Q(the_date__gte=less)).all()[:5]
		invoices = semiadmin_model.Invoice.objects.filter(Q(the_date__lte=great) & Q(the_date__gte=less)).all()[:5]
		return render(request, 'semiadmin/dashboard.html', {
			'num_students': num_students,
			'num_teachers': num_teachers,
			'num_staffs': num_staffs,
			'num_parents': num_parents,
			'num_left_school': num_left_school,
			'expenses': expenses,
			'invoices': invoices,
			'month': day.strftime('%B'),
			'event_calendars': event_calendars,
			'num_attendance': num_attendance,
		})
		

class SemiAdminAccount(View):
	def get(self, request):
		img_url = DEFAULT_IMAGE_THE_URL
		return render(request, 'semiadmin/profile.html', {'img_url': img_url})
		
	def post(self, request):
		profile_image = request.POST.get('profile_image')
		name = request.POST.get('name')
		email = request.POST.get('email')
		phone = request.POST.get('phone')
		address = request.POST.get('address')
		# print(dir(request.user.semiadmin.objects))
		user = user_model.User.objects.filter(pk=request.user.pk).first()
		if email:
			user.email = email
			user.save()

		auth_user = user.semiadmin
		auth_user.name = name
		auth_user.phone = phone
		auth_user.address = address
		auth_user.profile_image = profile_image
		auth_user.save()
		return JsonResponse({"status":True,"notification":"profile updated successfully"})



class SemiAdminChangePassword(View):
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
		return JsonResponse({"status":False, "notification": "The current_password password did not match"})


class Logout(View):
	def get(self, request):
		logout(request)
		return redirect('registration:portal_login')