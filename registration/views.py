from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from management.models import User
from student.models import Student

# Create your views here.

class PortalLogin(View):
	def get(self, request):
		return render(request, 'registration/portal_login.html', {})

	def post(self, request):
		email = request.POST.get('email')
		password = request.POST.get('password')
		next_url = request.session.pop('next', None)
		invalid_login_msg = 'Wrong credential'
		user = User.objects.filter(email=email).first()

		## Student not implemented so no need.
		# if not user:
		# 	student = Student.objects.filter(student_id=email).first()
		# 	user = student.user

		if user:
			is_auth = user.check_password(password)
			if is_auth:
				logout(request)
				messages.success(request, "Welcome back")

				## Not implemented "Confirm Email Functionality"				
				# if user.is_active and not user.confirmed_email:
				# 	return redirect(reverse("registration:confirm-token", kwargs={"user_id": user.id}))

				if user.is_active and user.is_semiadmin and hasattr(user, 'semiadmin'):
					login(request, user)
					return redirect(next_url or '/portal/admin/dashboard')

				## Student not implemented so no need.
				# elif user.is_active and user.is_student:
				# 	return redirect(next_url or '/portal/student/dashboard')

				## Teacher not completely implemented so no need.
				# elif user.is_active and user.is_teacher and hasattr(user, 'teacher'):
				# 	login(request, user)
				# 	return redirect(next_url or '/portal/teacher/dashboard')


				elif user.is_active:
					invalid_login_msg = 'User not portal admin'

				else:
					invalid_login_msg = 'User Deactivated'

		messages.success(request, invalid_login_msg)
		return render(request, 'registration/portal_login.html', {})
			




class AdminLogin(View):
	def get(self, request):
		msg = 'Email or password is incorrect!'
		return render(request, 'registration/admin_login.html', {'msg':None})

	# def post(self, request):
		# pass